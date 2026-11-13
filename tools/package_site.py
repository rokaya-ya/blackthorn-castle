"""Package only the public comic reader after validating its approved artwork."""
import shutil
from pathlib import Path
from validate_library import ROOT,validate

validate()
out=ROOT/'_site'
assert not out.exists(), 'Use a clean build checkout; do not overwrite an existing package'
out.mkdir()
for name in ['assets','chapters']:
    shutil.copytree(ROOT/name,out/name)
for name in ['index.html','read.html','publish.html','.nojekyll']:
    shutil.copyfile(ROOT/name,out/name)
print('Packaged public comic assets only into _site')
