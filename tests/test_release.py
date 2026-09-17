"""Structural compatibility, installer isolation, and actual EEL detector tests.
Usage: python3 tests/test_release.py /path/to/WDL/WDL/eel2/loose_eel
"""
import importlib.util
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

repo = Path(__file__).resolve().parents[1]
s = (repo/'Effects/DrumCloud/DrumCloud_JS.jsfx').read_text()
baseline = subprocess.check_output(['git','show','8f5b60b943bfbbe38b4bc7f7b1c05e10f1fd201f:Effects/DrumCloud/DrumCloud_JS.jsfx'], cwd=repo, text=True)
strip_hidden_marker = lambda line: re.sub(r'([>:])-', r'\1', line)
current_legacy_sliders = re.findall(r'^slider(?:[1-9]|[12][0-9]|3[0-2]):.*$', s, re.M)
baseline_legacy_sliders = re.findall(r'^slider(?:[1-9]|[12][0-9]|3[0-2]):.*$', baseline, re.M)
assert list(map(strip_hidden_marker, current_legacy_sliders)) == baseline_legacy_sliders
# Outside the deliberately changed spawn tuning expression, the entire audio section is unchanged.
audio = lambda text: text.split('@sample\n')[1].split('@gfx')[0]
assert audio(s).replace('(grain_detune + fine_tune / 100)', 'grain_detune') == audio(baseline)

# v0.27 GUI work must preserve the complete stable v0.26 parameter surface
# and audio engine byte-for-byte. ReaKit imports now resolve to bundled local files.
stable_026 = subprocess.check_output(['git','show','15b93760f8c86b03ae290d10abf34e4afb14a072:Effects/DrumCloud/DrumCloud_JS.jsfx'], cwd=repo, text=True)
# A leading '-' on the visible label is JSFX's supported native-slider hiding
# marker. Ignore only that presentation marker for compatibility comparison.
current_sliders = re.findall(r'^slider\d+:.*$', s, re.M)
stable_sliders = re.findall(r'^slider\d+:.*$', stable_026, re.M)
assert list(map(strip_hidden_marker, current_sliders)) == stable_sliders
hidden = {int(n) for n in re.findall(r'^slider(\d+):[^\n>]+>-', s, re.M)}
assert re.search(r'^slider1:.*:Sample$', s, re.M)
assert hidden == {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                  17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                  29, 30, 31, 32, 33, 34}
assert audio(s) == audio(stable_026)
reakit_imports = re.findall(r'^\s*import\s+(ReaKit/\S+)\s*$', s, re.M)
assert reakit_imports == [
    'ReaKit/Library/knobs_kbsg.jsfx-inc',
    'ReaKit/Library/buttons_kbsg.jsfx-inc',
]
reakit_root = repo/'Effects/DrumCloud/ReaKit'
for import_path in reakit_imports:
    target = repo/'Effects/DrumCloud'/import_path
    assert target.is_file(), f'missing local include: {target}'
    # The vendored subset is the complete dependency closure: neither include
    # imports another file, so no separately installed ReaKit can be consulted.
    assert not re.search(r'^\s*import\s+', target.read_text(), re.M)
assert (reakit_root/'LICENSE.txt').is_file()
assert (reakit_root/'THIRD_PARTY_CREDITS.md').is_file()

# ReaPack must install the complete local closure and its licensing files in
# the same effect directory where the relative imports resolve.
provided_reakit = {
    'ReaKit/Library/buttons_kbsg.jsfx-inc',
    'ReaKit/Library/knobs_kbsg.jsfx-inc',
    'ReaKit/LICENSE.txt',
    'ReaKit/THIRD_PARTY_CREDITS.md',
}
metadata = s.split('provides:\n', 1)[1].split('\nslider1:', 1)[0]
assert 'ReaKit/Library/*' in metadata
assert 'ReaKit/LICENSE.txt' in metadata
assert 'ReaKit/THIRD_PARTY_CREDITS.md' in metadata
assert 'ReaKit ReaPack repository https://raw.githubusercontent.com/mequaz-sudo/ReaKit/main/index.xml' in s
assert 'Report an issue https://github.com/Chmod666music/DrumCloud-ReaPack/issues' in s
index = ET.parse(repo/'index.xml')
release = index.find(".//version[@name='0.27.1']")
assert release is not None
indexed_reakit = {
    source.attrib['file'] for source in release.findall('source')
    if source.attrib.get('file', '').startswith('ReaKit/')
}
assert indexed_reakit == provided_reakit
print('PASS: local ReaKit dependency closure and v0.27.1 package metadata complete')
for slider_number in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                      17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                      29, 30, 31, 32, 33, 34):
    assert (f'dc_automate({slider_number})' in s or
            f'dc_automate_discrete({slider_number})' in s)
for slider_number in (2, 3, 4, 5, 6, 7, 9, 10, 12, 13, 14, 15, 16,
                      18, 19, 20, 21, 22, 24, 25, 26, 27, 28, 31, 33):
    assert (f'dc_end_if_released(dc_m_' in s and
            f',{slider_number});' in s) or slider_number == 4
assert 'slider_automate(2 ^ (slider_index - 1), 1)' in s
print('PASS: v0.26 sliders/audio frozen, 33 custom bindings and native Sample selector present')
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
    assert (r/'Effects/DrumCloud/ReaKit/Library/knobs_kbsg.jsfx-inc').is_file()
    assert (r/'Effects/DrumCloud/ReaKit/Library/buttons_kbsg.jsfx-inc').is_file()
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
