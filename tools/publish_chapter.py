"""Register a complete reviewed chapter, build/check the library, optionally push.

Original PNG masters stay in the production project. Existing chapters are never replaced.
"""
import argparse,hashlib,json,re,shutil,subprocess,tempfile
from pathlib import Path
from PIL import Image
from build_library import build,ROOT
from validate_library import validate

def main():
    ap=argparse.ArgumentParser();ap.add_argument('pages',type=Path);ap.add_argument('--chapter',type=int,required=True);ap.add_argument('--title',required=True);ap.add_argument('--review-json',type=Path,required=True);ap.add_argument('--expected-pages',type=int,required=True);ap.add_argument('--pdf',type=Path);ap.add_argument('--publish',action='store_true');args=ap.parse_args()
    data=json.loads((ROOT/'chapters/chapters.json').read_text(encoding='utf-8'));n=args.chapter
    cover=args.pages.parent/'cover.png'
    assert cover.is_file(), 'Save the reviewed 2:3 portrait cover as cover.png beside the pages folder'
    assert json.loads(args.review_json.read_text(encoding='utf-8')).get('coverHash')==hashlib.sha256(cover.read_bytes()).hexdigest(), 'Review must bind the approved coverHash'
    assert n==max(c['n'] for c in data['chapters'])+1,'Only the next new chapter may be registered'
    dest=ROOT/f'chapters/{n}';assert not dest.exists(),'Refusing to replace existing content'
    review=json.loads(args.review_json.read_text(encoding='utf-8'));assert review.get('status')=='PASS' and review.get('storyPages')==args.expected_pages,'A complete passing production review is required'
    files=sorted((int(f.stem),f) for f in args.pages.iterdir() if re.fullmatch(r'\d+',f.stem) and f.suffix.lower() in ['.png','.jpg','.jpeg','.webp'])
    assert [i for i,f in files]==list(range(1,args.expected_pages+1)),'Pages must be numbered 1 through expected count exactly once'
    # The completion report binds approval to every master, not just its page count.
    masters=review.get('masterHashes',{})
    assert len(masters)==len(files),'Review must list a SHA256 for every approved master'
    for i,f in files: assert masters.get(str(i))==hashlib.sha256(f.read_bytes()).hexdigest(),f'Page {i} changed after review'
    if args.pdf: assert args.pdf.is_file()
    record={'n':n,'title':args.title,'by':'','status':'complete','review':'passed','expectedPages':len(files),'cover':f'chapters/{n}/large/001.jpg','pages':[]}
    with tempfile.TemporaryDirectory(prefix='.chapter-stage-',dir=ROOT) as stage:
        stage=Path(stage)
        with Image.open(cover) as source:
            im=source.convert('RGB');w,h=im.size
            assert w>=1024 and w*3==h*2, 'Cover must be at least 1024 x 1536, in 2:3 portrait format'
            im.save(stage/'cover.jpg',quality=94,subsampling=0,optimize=True,progressive=True)
            im.resize((512,768),Image.Resampling.LANCZOS).save(stage/'cover-thumb.jpg',quality=92,subsampling=0,optimize=True,progressive=True)
            record.update(cover=f'chapters/{n}/cover.jpg',coverThumb=f'chapters/{n}/cover-thumb.jpg',coverPage={'src':f'chapters/{n}/cover.jpg','w':w,'h':h,'sha256':hashlib.sha256((stage/'cover.jpg').read_bytes()).hexdigest()})
        for i,f in files:
            with Image.open(f) as source:
                im=source.convert('RGB');w,h=im.size
                assert w>=1536 and h>=864,'Insufficient master resolution'
                for size,width,q in [('large',w,92),('small',min(960,w),88),('thumb',min(360,w),85)]:
                    out=stage/size/f'{i:03}.jpg';out.parent.mkdir(exist_ok=True)
                    image=im if width==w else im.resize((width,round(h*width/w)),Image.Resampling.LANCZOS)
                    image.save(out,quality=q,subsampling=0,optimize=True,progressive=True)
                out=stage/'large'/f'{i:03}.jpg';record['pages'].append({'w':w,'h':h,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
        if args.pdf:
            shutil.copyfile(args.pdf,stage/f'chapter-{n}.pdf');record['pdf']=f'chapters/{n}/chapter-{n}.pdf'
        shutil.copytree(stage,dest)
    data['chapters'].append(record);(ROOT/'chapters/chapters.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');build();validate()
    if args.publish:
        # Never stage unrelated project files. Failed pushes leave the reviewed commit local.
        branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
        assert branch=='main','Publish from main only after merging completed work'
        subprocess.run(['git','add',f'chapters/{n}','chapters/chapters.json','assets/comic.js','index.html','read.html'],cwd=ROOT,check=True)
        subprocess.run(['git','commit','-m',f'Publish complete Chapter {n}: {args.title}'],cwd=ROOT,check=True)
        subprocess.run(['git','push','origin','main'],cwd=ROOT,check=True)
    print(f'Chapter {n} registered. The library and chapter navigation update from the catalog automatically.')
if __name__=='__main__': main()
