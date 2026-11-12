"""Build the portable, static library from the one canonical chapter catalog."""
import json, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
def build():
    data=json.loads((ROOT/'chapters/chapters.json').read_text(encoding='utf-8'))
    data['chapters'].sort(key=lambda c:c['n'])
    (ROOT/'assets/comic.js').write_text('window.COMIC = '+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
    for name in ['index.html','read.html']:
        shutil.copyfile(ROOT/'templates'/name,ROOT/name)
    print(f"Built library: {len(data['chapters'])} chapters, {sum(len(c['pages']) for c in data['chapters'])} pages")
if __name__=='__main__': build()
