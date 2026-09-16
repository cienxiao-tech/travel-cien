"""Run python render.py to rebuild index.html from page-data.json."""
from pathlib import Path
import json,html,base64
root=Path(__file__).resolve().parent;d=json.loads((root/'page-data.json').read_text());s=(root/'page-template.html').read_text();E=lambda v:html.escape(str(v),quote=True)
def picture(n):
 v=n['visit'];photo=v.get('photo')
 if not photo:return ''
 rec=d['point_media_manifest'][n['id']];src=photo if photo.startswith('https://') else 'data:image/webp;base64,'+base64.b64encode((root/photo).read_bytes()).decode()
 out=f'<figure><img src="{src}" alt="{E(n["name"])}实景" loading="lazy" referrerpolicy="no-referrer" onerror="this.hidden=true;this.nextElementSibling.querySelector(&quot;a&quot;).textContent=&quot;图片未加载，查看来源 ↗&quot;" width="1100" height="688"><figcaption><a href="{E(rec["source_page"])}" target="_blank" rel="noopener">图片来源</a>'
 if rec.get('creator'):out+=' · '+E(rec['creator'])
 if rec.get('license_url'):out+=f' · <a href="{E(rec["license_url"])}" target="_blank" rel="noopener">许可</a>'
 return out+'</figcaption></figure>'
for day in d['days']:
 out=f'<article id="day-{day["day"]}" class="panel day-card" data-index="{day["day"]}"><div class="dayhead"><div class="daynum">DAY {day["day"]:02} · {E(day["date"])}</div><h2>{E(day["title"])}</h2></div><p>{E(day["description"])}</p><ol class="daily-stops">'
 for item in day['timeline']:
  nodes=[d['places'][k] for k in item['place_ids']];intro=item.get('intro','');out+='<li class="daily-stop"><div class="stop-shell"><div class="stop-overview"><h3 class="stop-title">'+E(item['title'])+'</h3>'
  if item['activity']:out+='<p class="stop-activity">'+E(item['activity'])+'</p>'
  if item['duration_text']:out+='<span class="stop-duration">'+E(item['duration_label'])+'：<b>'+E(item['duration_text'])+'</b></span>'
  out+='</div>'
  if nodes:
   out+='<details class="stop-more"><summary aria-label="展开或收起详情"></summary><div class="point-body">'
   # Scenic introductions are user-authored and kept together, with a single exact-place photo.
   if intro:
    illustrated=next((n for n in nodes if n['visit'].get('photo')),None)
    if illustrated:out+=picture(illustrated)
    out+='<p>'+E(intro)+'</p>'
   else:
    for n in nodes:
     out+=picture(n)
     if n['visit'].get('intro'):out+='<p>'+E(n['visit']['intro'])+'</p>'
   for n in nodes:
    recommendations=n['visit'].get('dish_recommendations',[])
    if recommendations:
     out+='<div class="dish-recommendations"><h4>推荐尝尝</h4><ul>'
     for dish in recommendations:
      out+='<li><strong>'+E(dish['name'])+'</strong><span>'+E(dish['description'])+'</span></li>'
     out+='</ul><div class="dish-source">'
     for index,url in enumerate(n['visit'].get('dish_sources',[])):
      out+=f'<a href="{E(url)}" target="_blank" rel="noopener">菜品参考{index+1 if index else ""} ↗</a> '
     out+='</div></div>'
   out+='<div class="actions">'
   for n in nodes:
    if n.get('map_url'):
     label='地图定位' if len(nodes)==1 else n['name']
     out+=f'<a href="{E(n["map_url"])}" target="_blank" rel="noopener">{E(label)} ↗</a>'
   if not any(n['visit'].get('photo') for n in nodes) and nodes[0].get('map_url'):
    out+=f'<a href="{E(nodes[0]["map_url"])}" target="_blank" rel="noopener">地点照片 ↗</a>'
   out+='</div></div></details>'
  out+='</div></li>'
 out+='</ol>'
 if day.get('closing_note'):out+='<p class="day-closing">'+E(day['closing_note'])+'</p>'
 out+='</article>';s=s.replace('@@DAY@@',out,1)
assert '@@DAY@@' not in s
(root/'index.html').write_text(s)
print('Rendered',len(d['days']),'days;',sum(len(day['timeline']) for day in d['days']),'stops')
