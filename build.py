"""Build the original static site; publish only explicit runtime dependencies to dist/."""
from pathlib import Path
import re,base64,mimetypes,shutil
from html import unescape
from content_sync import render_days
p=Path(__file__).resolve().parent
s=(p/'page-template.html').read_text(encoding='utf-8')
assert s.count('<!-- DAILY_CONTENT -->')==1
s=s.replace('<!-- DAILY_CONTENT -->',render_days((p/'itinerary-content-verified.md').read_text(encoding='utf-8')))
s=re.sub(r'<link\b(?=[^>]*href="theme.css")[^>]*>',lambda _: '<style id="balkan-design-system">'+(p/'theme.css').read_text(encoding='utf-8')+'</style>',s)
(p/'index.html').write_text(s,encoding='utf-8')
# Offline edition is retained as a download, never placed into the deployment directory.
def asset_data(relative):
    asset=p/relative
    if not asset.is_file():raise FileNotFoundError(asset)
    mime=mimetypes.guess_type(asset.name)[0] or 'application/octet-stream'
    return 'data:'+mime+';base64,'+base64.b64encode(asset.read_bytes()).decode('ascii')
offline=re.sub(r'(?<=src=")(assets/[^"<>]+)(?=")',lambda m:asset_data(m[1]),s)
offline=re.sub(r'url\(([\'"]?)(assets/[^\)\'\"]+)\1\)',lambda m:'url("'+asset_data(m[2])+'")',offline)
(p/'offline.html').write_text(offline,encoding='utf-8')
# No recursive repository copy. Only index and the local assets it references.
dist=p/'dist'
if dist.is_symlink():raise RuntimeError('dist must not be a symlink')
if dist.exists():shutil.rmtree(dist)
dist.mkdir();(dist/'index.html').write_text(s,encoding='utf-8')
refs=set(re.findall(r'(?:src|href)="(assets/[^"<>]+)"',s))
refs.update(m[1] for m in re.findall(r'url\(([\'"]?)(assets/[^\)\'\"]+)\1\)',s))
for relative in sorted(refs):
    relative=unescape(relative);source=(p/relative).resolve()
    if not source.is_relative_to((p/'assets').resolve()):raise ValueError(relative)
    if not source.is_file():raise FileNotFoundError(source)
    target=dist/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
files=[f for f in dist.rglob('*') if f.is_file()]
for f in files:
    if f.stat().st_size>25*1024*1024:raise ValueError(f'Asset too large: {f}')
    assert not any(part.startswith('.') or part=='node_modules' for part in f.relative_to(dist).parts)
print(f'Built dist/: {len(files)} files; largest {max(f.stat().st_size for f in files):,} bytes; no repository/development files.')
