"""Render the authoritative daily section using the existing HTML component classes."""
import re,html
from pathlib import Path
E=html.escape

def parse_fields(text):
    fields={};key=None
    for line in text.splitlines():
        m=re.match(r'^\* ([^：]+)：(.*)$',line)
        if m:
            key=m[1];fields[key]=m[2].strip()
        elif key and line.startswith('  * '):
            fields[key]+=('\n' if fields[key] else '')+line[4:].strip()
    return fields

def parse_days(md):
    section=md.split('## 每日行程\n',1)[1].split('\n## ',1)[0]
    days=[]
    for block in re.split(r'^### Day ',section,flags=re.M)[1:]:
        head,*points=re.split(r'^#### ',block,flags=re.M)
        day=parse_fields(head);day['number']=int(head.split(' · ')[0]);day['points']=[]
        for point in points:
            title=point.splitlines()[0];f=parse_fields(point)
            f['title']=title.split(' · ',1)[1] if ' · ' in title else title
            f['alternative']=title.startswith('备选')
            f['sequence']=None if f['alternative'] else int(title.split(' · ')[0])
            day['points'].append(f)
        days.append(day)
    assert [d['number'] for d in days]==list(range(1,13))
    ids=[f['ID'] for d in days for f in d['points'] if f.get('ID')]
    assert len(ids)==len(set(ids)),'Duplicate stable ID'
    return days

# URLs can contain balanced parentheses in Commons filenames.
LINK=re.compile(r'\[([^\]]+)\]\((https?://(?:[^\s()]|\([^()]*\))+?)\)')
def inline(s,kind='external'):
    out=[];pos=0
    for m in LINK.finditer(s):
        out.append(E(s[pos:m.start()]));out.append(f'<a class="semantic-link link-{kind}" href="{E(m[2],quote=True)}" rel="noopener" target="_blank"><span class="link-label">{E(m[1])}</span></a>');pos=m.end()
    out.append(E(s[pos:]));return ''.join(out)

def render_point(f):
    attrs=f' data-type="{E(f.get("类型",""))}"'
    if f.get('ID'):attrs+=f' id="{E(f["ID"])}"'
    if f.get('住宿ID'):attrs+=f' data-hotel-id="{E(f["住宿ID"])}"'
    title=('备选方案 · ' if f['alternative'] else '')+f['title']
    out=f'<div class="stop-shell"{attrs}><div class="stop-overview"><h3 class="stop-title">{E(title)}</h3>'
    if f.get('简介'):out+=f'<p class="stop-activity">{E(f["简介"])}</p>'
    if f.get('时间'):out+=f'<span class="stop-duration">时间：<b>{E(f["时间"])}</b></span>'
    if f.get('预计用时'):out+=f'<span class="stop-duration">{E(f.get("时长口径") or "预计用时")}：<b>{E(f["预计用时"])}</b></span>'
    out+='</div><details class="stop-more"><summary aria-label="展开或收起详情"></summary><div class="point-body">'
    if f.get('图片'):
        for src in f['图片'].split('；'):
            out+=f'<figure><img alt="{E(f.get("图片说明") or f["地点"])}" height="688" width="1100" loading="lazy" src="{E(src)}"/><figcaption>{inline(f.get("图片来源及许可", ""))}</figcaption></figure>'
    if f.get('地点'):out+=f'<p class="fine">{E(f["地点"])}</p>'
    if f.get('备注'):out+=f'<p>{E(f["备注"])}</p>'
    for key,value in f.items():
        if key=='国家方向' or '方口岸' in key:
            out+=f'<p class="fine">{E(key)}：{E(value)}</p>'
    out+='<div class="point-info">'
    if f.get('推荐菜'):
        out+='<div class="dish-recommendations"><h4>推荐尝尝</h4><ul>'
        for dish in f['推荐菜'].splitlines():
            name,sep,desc=dish.partition(' —— ')
            out+=f'<li><strong>{E(name)}</strong>'+ (f'<span> —— {E(desc)}</span>' if sep else '')+'</li>'
        out+='</ul></div>'
    if f.get('是否建议预约'):out+=f'<p class="fine">是否建议预约：{E(f["是否建议预约"])}</p>'
    if f.get('菜单参考'):out+=f'<div class="dish-source">{inline(f["菜单参考"])}</div>'
    if f.get('地图'):out+=f'<div class="actions">{inline(f["地图"],"map")}</div>'
    out+='</div></div></details></div>'
    if f['alternative']:return '<aside class="note" aria-label="Alternative Route / 备选方案">'+out+'</aside>'
    return f'<li class="daily-stop" value="{f["sequence"]}">'+out+'</li>'

def render_days(md):
    out=[]
    for d in parse_days(md):
        n=d['number'];s=f'<article class="panel day-card" data-index="{n}" id="day-{n}" data-hotel-id="{E(d.get("住宿ID",""))}"><div class="dayhead"><div class="daynum">DAY {n:02d} · {E(d["日期"])}</div><h2>{E(d["主题"])}</h2></div><p>{E(d["当天概述"])}</p>'
        s+=f'<p class="fine">住宿：{E(d["住宿"])}</p>'
        # Preserve mother order; alternative wrapper never increments the stop counter.
        s+='<ol class="daily-stops">'+''.join(('<li class="route-alternative">'+render_point(f)+'</li>') if f['alternative'] else render_point(f) for f in d['points'])+'</ol>'
        s+=f'<p class="day-closing">{E(d["当天收尾"])}</p></article>';out.append(s)
    return ''.join(out)
