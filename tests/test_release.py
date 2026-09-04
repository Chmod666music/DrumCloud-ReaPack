"""Structural compatibility, installer isolation, and actual EEL detector tests.
Usage: python3 tests/test_release.py /path/to/WDL/WDL/eel2/loose_eel
"""
import importlib.util
import re
import subprocess
import sys
import tempfile
from pathlib import Path

repo = Path(__file__).resolve().parents[1]
s = (repo/'Effects/DrumCloud/DrumCloud_JS.jsfx').read_text()
baseline = subprocess.check_output(['git','show','8f5b60b943bfbbe38b4bc7f7b1c05e10f1fd201f:Effects/DrumCloud/DrumCloud_JS.jsfx'], cwd=repo, text=True)
assert re.findall(r'^slider(?:[1-9]|[12][0-9]|3[0-2]):.*$', s, re.M) == re.findall(r'^slider(?:[1-9]|[12][0-9]|3[0-2]):.*$', baseline, re.M)
# Outside the deliberately changed spawn tuning expression, the entire audio section is unchanged.
audio = lambda text: text.split('@sample\n')[1].split('@gfx')[0]
assert audio(s).replace('(grain_detune + fine_tune / 100)', 'grain_detune') == audio(baseline)
for p in (repo/'Effects/DrumCloud/Presets').iterdir():
    assert p.read_bytes() == subprocess.check_output(['git','show','8f5b60b943bfbbe38b4bc7f7b1c05e10f1fd201f:'+ str(p.relative_to(repo))], cwd=repo)
assert len(list((repo/'Effects/DrumCloud/Samples').glob('*.wav'))) == 130
print('PASS: sliders 1–32, baseline audio except tuning, presets/action, 130 samples')
spec = importlib.util.spec_from_file_location('installer', repo/'tools/install_dev.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
with tempfile.TemporaryDirectory() as t:
    r = Path(t)
    duplicate = r/'Effects/DrumCloud-ReaPack/Effects/DrumCloud'
    duplicate.mkdir(parents=True); (duplicate/'DrumCloud_JS.jsfx').write_text('duplicate')
    user = r/'Data/DrumCloud/User Samples/mine.wav'; user.parent.mkdir(parents=True); user.write_bytes(b'keep')
    try:
        m.install(repo, r)
        raise AssertionError('duplicate not refused')
    except ValueError: pass
    m.install(repo, r, True)
    assert user.read_bytes() == b'keep'
    assert len(list((r/'Effects').rglob('*.jsfx'))) == 1
    assert len(list((r/'DrumCloud-dev-backups').rglob('DrumCloud_JS.jsfx'))) == 1
    assert not (r/'Effects/DrumCloud-ReaPack').exists()
print('PASS: installer duplicate refusal, archive, one FX, user file preserved')
# The nested directory is legitimate when registered by ReaPack.
import sqlite3
with tempfile.TemporaryDirectory() as t:
    r = Path(t)
    effect = r/'Effects/DrumCloud-ReaPack/Effects/DrumCloud/DrumCloud_JS.jsfx'
    effect.parent.mkdir(parents=True); effect.write_text('old')
    (r/'ReaPack').mkdir()
    with sqlite3.connect(r/'ReaPack/registry.db') as db:
        db.execute('CREATE TABLE files (path TEXT)')
        db.execute('INSERT INTO files VALUES (?)', (str(effect.relative_to(r)),))
    m.install(repo, r, True)
    assert effect.read_text() == s
    assert len(list((r/'Effects').rglob('*.jsfx'))) == 1
    assert not (r/'Effects/DrumCloud').exists()
print('PASS: registered ReaPack path preserved, no duplicate created or archived')


if len(sys.argv) < 2:
    raise SystemExit('Supply loose_eel to run DSP tests')
eel = str(Path(sys.argv[1]).resolve())
functions = s[s.index('function valid_number'):s.index('// ==================================================\n// FACTORY SAMPLE ROOT MAP')]
commands = s[s.index('apply_tuning && !last_apply_tuning'):s.index('last_auto_root = auto_root;',s.index('apply_tuning && !last_apply_tuning'))]
code = 'function slider_automate(x)(0;); function sliderchange(x)(0;);\n'+functions+'\n'
for sr, note, cents, harmonic in [(44100,54,-23,0),(48000,69,31,0),(96000,40,-42,0),(44100,80,47,0),(48000,60,-49,1)]:
    code += f'''
    sample_samplerate={sr}; sample_channels=1; frame_count={sr}; sample_buffer=0;
    freq=440*2^(({note}-69+{cents}/100)/12); i=0;
    loop(frame_count, sample_buffer[i]=0.5*sin(2*$pi*freq*i/sample_samplerate)+{harmonic}*0.25*sin(4*$pi*freq*i/sample_samplerate); i+=1;);
    root_note=17; fine_tune=12; analyze_loaded_root();
    printf("tone {sr} {note} {cents}: root=%d cents=%.3f confidence=%.3f status=%d\\n",detected_root_note,detected_cents,detected_confidence,analysis_status);
    analysis_status != 1 || detected_root_note != {note} || abs(detected_cents-({cents})) > 1 || root_note != 17 || fine_tune != 12 ? failures+=1;
    apply_tuning=2; last_apply_tuning=0;
    {commands}
    root_note != {note} || abs(fine_tune+({cents})) > 1 ? failures+=1;
    '''
code+='''
memset(sample_buffer,0,frame_count);
root_note=17; fine_tune=12; analyze_loaded_root();
analysis_status != 2 ? failures+=1;
apply_tuning=2; last_apply_tuning=0;
'''+commands+'''
root_note != 17 || fine_tune != 12 ? failures+=1;
i=0; loop(frame_count, sample_buffer[i]=rand(2)-1; i+=1;);
analyze_loaded_root(); analysis_status != 2 ? failures+=1;
// Three regions at different pitches must not be accepted.
i=0; loop(frame_count, f=i<frame_count*0.4 ? 220 : (i<frame_count*0.65 ? 330 : 440); sample_buffer[i]=sin(2*$pi*f*i/sample_samplerate); i+=1;);
analyze_loaded_root(); analysis_status != 2 ? failures+=1;
printf("failures=%d\\n",failures);
'''
with tempfile.TemporaryDirectory() as t:
    p=Path(t)/'detector.eel'; p.write_text(code)
    result=subprocess.run([eel,str(p)],capture_output=True,text=True)
    print(result.stdout)
    assert result.returncode==0 and 'failures=0' in result.stdout, result.stderr
print('PASS: actual EEL detector accuracy, correction sign, analysis non-mutation, silence/noise/unstable rejection')
