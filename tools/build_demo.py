from pathlib import Path
import json, html

ROOT = Path(__file__).resolve().parents[1]
audit = json.loads((ROOT / 'data/figma-typography.json').read_text())
groups = {g['id']: g for g in audit['groups']}
map_audit = json.loads((ROOT / 'data/map-coordinate-typography.json').read_text())
groups.update({g['id']: g for g in map_audit['groups']})
SOURCE = audit['source']
detail_audit = json.loads((ROOT / 'data/station-detail-typography.json').read_text())
groups.update({g['id']: g for g in detail_audit['groups']})
from detail_modules import modules as detail_modules
charging_audit = json.loads((ROOT / 'data/charging-typography.json').read_text())
groups.update({g['id']: g for g in charging_audit['groups']})
from charging_modules import modules as charging_modules
terminal_audit = json.loads((ROOT / 'data/terminal-detail-typography.json').read_text())
groups.update({g['id']: g for g in terminal_audit['groups']})
from terminal_modules import modules as terminal_modules
profile_audit = json.loads((ROOT / 'data/profile-typography.json').read_text())
groups.update({g['id']: g for g in profile_audit['groups']})
from profile_modules import modules as profile_modules

def row(name, old, new, note):
    return dict(name=name, old=old, new=new, note=note)

modules = [
    dict(key='filter', title='快捷筛选栏', old='19772:244310', new='19772:244345',
         subtitle='筛选项文字统一加大一号', height=160,
         rows=[row('筛选项文字',12,13,'综合排序、黑钻会员、星级站、停车减免、超充；同类只圈一个。')],
         marks=[dict(number='01',label='筛选项文字',indices=[0],old=12,new=13,route='top',ly=34)],
         note='仅列当前稿中已调整的筛选项；右侧偏好图标不涉及字号调整。'),
    dict(key='station', title='电站卡片', old='19772:242932', new='19772:243753',
         subtitle='站名、标签、终端数量分别校准', height=266,
         rows=[row('电站名称',15,16,'站名加大；个人桩卡片的名称使用相同调整。'),
               row('电站标签',11,12,'已收藏、最近充过、充电动态、停车减免、不对外、重卡可用；只圈「重卡可用」。'),
               row('终端数量',12,13,'兆、超、快、慢的数量与分隔符 / 同步加大；只圈一组 3/4。')],
         marks=[dict(number='02',label='电站名称',indices=[0],old=15,new=16,route='top',ly=28),
                dict(number='03',label='电站标签',indices=[9],old=11,new=12,route='right',ly=146),
                dict(number='04',label='终端数量',indices=[21,22,23],old=12,new=13,route='right',ly=209)],
         note='终端数量旁的「闲」字仍为 12；价格、距离、推荐及会员标签未调整。'),
    dict(key='personal', title='个人桩卡片', old='19772:243483', new='19772:243733',
         subtitle='沿用名称与标签调整，补充空闲状态字号', height=230,
         rows=[row('个人桩名称',15,16,'同上方「电站名称」，此处不重复圈选。'),
               row('个人桩标签',11,12,'含已收藏、最近充过、免预约、线上充、在线交易、停车免费、自由进出；同类不重复圈选。'),
               row('终端状态「空闲」',11,12,'状态文字加大，原字重保持不变。')],
         marks=[dict(number='05',label='终端状态',indices=[14],old=11,new=12,route='right',ly=162)],
         note='电站距离与充电价格维持原字号。'),
    dict(key='aggregate', title='个人桩聚合卡片', old='19772:243574', new='19772:243714',
         subtitle='聚合标题与距离说明一起校准', height=210,
         rows=[row('聚合标题',15,16,'「附近10km有12个共享个人桩」整句加大，包含数字和 km。'),
               row('距离说明',12,13,'「距离最近」与距离数值 476m 一起加大。')],
         marks=[dict(number='06',label='聚合标题',indices=[4],old=15,new=16,route='top',ly=27),
                dict(number='07',label='距离说明',indices=[5,6],old=12,new=13,route='bottom',ly=158)],
         note='「去查看」仍为 12。'),
    dict(key='charging', title='充电中卡片', old='19785:244611', new='19785:244650',
         subtitle='只调整顶部状态与电站信息', height=205,
         rows=[row('状态标题「充电中」',13,14,'状态标题加大一号。'),
               row('电站及终端信息',10,11,'右上角电站名称与终端信息加大一号。')],
         marks=[dict(number='08',label='状态标题',indices=[0],old=13,new=14,route='top',ly=28),
                dict(number='09',label='电站及终端信息',indices=[1],old=10,new=11,route='right',ly=100)],
         note='电量、费用、单位、预计时长及底部说明维持原字号。'),
    dict(key='map-coordinate', title='地图坐标卡片', old='20175:274973', new='20175:275032',
         subtitle='终端数量与分隔符统一加大一号', height=230,
         rows=[row('终端数量',12,13,'兆、超、快、慢的数量与分隔符 / 同步加大；同类只圈一组 3/3。')],
         marks=[dict(label='终端数量',indices=[5,6,7],old=12,new=13,route='right',ly=102,pad=2)],
         note='兆、超、快、慢的终端数量及分隔符 / 均按此调整；「闲」、价格与会员角标维持原字号。'),
]

def bounds(g, indices):
    boxes=[g['texts'][i][2] for i in indices]
    x=min(b[0] for b in boxes); y=min(b[1] for b in boxes)
    return x,y,max(b[0]+b[2] for b in boxes)-x,max(b[1]+b[3] for b in boxes)-y

def annotations(m,version):
    if not m['marks']: return ''
    g=groups[m[version]]; ox=20+(375-g['box'][2])/2; oy=56; labelx=435
    parts=[]
    for mark in m['marks']:
        indices=mark['indices'][version] if isinstance(mark['indices'],dict) else mark['indices']
        x,y,w,h=bounds(g,indices)
        if 'x_offsets' in mark: x+=mark['x_offsets'][version=='new']
        if 'widths' in mark: w=mark['widths'][version=='new']
        pad=mark.get('pad',4); py=min(3,pad)
        x+=ox-pad; y+=oy-py; w+=pad*2; h+=py*2
        ly=mark['ly']; end=labelx-9; lane=mark.get('lane',409)
        if mark['route']=='custom-right':
            sx=x+w; sy=y+h/2
            path=f'M {sx} {sy} H {mark["via_x"]} V {mark["bend_y"]} H {lane} V {ly+4} H {end}'
        elif mark['route']=='custom':
            sx=x+w/2; sy=y if mark['lead']=='top' else y+h
            path=f'M {sx} {sy} V {mark["bend_y"]} H {lane} V {ly+4} H {end}'
        elif mark['route']=='top':
            sx=x+w/2; sy=y
            path=f'M {sx} {sy} V 25 H 411 V {ly+4} H {end}'
        elif mark['route']=='bottom':
            sx=x+w/2; sy=y+h
            path=f'M {sx} {sy} V {ly+4} H {end}'
        else:
            sx=x+w; sy=y+h/2
            path=f'M {sx} {sy} H {lane} V {ly+4} H {end}'
        color_text = f'<text x="{labelx}" y="{ly+49}" class="mark-color">文字色 {mark["colors"][version]}</text>' if 'colors' in mark else ''
        parts.append(f'''<g class="annotation"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5"/>
<path d="{path}"/><circle cx="{end}" cy="{ly+4}" r="2.5" class="line-dot"/>
<text x="{labelx}" y="{ly}" class="mark-label">{mark['label']}</text>
<text x="{labelx}" y="{ly+24}" class="mark-value">{mark[version]}<tspan class="mark-unit"> px</tspan></text>{color_text}</g>''')
    return f'<svg class="overlay" viewBox="0 0 584 {m["height"]}" aria-label="{m["title"]}字号标注">'+''.join(parts)+'</svg>'

def figure(m,version):
    g=groups[m[version]]; w,h=g['box'][2:]; x=20+(375-w)/2
    label='原设计' if version=='old' else '视觉校准后'
    deltas=sorted(set(r['new']-r['old'] for r in m['rows'] if r.get('comparable',True)))
    delta_label='字号 '+ ' / '.join(f'+{n}' for n in deltas) if deltas else '字号未调整'
    if any(not r.get('comparable',True) for r in m['rows']): delta_label+=' · 文案变化'
    has_colors=any('colors' in r for r in m['rows'])
    if has_colors: delta_label+=' · 文字色调整'
    original_detail='原字号 · 文字色' if has_colors else '原字号'
    return f'''<figure class="figure-card {version}"><figcaption><span class="version-label"><i></i>{label}</span><span class="version-detail">{original_detail if version=='old' else delta_label}</span></figcaption>
<div class="figure-board" style="aspect-ratio:584/{m['height']}">
<img class="design-image" src="assets/{m['key']}-{version}@3x.png" width="{int(w*3)}" height="{int(h*3)}" style="left:{x/584*100}%;top:{56/m['height']*100}%;width:{w/584*100}%;height:{h/m['height']*100}%" alt="{m['title']} · {label} · Figma 3倍原图">
{annotations(m,version)}</div></figure>'''

def render_content(modules):
    cards=[]
    for i,m in enumerate(modules,1):
        cards.append(f'''<section id="{m['key']}" class="module card"><div class="module-head"><div class="module-heading"><span class="module-index">{i:02}</span><div><h2>{m['title']}</h2><p>{m['subtitle']}</p></div></div></div>
    <div class="module-body"><div class="compare-grid">{figure(m,'old')}{figure(m,'new')}</div>
    <p class="module-note">{m['note']}</p></div></section>''')

    nav=''.join(f'<a class="module-link" href="#{m["key"]}"><span>{i:02}</span>{m["title"]}</a>' for i,m in enumerate(modules,1))
    return cards,nav

CSS = '''

:root{--brand:#00ace5;--brand-soft:#e8f8fd;--ink:#16181c;--ink-2:#414345;--ink-3:#6e737c;--line:#e5e7eb;--canvas:#f5f6f8;--red:#ff625b;--board:#2f3236;--shadow:0 12px 32px rgba(31,42,55,.04);--blue:#2168f5;--blue-soft:#eef4ff;--directory-width:186px;--layout-gap:24px}
.mark-color{font-size:12px;font-weight:500}.color-detail{display:flex;align-items:center;gap:6px;margin-top:7px;font-size:11px;font-weight:500;color:var(--ink-3);white-space:nowrap}.color-detail i{width:11px;height:11px;border-radius:3px;border:1px solid #00000015;flex:none}.summary-color{margin-top:5px;font-size:11px;white-space:nowrap}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scrollbar-gutter:stable}
body{margin:0;min-width:320px;color:var(--ink);background:radial-gradient(ellipse 1100px 680px at 8% 0%,rgba(33,104,245,.065),transparent 75%),var(--canvas);font:14px/1.6 -apple-system,BlinkMacSystemFont,"PingFang SC","Helvetica Neue",Arial,sans-serif;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}a:focus-visible{outline:3px solid #2168f54d;outline-offset:4px}h1,h2,h3,p,figure{margin:0}
.header-inner{max-width:1740px;margin:auto;padding:64px 36px 0;display:grid;grid-template-columns:var(--directory-width) minmax(0,1fr);column-gap:var(--layout-gap)}
.header-inner>*{grid-column:-2/-1;min-width:0}
h1{font-size:clamp(36px,4.5vw,58px);font-weight:750;line-height:1.12;letter-spacing:-.045em}
.intro{color:var(--ink-3);margin-top:12px;font-size:14px;line-height:1.85}
.hero-copy{max-width:850px;margin-top:18px;color:var(--ink-3);font-size:16px;line-height:1.75}
.summary-pill{justify-self:start;display:inline-flex;align-items:center;gap:9px;margin-top:26px;padding:8px 13px;border:1px solid var(--line);border-radius:999px;background:rgba(255,255,255,.72);color:#525861;font-size:12px;font-weight:550}
.summary-pill strong{color:var(--ink);font-weight:650}.status-dot{width:6px;height:6px;flex:none;border-radius:50%;background:#25aa61;box-shadow:0 0 0 4px rgba(37,170,97,.1);margin:0 3px}
.page-navigation{position:sticky;top:0;z-index:30;margin-top:32px;padding:12px 0;background:var(--canvas);box-shadow:0 1px 0 rgba(31,42,55,.07)}
.navigation-inner{max-width:1740px;margin:auto;padding:0 36px;display:grid;grid-template-columns:var(--directory-width) minmax(0,1fr);column-gap:var(--layout-gap)}
.header-bottom{grid-column:-2/-1;min-width:0;display:flex;align-items:center;justify-content:space-between;gap:20px}
.page-switcher{display:inline-flex;gap:6px;padding:5px;border:1px solid #d9e0ea;border-radius:15px;background:#fff;box-shadow:0 4px 16px rgba(31,42,55,.05)}
.page-switcher a{display:flex;align-items:center;justify-content:center;min-width:104px;min-height:46px;padding:0 26px;border-radius:10px;font-size:16px;font-weight:700;color:#5a626e;white-space:nowrap;transition:color .18s,background .18s,box-shadow .18s}
.page-switcher a:hover{color:var(--blue);background:var(--blue-soft)}.page-switcher a.active{color:#fff;background:var(--blue);box-shadow:0 3px 9px rgba(33,104,245,.24)}.page-switcher a.active:hover{background:#185bdb}
.header-links{display:flex;align-items:center;gap:20px}.text-link{font-size:12px;color:#7e8590}.text-link:hover{color:var(--blue)}
.layout{max-width:1740px;margin:0 auto;padding:28px 36px 64px;display:grid;grid-template-columns:var(--directory-width) minmax(0,1fr);gap:var(--layout-gap)}.directory{position:sticky;top:24px;max-height:calc(100vh - 48px);align-self:start;border:1px solid var(--line);border-radius:14px;background:#fff;box-shadow:var(--shadow);overflow:auto}.directory-title{padding:18px 18px 15px;font-weight:650;border-bottom:1px solid var(--line)}.module-list{padding:9px}.module-link{display:flex;align-items:center;gap:10px;padding:11px 10px;font-size:13px;color:var(--ink-3);border-radius:8px;white-space:nowrap}.module-link span{font-size:11px;color:#a0a6ad;font-variant-numeric:tabular-nums}.module-link:hover{background:#f7f9fa}.module-link.active{color:#007fab;background:var(--brand-soft);font-weight:600}.module-link.active span{color:var(--brand)}.directory-foot{font-size:11px;color:#969da4;border-top:1px solid var(--line);padding:14px 18px;line-height:1.7}.content{min-width:0;display:grid;gap:24px}.card{background:white;border:1px solid var(--line);border-radius:16px;box-shadow:var(--shadow);overflow:hidden}.module{scroll-margin-top:24px}.module-head{display:flex;align-items:center;justify-content:space-between;gap:18px;padding:24px 26px;border-bottom:1px solid var(--line)}.module-heading{display:flex;align-items:center;gap:13px}.module-index{display:grid;place-items:center;width:38px;height:38px;background:var(--brand-soft);color:#0085b1;border-radius:10px;font-weight:650;font-size:13px;flex:none}h2{font-size:23px;letter-spacing:-.35px;line-height:1.4}.module-heading p{color:var(--ink-3);font-size:12px;margin-top:5px}.module-body{padding:22px 26px 24px}.compare-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.figure-card{background:var(--board);border:1px solid #262a2e;border-radius:11px;overflow:hidden;min-width:0}.figure-card figcaption{height:45px;border-bottom:1px solid #ffffff14;display:flex;align-items:center;justify-content:space-between;padding:0 16px}.version-label{display:flex;gap:8px;align-items:center;color:#f5f6f8;font-size:13px;font-weight:600}.version-label i{width:7px;height:7px;border-radius:50%;background:#ffad4f}.new .version-label i{background:#4dd5ff}.version-detail{color:#a1a8b0;font-size:11px}.figure-board{position:relative;width:100%;overflow:hidden}.design-image{position:absolute;display:block;object-fit:contain}.overlay{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible}.annotation rect{stroke:var(--red);stroke-width:1.5;fill:none}.annotation path{fill:none;stroke:var(--red);stroke-width:1.1;stroke-linejoin:round;stroke-linecap:round}.annotation .line-dot{fill:var(--red)}.annotation text{fill:#ff827d;stroke:none;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif}.mark-label{font-size:12px;font-weight:500}.annotation .mark-value{font-size:22px;font-weight:650;fill:#ff716a}.mark-unit{font-size:11px;font-weight:450}h3{font-size:15px;margin:23px 0 10px;font-weight:600}.table-wrap{overflow:auto;border:1px solid var(--line);border-radius:8px}table{border-collapse:collapse;width:100%;font-size:12px;text-align:left;line-height:1.65}th,td{padding:12px 14px;border-bottom:1px solid var(--line);vertical-align:middle}thead th{background:#f8fafb;color:#687078;font-weight:500;white-space:nowrap}tbody th{font-weight:550;color:#33393f;width:18%;min-width:130px}td{color:#747b83}tbody tr:last-child>*{border-bottom:0}.old-size,.new-size{font-size:16px;white-space:nowrap;width:12%;color:#6c737c;font-variant-numeric:tabular-nums}.new-size{font-weight:650;color:#008ab7}td small{font-size:11px;font-weight:400}td em{display:inline-block;font-size:10px;font-style:normal;background:#eaf8fc;border-radius:4px;padding:1px 5px;margin-left:8px;color:#0093bf;vertical-align:2px}.module-note{color:#9ba1a8;font-size:11px;line-height:1.8;margin-top:12px;padding-left:12px;border-left:2px solid #e6eaed}.summary-head{padding:24px 26px 8px}.summary-body{padding:16px 26px 26px}.summary tbody th{width:30%}.summary td b{color:#008ab7}.footer-note{margin-top:15px;color:#9299a0;font-size:12px}.footer-note a{color:#008ab7}
@media(min-width:1500px){.module-head{padding:25px 28px}.module-body{padding:24px 28px 26px}.figure-card figcaption{height:49px}.version-label{font-size:14px}}
@media(max-width:1199px){.layout{grid-template-columns:1fr;max-width:1240px;padding:24px 28px 50px}.directory{display:none}.module-body{padding:20px}.module-head{padding:22px}.header-inner{padding:56px 28px 0;grid-template-columns:minmax(0,1fr)}}
@media(max-width:740px){.header-inner{padding:40px 12px 0}.hero-copy{font-size:14px;margin-top:14px}.summary-pill{margin-top:20px}.header-bottom{margin-top:28px;gap:12px;flex-wrap:wrap}.page-switcher{width:100%}.page-switcher a{flex:1;min-width:0;min-height:44px;padding:0 12px;font-size:15px}.header-links{gap:14px}.layout{padding:20px 12px 40px}.content{gap:16px}.module-head{padding:18px 16px}.module-body{padding:14px}.module-index{width:32px;height:32px;border-radius:8px}h2{font-size:19px}.module-heading{gap:10px}.module-heading p{font-size:11px}.compare-grid{grid-template-columns:1fr;gap:12px}.figure-card figcaption{height:42px}table{min-width:590px}th,td{padding:10px 12px}.summary table{min-width:440px}.summary-head{padding:20px 18px 6px}.summary-body{padding:14px 18px 20px}}
@media print{.header-bottom,.directory{display:none!important}.layout{display:block;padding:0}.header-inner{padding:0 0 25px;grid-template-columns:minmax(0,1fr)}.module{break-inside:avoid;margin-bottom:20px;box-shadow:none}.module-head{padding:14px}.module-body{padding:14px}.compare-grid{grid-template-columns:repeat(2,minmax(0,1fr))}body{-webkit-print-color-adjust:exact;print-color-adjust:exact;background:#fff}.card{border-radius:8px}table{min-width:0}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important}}
'''

CSS += '\ntd em.content-change{background:#fff4df;color:#9b6a19}\n'

CSS += '''
:root{--navigation-height:82px;--anchor-offset:calc(var(--navigation-height) + 24px)}
.layout{padding-top:16px}
.directory{top:var(--anchor-offset);max-height:calc(100vh - var(--anchor-offset) - 24px)}
.module{scroll-margin-top:var(--anchor-offset)}
@media(max-width:1199px){.navigation-inner{padding:0 28px;grid-template-columns:minmax(0,1fr)}.layout{padding-top:12px}}
@media(max-width:740px){.page-navigation{margin-top:16px}.navigation-inner{padding:0 12px}.header-bottom{margin-top:0}.layout{padding-top:8px}}
@media print{.page-navigation{display:none!important}}
'''

JS='''
const links=[...document.querySelectorAll('.module-link')],sections=[...document.querySelectorAll('.module')];
const navigation=document.querySelector('.page-navigation');
function syncNav(){
  let current=sections[0];
  const threshold=navigation.getBoundingClientRect().height+26;
  for(const section of sections){if(section.getBoundingClientRect().top<=threshold)current=section;}
  if(scrollY>0&&scrollY+innerHeight>=document.documentElement.scrollHeight-2)current=sections[sections.length-1];
  links.forEach(a=>{const active=a.hash==='#'+current.id;a.classList.toggle('active',active);if(active)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');});
}
new ResizeObserver(()=>{
  document.documentElement.style.setProperty('--navigation-height',Math.ceil(navigation.getBoundingClientRect().height)+'px');
  syncNav();
}).observe(navigation);
let scheduled=false;addEventListener('scroll',()=>{if(!scheduled){scheduled=true;requestAnimationFrame(()=>{syncNav();scheduled=false;});}},{passive:true});syncNav();
'''

def render_page(modules,page_name,SOURCE,filename):
    cards,nav=render_content(modules)
    page_entries=[('首页','index.html'),('充电中','charging.html'),('电站详情','station-detail.html'),('终端详情','terminal-detail.html'),('个人中心','profile.html')]
    page_links=[]
    for name,href in page_entries:
        active='active' if name==page_name else ''
        current='aria-current="page"' if active else ''
        page_links.append(f'<a href="{href}" class="{active}" {current}>{name}</a>')
    page_navigation=''.join(page_links)
    document=f'''<!doctype html>
    <html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="APP8.0 iOS 字号校准：Figma 3倍原图、新旧字号对照及红线标注"><title>{page_name} · APP8.0 iOS 字号校准</title><link rel="icon" href="favicon.ico?v=1" sizes="16x16 32x32 48x48"><link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png?v=1"><link rel="icon" type="image/svg+xml" sizes="any" href="assets/favicon.svg?v=1"><style>{CSS}</style></head>
    <body><header class="page-header"><div class="header-inner">
    <h1>APP8.0 iOS 字号校准</h1><p class="hero-copy">针对 iOS 大屏阅读体验，校准部分文字字号。</p>
    <div class="summary-pill"><i class="status-dot" aria-hidden="true"></i><strong>{page_name} · {len(modules)} 组对照</strong><span>左侧原设计 · 右侧校准后</span></div>
    </div></header>
    <div class="page-navigation"><div class="navigation-inner">
    <div class="header-bottom"><nav class="page-switcher" aria-label="页面切换">{page_navigation}</nav><div class="header-links"><a class="text-link" href="{SOURCE}" target="_blank" rel="noopener">Figma 原稿 ↗</a></div></div>
    </div></div>
    <div class="layout"><aside class="directory"><div class="directory-title">对照目录</div><nav class="module-list" aria-label="对照模块">{nav}</nav><div class="directory-foot">同类元素只圈一个代表<br>相同调整不重复圈选</div></aside><main class="content">{''.join(cards)}</main></div>
    <script>{JS}</script></body></html>'''
    (ROOT/filename).write_text(document)
    print('Built',filename,'modules',len(modules),'marks',sum(len(m['marks']) for m in modules))

render_page(modules,'首页',audit['source'],'index.html')
render_page(detail_modules,'电站详情',detail_audit['source'],'station-detail.html')
render_page(charging_modules,'充电中',charging_audit['source'],'charging.html')
render_page(terminal_modules,'终端详情',terminal_audit['source'],'terminal-detail.html')
render_page(profile_modules,'个人中心',profile_audit['source'],'profile.html')
(ROOT/'data/changes.json').write_text(json.dumps(modules,ensure_ascii=False,indent=2))
(ROOT/'data/station-detail-changes.json').write_text(json.dumps(detail_modules,ensure_ascii=False,indent=2))
(ROOT/'data/charging-changes.json').write_text(json.dumps(charging_modules,ensure_ascii=False,indent=2))
(ROOT/'data/terminal-detail-changes.json').write_text(json.dumps(terminal_modules,ensure_ascii=False,indent=2))
(ROOT/'data/profile-changes.json').write_text(json.dumps(profile_modules,ensure_ascii=False,indent=2))
(ROOT/'README.md').write_text("""# APP8.0 iOS 字号校准

[在线预览](https://wangyekai918-star.github.io/ios-font-calibration/) · [GitHub 仓库](https://github.com/wangyekai918-star/ios-font-calibration)

双击 `index.html` 查看首页、`charging.html` 查看充电中、`station-detail.html` 查看电站详情、`terminal-detail.html` 查看终端详情、`profile.html` 查看个人中心。顶部 Tab 顺序为：首页、充电中、电站详情、终端详情、个人中心。所有图片已保存在本地，无需联网。

- 首页：6 组对照、10 处代表标注；末尾新增地图坐标卡片，兆、超、快、慢的终端数量与分隔符 / 为 12→13，「闲」、价格及会员角标维持原字号。
- 地图坐标卡片 [Figma 原稿](https://www.figma.com/design/YJ7KptNBMPFPQLWv4lZMTA/?node-id=20175-275090)。
- 电站详情：13 组对照、38 处代表标注；新增基础信息下方的特色服务（12→13），更新卡券套餐、停车、超时占用费、终端列表、电站信息、车友印象及周边服务主标题（15→16）。价格信息标题在当前设计稿中仍为 15。
- 充电中：5 组对照、13 处代表标注；顶部充电时长与充放电量为 14→15，包含超时占用费「不收取」的字号调整。
- 终端详情：8 组对照、22 处代表标注；价格、停车、超时占用费、卡券套餐、支付方式和发票主标题为 15→16，支付选择标签为 12→13。企业账户场景屏外的「余额付」仍为 12，已注明开发时统一为 13；发票末尾右括号仍为 12，保留说明。
- 个人中心：5 组对照、5 处代表标注；账户资产、常用功能、福利活动、个人桩和更多功能的相关文字均为 12→13。常用功能四个入口名称的文字色同时由 #6F7173 改为 #414345，直接在原图上标明字号与色值。
- 全部采用 Figma 3 倍 PNG 原图叠加红框、引线和实际字号；同类元素只圈一个代表，图上标注标题不显示编号。
- 页面通过原图直接对照，不再展示字号变化表格及汇总列表。
- 顶部采用简洁标题与吸顶页面导航；滚动时 Tab 固定在顶部，目录定位会预留导航高度，标注始终显示。
- 浏览器标签使用蓝底白色 Aa 图标，提供 SVG、PNG 和 ICO 格式；五个页面共用网站名称与图标。
- 价格信息包含分时价格与全天统一价，使用原始 3 倍图按 Figma 相对位置拼接。
- assets：原图。data：文字层核对数据、配置及备份。tools：页面生成脚本。

字号单位为 Figma 的 px，3 倍仅为导出倍率。两个版本始终保持相同图片缩放比例。
""")
