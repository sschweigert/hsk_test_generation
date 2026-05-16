import sys
from pypinyin import pinyin, Style
 
# Run this on a words file in the words folder to add the pinyin
# as the second argument

def add_pinyin(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
 
    results = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            results.append('')
            continue
 
        parts = stripped.split(';', 1)
        if len(parts) != 2:
            results.append(stripped)
            continue
 
        chinese = parts[0].strip()
        english = parts[1].strip()
 
        py = ' '.join([syl[0] for syl in pinyin(chinese, style=Style.TONE)])
 
        results.append(f"{chinese};{py};{english}")
 
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(results))
 
    print(f"Done! Updated {filepath}")
 
if len(sys.argv) != 2:
    print("Usage: python add_pinyin.py <filepath>")
    sys.exit(1)
 
add_pinyin(sys.argv[1])
