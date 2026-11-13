"""Reject incomplete chapters, missing art, changed approved pages and stale builds."""
import hashlib,json,re,sys
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent
def validate():
    data=json.loads((ROOT/'chapters/chapters.json').read_text(encoding='utf-8'))
    chapters=data['chapters']; nums=[c['n'] for c in chapters]
    assert nums==list(range(1,len(nums)+1)), 'Chapter order must be continuous'
    count=0
    for c in chapters:
        assert c.get('status')=='complete',f"Chapter {c['n']} is not marked complete"
        assert c.get('review')=='passed',f"Chapter {c['n']} has not passed review"
        assert c.get('expectedPages')==len(c['pages'])>0, 'Missing or extra page entries'
        folder=ROOT/f"chapters/{c['n']}/large"
        assert len(list(folder.glob('*.jpg')))==len(c['pages']),f"Unexpected page count in {folder}"
        for i,p in enumerate(c['pages'],1):
            f=ROOT/p.get('src',f"chapters/{c['n']}/large/{i:03}.jpg")
            assert f.is_relative_to(ROOT) and f.is_file(),f'Missing page: {f}'
            with Image.open(f) as im:
                im.verify()
            with Image.open(f) as im: assert im.size==(p['w'],p['h']),f'Wrong page geometry: {f}'
            assert hashlib.sha256(f.read_bytes()).hexdigest()==p['sha256'],f'Unreviewed art change: {f}'
            count+=1
        assert (ROOT/c['cover']).is_file(), 'Missing chapter cover'
        if c.get('coverPage'):
            p=c['coverPage'];f=ROOT/p['src']
            assert f.is_relative_to(ROOT) and f.is_file(), 'Missing reader cover'
            with Image.open(f) as im:
                assert im.size==(p['w'],p['h']) and im.width*3==im.height*2, 'Cover must be 2:3 portrait'
                im.verify()
            assert hashlib.sha256(f.read_bytes()).hexdigest()==p['sha256'], 'Unreviewed cover change'
            with Image.open(ROOT/c['coverThumb']) as im:
                assert im.size==(512,768), 'Wrong cover thumbnail geometry'
        if c.get('pdf'): assert (ROOT/c['pdf']).is_file(), 'Missing PDF'
    expected='window.COMIC = '+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n'
    assert (ROOT/'assets/comic.js').read_text(encoding='utf-8')==expected,'Stale comic.js; run build_library.py'
    for n in ['index.html','read.html']:
        assert (ROOT/n).read_bytes()==(ROOT/'templates'/n).read_bytes(),f'Stale {n}'
    for n in ['assets/library.css','assets/library.js','assets/book-library.css','assets/book-reader.css','assets/book-reader.js']: assert (ROOT/n).is_file()
    print(json.dumps({'status':'PASS','chapters':len(chapters),'pages':count,'allImagesVerified':True}))
    return {'chapters':len(chapters),'pages':count}
if __name__=='__main__':
    try: validate()
    except (AssertionError,Exception) as e:
        print(f'Validation failed: {e}',file=sys.stderr);sys.exit(1)
