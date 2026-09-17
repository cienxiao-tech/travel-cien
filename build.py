from pathlib import Path
import re
p=Path(__file__).resolve().parent
s=(p/"page-template.html").read_text()
s=re.sub(r'<link\b(?=[^>]*href="theme.css")[^>]*>',lambda _: '<style id="balkan-design-system">'+(p/"theme.css").read_text()+"</style>",s)
(p/"index.html").write_text(s)
