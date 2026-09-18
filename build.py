from pathlib import Path
import re
p=Path(__file__).resolve().parent
s=(p/"page-template.html").read_text()
s=re.sub(r'<link\b(?=[^>]*href="theme.css")[^>]*>',lambda _: '<style id="balkan-design-system">'+(p/"theme.css").read_text()+"</style>",s)
(p/"index.html").write_text(s)

# Standalone edition: embed visual assets; keep links and all page scripts intact.
import base64
import mimetypes

def asset_data(relative):
    asset = p / relative
    if not asset.is_file():
        raise FileNotFoundError(asset)
    mime = mimetypes.guess_type(asset.name)[0] or 'application/octet-stream'
    return 'data:' + mime + ';base64,' + base64.b64encode(asset.read_bytes()).decode('ascii')

offline = re.sub(r'(?<=src=")(assets/[^"<>]+)(?=")', lambda m: asset_data(m.group(1)), s)
offline = re.sub(r'url\(([\'"]?)(assets/[^\)\'\"]+)\1\)', lambda m: 'url("' + asset_data(m.group(2)) + '")', offline)
(p / 'offline.html').write_text(offline)
