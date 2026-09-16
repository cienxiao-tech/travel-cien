"""Run: python render.py. Reads page-data.json and writes self-contained index.html."""
from pathlib import Path
import json,re,html,base64
root=Path(__file__).resolve().parent;d=json.loads((root/'page-data.json').read_text());s=(root/'page-template.html').read_text();E=lambda x:html.escape(str(x),quote=True)
for day in d['days']:
 out=f'<article id="day-{day["day"]}" class="panel day-card" data-index="{day["day"]}"><div class="dayhead"><div class="daynum">DAY {day["day"]:02} · {E(day["date"])}</div><h2>{E(day["title"])}</h2></div><p>{E(day["description"])}</p><ol class="schedule">'
 for item in day['timeline']:
  nodes=[d['places'][k] for k in item['place_ids']];mins=item['duration_minutes'];dur=(f'{mins//60}小时'+(f'{mins%60}分钟' if mins%60 else '')) if mins and mins>=60 else (f'{mins}分钟' if mins else '')
  # A duration covers the entire authored activity, including its stated transfers.
  badge=f'<span class="schedule-badge">安排 {dur}</span>' if dur else ''
  header='<span class="point-name">'+E(item['title'])+'</span>'+badge
  if item['activity']:header+='<p class="schedule-activity">'+E(item['activity'])+'</p>'
  out+='<li class="schedule-item"><div class="schedule-time">'+E(item['time'])+'</div><div class="schedule-content">'
  if nodes:
   out+='<details class="point-card"><summary>'+header+'</summary><div class="point-body">'
   for n in nodes:
    v=n['visit'];photo=v.get('photo');out+='<h4>'+E(n['name'])+'</h4>'
    if photo:
     rec=d['point_media_manifest'][n['id']];b64=base64.b64encode((root/photo).read_bytes()).decode()
     out+=f'<figure><img src="data:image/webp;base64,{b64}" alt="{E(n["name"])}实景" loading="lazy" width="1100" height="688"><figcaption><a href="{E(rec["source_page"])}" target="_blank" rel="noopener">图片来源</a>'
     if rec.get('creator'):out+=' · '+E(rec['creator'])
     if rec.get('license_url'):out+=f' · <a href="{E(rec["license_url"])}" target="_blank" rel="noopener">许可</a>'
     out+='</figcaption></figure>'
    out+='<p>'+E(v['intro'])+'</p><div class="actions">'
    if n.get('map_url'):
     out+=f'<a href="{E(n["map_url"])}" target="_blank" rel="noopener">地图定位 ↗</a>'
     if not photo:out+=f'<a href="{E(n["map_url"])}" target="_blank" rel="noopener">地点照片 ↗</a>'
    out+='</div>'
   out+='</div></details>'
  else:out+='<div class="schedule-simple">'+header+'</div>'
  out+='</div></li>'
 out+='</ol></article>';s=s.replace('@@DAY@@',out,1)
assert '@@DAY@@' not in s
(root/'index.html').write_text(s)
print('Rendered',len(d['days']),'days;',sum(len(day['timeline']) for day in d['days']),'activities')
