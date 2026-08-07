import re, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # scriptul sta in tools/

def clean(text):
    # CSS: @keyframes hb-slow/hb-fast/heartbeat-slow/heartbeat-fast
    text = re.sub(r'@keyframes hb-slow\s*\{[^}]*\}\s*', '', text)
    text = re.sub(r'@keyframes hb-fast\s*\{[^}]*\}\s*', '', text)
    text = re.sub(r'@keyframes heartbeat-slow\s*\{[^}]*\}\s*', '', text)
    text = re.sub(r'@keyframes heartbeat-fast\s*\{[^}]*\}\s*', '', text)
    # CSS: .heart-marker and .heart-badge blocks (multiline)
    text = re.sub(r'\.heart-marker[\w\s\.]*\{[^}]*\}\s*', '', text)
    text = re.sub(r'\.heart-badge[\w\s\.]*\{[^}]*\}\s*', '', text)
    # JS: const heartSteps = { ... };
    text = re.sub(r'const heartSteps\s*=\s*\{[^}]*\};\s*', '', text)
    # JS: let heartEl = null;
    text = re.sub(r'let heartEl\s*=\s*null;\s*', '', text)
    # JS: function removeHeart() { ... }
    text = re.sub(r'function removeHeart\(\)\s*\{[^}]*\}\s*', '', text)
    # JS: function showHeart(square, fast) { multi-line }
    text = re.sub(r'function showHeart\([^)]*\)\s*\{.*?\}\s*', '', text, flags=re.DOTALL)
    # JS: if (heartSteps[s]) showHeart(...);
    text = re.sub(r'\s*if\s*\(heartSteps\[s\]\)\s*showHeart\([^)]*\);\s*', '\n', text)
    # JS: inline removeHeart/showHeart calls (lines containing only these)
    text = re.sub(r'[ \t]*(?:removeHeart|showHeart)\([^)]*\);?\s*\n', '', text)
    return text

pages = [30, 31, 43, 44, 45]
for n in pages:
    path = os.path.join(BASE, f'pagina{n}.html')
    with open(path, encoding='utf-8') as f:
        original = f.read()
    cleaned = clean(original)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(cleaned)
    removed = original.count('heart') - cleaned.count('heart')
    print(f'pagina{n}.html — eliminat {removed} referinte "heart"')
