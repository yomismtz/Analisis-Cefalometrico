from pathlib import Path

ROOT = Path('.')
main = ROOT / 'app/src/main/java/com/cefalo/angulos/MainActivity.java'
if not main.exists():
    raise RuntimeError('MainActivity.java not found')

s = main.read_text(encoding='utf-8')
old = '        if (btnCvm != null) btnCvm.setVisibility(View.GONE);\n'
new = '''        // CVM uses the same lateral cephalogram and is a validated complementary
        // skeletal-maturation assessment. Keep it accessible in the dedicated
        // lateral-skull edition instead of silently removing the capability.
        if (btnCvm != null) btnCvm.setVisibility(View.VISIBLE);\n'''
if old in s:
    s = s.replace(old, new, 1)
elif 'if (btnCvm != null) btnCvm.setVisibility(View.VISIBLE);' not in s:
    raise RuntimeError('Could not restore CVM access; standalone visibility block changed upstream')
main.write_text(s, encoding='utf-8')

# Guard against accidentally re-hiding the assessment in a future generator pass.
final = main.read_text(encoding='utf-8')
if 'if (btnCvm != null) btnCvm.setVisibility(View.VISIBLE);' not in final:
    raise RuntimeError('CVM access guard failed')

print('CVM C2-C4 skeletal maturation remains accessible in the lateral-skull edition.')
