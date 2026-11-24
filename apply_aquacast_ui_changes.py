from pathlib import Path
import re,sys
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path.cwd()
html=root/'index.html'; app=root/'js/app.js'; css=root/'css/styles.css'; chart=root/'js/chart-mode.js'
for p in (html,app,css,chart):
 if not p.exists(): raise SystemExit(f'Missing {p}; run against the root of AQUACAST-2ND-Repo')
def replace_once(s,a,b,name):
 if s.count(a)!=1: raise RuntimeError(f'{name}: expected 1 match, found {s.count(a)}')
 return s.replace(a,b,1)
s=html.read_text(encoding='utf-8')
s=replace_once(s,'<div class="workspace-label">WORKSPACE</div>','', 'workspace label')
s=re.sub(r'\s*<button class="nav-item admin-only hidden" data-page="evaluation">.*?</button>','',s,count=1,flags=re.S)
s=re.sub(r'\s*<button class="nav-item" data-page="information">.*?</button>','',s,count=1,flags=re.S)
s=replace_once(s,'<span>Workspace</span><span class="crumb-divider">/</span>','', 'breadcrumb')
s=replace_once(s,'<label class="chart-mode-control" for="chartMode">Charts <select id="chartMode" aria-label="Chart rendering mode"><option value="auto">Auto</option><option value="online">Online</option><option value="offline">Offline</option></select></label><span id="chartModeStatus" class="chart-mode-status" aria-live="polite">Charts: Offline · Canvas</span>','', 'chart mode controls')
s=replace_once(s,'</div><button class="logout-button" id="logoutButton" type="button">Sign out</button></div>','</div></div>', 'topbar signout')
s=replace_once(s,'<button type="button" class="account-menu-action" id="accountPrivacyButton">','<div class="account-appearance"><label for="accountTheme">Appearance</label><select id="accountTheme" aria-label="Appearance theme"><option value="light">Light mode</option><option value="dark">Dark mode</option></select></div>\n            <button type="button" class="account-menu-action" id="accountPrivacyButton">','theme control')
# Admin tabs are the only way to access moved content; their underlying DOM remains unchanged.
s=replace_once(s,'<div class="admin-tariff-grid" id="adminTariffGrid"></div>','<div class="admin-tool-tabs" role="tablist" aria-label="Administrator settings sections"><button type="button" class="admin-tool-tab active" data-admin-tab="tariffs">Tariff settings</button><button type="button" class="admin-tool-tab" data-admin-tab="evaluation">Model evaluation</button><button type="button" class="admin-tool-tab" data-admin-tab="information">Data &amp; model information</button></div><div id="adminTariffPanel"><div class="admin-tariff-grid" id="adminTariffGrid"></div></div>','admin tabs')
# Move original evaluation and information sections into admin page as children, preserving their original content and IDs.
for section_id in ('evaluation','information'):
 start=s.index('<section class="page-section',s.index('<div class="content-wrap">')) if False else -1
 pattern=r'\s*<section class="page-section[^>]*" id="page-'+section_id+r'"[^>]*>.*?</section>'
 m=re.search(pattern,s,re.S)
 if not m: raise RuntimeError('Cannot locate section '+section_id)
 block=m.group(0).strip()
 block=re.sub(r'class="page-section[^\"]*"', 'class="admin-tool-panel hidden"',block,count=1)
 s=s[:m.start()]+s[m.end():]
 anchor='        </section>\n        <footer class="main-footer">'
 if anchor not in s: raise RuntimeError('Admin closing anchor not found')
 s=s.replace(anchor,'          '+block+'\n'+anchor,1)
html.write_text(s,encoding='utf-8')

s=app.read_text(encoding='utf-8')
s=replace_once(s,"    if (['admin','evaluation','notices'].includes(page) && state.role!=='admin') return;","    if (['admin','evaluation','information','notices'].includes(page) && state.role!=='admin') return;\n    if(page==='evaluation'||page==='information'){setPage('admin');selectAdminTab(page);return;}",'route admin tools')
s=replace_once(s,"    if(page==='notices') window.AQUACAST_NOTIFY?.renderAdmin();","    if(page==='admin') selectAdminTab('tariffs');\n    if(page==='notices') window.AQUACAST_NOTIFY?.renderAdmin();",'admin default tab')
s=replace_once(s,"  function closeAccountMenu(){",'''  function selectAdminTab(tab){
    if(state.role!=='admin') return;
    const valid=['tariffs','evaluation','information'];if(!valid.includes(tab))tab='tariffs';
    document.querySelectorAll('[data-admin-tab]').forEach(b=>{const on=b.dataset.adminTab===tab;b.classList.toggle('active',on);b.setAttribute('aria-selected',String(on));});
    const tariffs=document.getElementById('adminTariffPanel');if(tariffs)tariffs.classList.toggle('hidden',tab!=='tariffs');
    for(const id of ['evaluation','information'])document.getElementById('page-'+id)?.classList.toggle('hidden',tab!==id);
    if(tab==='evaluation')document.dispatchEvent(new CustomEvent('aquacast:page',{detail:{page:'evaluation',station:activeStation(),role:state.role}}));
  }
  const THEME_KEY='aquacast-ui-theme';
  function applyTheme(theme){
    theme=theme==='dark'?'dark':'light';document.documentElement.dataset.theme=theme;
    const selector=document.getElementById('accountTheme');if(selector)selector.value=theme;
    try{localStorage.setItem(THEME_KEY,theme);}catch(e){}
  }
  function closeAccountMenu(){''','theme and tabs functions')
s=replace_once(s,"    $('#accountDetailsButton').addEventListener('click',()=>showAccountDialog('details'));","    $('#accountDetailsButton').addEventListener('click',()=>showAccountDialog('details'));\n    $('#accountTheme').addEventListener('change',e=>applyTheme(e.target.value));\n    try{applyTheme(localStorage.getItem(THEME_KEY)||'light');}catch(e){applyTheme('light');}",'theme events')
s=replace_once(s,"    $('#logoutButton').addEventListener('click',signOut);",'', 'remove logout handler')
s=replace_once(s,"    $('#mobileMenu').addEventListener('click',()=>toggleMobileNav());","    document.querySelectorAll('[data-admin-tab]').forEach(b=>b.addEventListener('click',()=>selectAdminTab(b.dataset.adminTab)));\n    $('#mobileMenu').addEventListener('click',()=>toggleMobileNav());",'admin tab events')
app.write_text(s,encoding='utf-8')

s=chart.read_text(encoding='utf-8')
s=replace_once(s,"  let preference = 'auto';",'', 'chart preference')
s=replace_once(s,"    if (preference === 'offline') return drawNative();",'', 'offline choice')
s=replace_once(s,"      updateStatus(preference === 'online' ? 'Charts: CDN unavailable · Offline fallback' : 'Charts: Offline fallback');","      updateStatus('Charts: Offline fallback');",'chart fallback')
s=replace_once(s,"    setMode(mode) { if (!['auto','online','offline'].includes(mode)) return; preference=mode; selectMode(); },",'', 'mode api')
s=replace_once(s,"  window.addEventListener('online', () => { if(preference==='auto') selectMode(); });","  window.addEventListener('online', selectMode);",'online listener')
s=replace_once(s,"  window.addEventListener('offline', () => { if(preference==='auto') { version++; drawNative(); } });","  window.addEventListener('offline', () => { version++; drawNative(); });",'offline listener')
s=replace_once(s,"    const select=document.getElementById('chartMode');\n    if(select) select.addEventListener('change', e=>window.AQUACAST_CHARTS.setMode(e.target.value));\n",'', 'chart select listener')
chart.write_text(s,encoding='utf-8')

s=css.read_text(encoding='utf-8')
s+='''
/* AQUACAST navigation, appearance and consolidated admin tools */
@media screen {
  .sidebar{transform:translateX(-105%)!important;visibility:hidden!important;transition:transform .22s ease,visibility .22s!important;z-index:71!important;overflow-y:auto;}
  .sidebar.open{transform:translateX(0)!important;visibility:visible!important;}
  .main-area{margin-left:0!important;}
  .mobile-menu{display:inline-flex!important;align-items:center;justify-content:center;min-width:44px;min-height:44px;cursor:pointer;}
  .mobile-scrim{display:block!important;position:fixed;inset:0;background:rgba(12,29,46,.55);z-index:70;opacity:0;visibility:hidden;pointer-events:none;transition:opacity .22s ease,visibility .22s;}
  .mobile-scrim.open{opacity:1;visibility:visible;pointer-events:auto;}
  .account-appearance{padding:10px 14px;display:flex;align-items:center;justify-content:space-between;gap:10px;font-size:13px;}
  .account-appearance select{padding:7px;border-radius:6px;border:1px solid var(--line);background:var(--surface);color:var(--text);}
  .admin-tool-tabs{display:flex;flex-wrap:wrap;gap:9px;margin:16px 0 20px;}
  .admin-tool-tab{padding:11px 15px;background:var(--surface);color:var(--text);border:1px solid var(--line);border-radius:8px;cursor:pointer;}
  .admin-tool-tab.active{background:var(--teal);color:white;border-color:var(--teal);}
  .admin-tool-panel{display:block;}
  .admin-tool-panel.hidden{display:none!important;}
}
:root[data-theme="dark"]{color-scheme:dark;--bg:#101b28;--surface:#1c2b3a;--text:#e8f0f8;--muted:#aebfd0;--line:#35495b;--soft:#243b45;--navy:#eaf3ff;--navy-2:#d9e9f8;--shadow:0 5px 20px #0005;}
:root[data-theme="dark"] body,:root[data-theme="dark"] .main-area,:root[data-theme="dark"] .content-wrap{background:var(--bg);color:var(--text);}
:root[data-theme="dark"] .topbar,:root[data-theme="dark"] .panel,:root[data-theme="dark"] .metric-card,:root[data-theme="dark"] .anomaly-card,:root[data-theme="dark"] .filter-bar,:root[data-theme="dark"] .report-sheet,:root[data-theme="dark"] .account-menu,:root[data-theme="dark"] .account-dialog-card,:root[data-theme="dark"] .table-panel,:root[data-theme="dark"] .report-stat{background:var(--surface)!important;color:var(--text)!important;border-color:var(--line)!important;}
:root[data-theme="dark"] h1,:root[data-theme="dark"] h2,:root[data-theme="dark"] h3,:root[data-theme="dark"] strong,:root[data-theme="dark"] .panel-heading h2,:root[data-theme="dark"] .page-heading h1,:root[data-theme="dark"] .review-details strong,:root[data-theme="dark"] td{color:var(--text)!important;}
:root[data-theme="dark"] p,:root[data-theme="dark"] small,:root[data-theme="dark"] .page-subtitle,:root[data-theme="dark"] .body-copy,:root[data-theme="dark"] .small-muted,:root[data-theme="dark"] .panel-heading p{color:var(--muted);}
:root[data-theme="dark"] input,:root[data-theme="dark"] select,:root[data-theme="dark"] textarea,:root[data-theme="dark"] th,:root[data-theme="dark"] .report-calendar-controls input,:root[data-theme="dark"] .report-calendar-controls select{background:#243749!important;color:var(--text)!important;border-color:var(--line)!important;}
:root[data-theme="dark"] .report-disclaimer,:root[data-theme="dark"] .prototype-banner{background:#263949;color:#e3edf7;}
:root[data-theme="dark"] .account-menu-action,:root[data-theme="dark"] .mobile-menu{color:var(--text);background:transparent;}
@media print{:root[data-theme="dark"]{color-scheme:light;--bg:#fff;--surface:#fff;--text:#202d3c;--muted:#718092;--line:#e4e9ee;--navy:#142c46;} :root[data-theme="dark"] body,:root[data-theme="dark"] .report-sheet{background:white!important;color:#202d3c!important;}}
'''
css.write_text(s,encoding='utf-8')
print('Applied changes to:',root)
