import re, subprocess, sys, tempfile
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'Effects/DrumCloud/DrumCloud_JS.jsfx'
s=p.read_text().split('@init\n',1)[1]
s=re.sub(r'^@[^\n]*','',s,flags=re.M)
s=re.sub(r'//[^\n]*','',s)
host={'file_avail','file_close','file_mem','file_open','file_riff','gfx_circle','gfx_drawnumber','gfx_drawstr','gfx_line','gfx_rect','gfx_set','gfx_setfont','gfx_triangle','midirecv','slider_automate','sliderchange','strcpy_fromslider'}
stubs={}
for m in reversed(list(re.finditer(r'\b('+'|'.join(host)+r')\s*\(',s))):
    start=m.end(); depth=1; pos=start; commas=0; quote=False
    while depth:
        c=s[pos]
        if c=='"' and s[pos-1]!='\\': quote=not quote
        if not quote:
            if c=='(': depth+=1
            elif c==')': depth-=1
            elif c==',' and depth==1: commas+=1
        pos+=1
    n=commas+1 if s[start:pos-1].strip() else 0
    name=m.group(1)+'_stub'+str(n)
    stubs[name]=n
    s=s[:m.start()]+name+'('+s[start:]
pre='\n'.join('function '+name+'('+','.join('a'+str(i) for i in range(n))+')(0;);' for name,n in stubs.items())
generated = Path(tempfile.mkdtemp())/'full_compile.eel'
generated.write_text(pre+'\n'+s[:s.index('max_grains = 32;')]+'\n0 ? (\n'+s[s.index('max_grains = 32;'):]+'\n);\nprintf("FULL_COMPILE_OK\\n");\n')
r=subprocess.run([str(Path(sys.argv[1]).resolve()),str(generated)],text=True,capture_output=True)
print(r.stdout,r.stderr)
assert r.returncode==0 and 'FULL_COMPILE_OK' in r.stdout

generated.unlink(); generated.parent.rmdir()
