from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/"page-template.html").read_text()
s=s.replace('<link rel="stylesheet" href="theme.css">','<style id="piva-editorial-11-6">'+(p/"theme.css").read_text()+"</style>")
(p/"index.html").write_text(s)
