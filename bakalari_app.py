#!/usr/bin/env python3
"""Žákovka – průměry, cíle, absence, rozvrh, úkoly.
Spuštění: python bakalari_app.py   (jen standardní knihovna, Python 3.8+)
Heslo se nikam neukládá."""
import os, hmac, base64, json, datetime, urllib.request, urllib.parse, webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

# Lokálně běží jen na tomto počítači. Na hostingu (proměnná PORT) se otevře do internetu,
# ale jen s přístupovým heslem v proměnné APP_PIN.
HOST = os.environ.get("HOST", "0.0.0.0" if "PORT" in os.environ else "127.0.0.1")
PORT = int(os.environ.get("PORT", 8765))
PIN = os.environ.get("APP_PIN", "")

def call(url, data=None, token=None):
    req = urllib.request.Request(url, data=data, method="POST" if data else "GET")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    if data:
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

def safe(f):
    try:
        return f()
    except Exception:
        return None

def fetch_all(base, user, pwd):
    p = urllib.parse.urlparse(base if "://" in base else "https://" + base)
    if p.scheme != "https" or not p.netloc:
        raise ValueError("Adresa školy musí být https://…")
    path = p.path
    for cut in ("/api", "/next", "/login", "/default"):
        if cut in path.lower():
            path = path[:path.lower().index(cut)]
    root = f"https://{p.netloc}{path.rstrip('/')}"
    body = urllib.parse.urlencode({"client_id": "ANDR", "grant_type": "password",
                                   "username": user, "password": pwd}).encode()
    tok = call(root + "/api/login", body)["access_token"]
    today = datetime.date.today().isoformat()
    return {
        "marks": call(root + "/api/3/marks", token=tok),
        "absence": safe(lambda: call(root + "/api/3/absence/student", token=tok)),
        "timetable": safe(lambda: call(root + f"/api/3/timetable/actual?date={today}", token=tok)),
        "homeworks": safe(lambda: call(root + f"/api/3/homeworks?from={today}", token=tok)),
        "events": safe(lambda: call(root + "/api/3/events", token=tok)),
    }

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, code, data, ctype="application/json"):
        b = data if isinstance(data, bytes) else data.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)
    def _ok(self):
        if not PIN:
            return True
        try:
            got = base64.b64decode(self.headers.get("Authorization", "")[6:]).decode().split(":", 1)[1]
        except Exception:
            got = ""
        if hmac.compare_digest(got.encode(), PIN.encode()):
            return True
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Zakovka"')
        self.send_header("Content-Length", "0")
        self.end_headers()
        return False
    def do_GET(self):
        if self._ok():
            self._send(200, PAGE, "text/html")
    def do_POST(self):
        if not self._ok():
            return
        try:
            d = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            self._send(200, json.dumps(fetch_all(d["base"], d["user"], d["pass"])))
        except Exception as e:
            self._send(400, json.dumps({"error": f"Přihlášení nebo načtení selhalo: {e}"}))

PAGE = r'''<!doctype html>
<html lang="cs"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Žákovka">
<title>Žákovka</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Figtree:wght@400;500;600&display=swap">
<style>
:root{box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px);
--bg:#F2F4F9;--sf:#fff;--ink:#16203A;--mu:#6A7389;--ln:#E3E7F0;--ac:#4B4DED;--acs:#E9E9FD;
--g1:#0E8F72;--g2:#4C9F4F;--g3:#B98300;--g4:#D9622B;--g5:#D13B3B}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0F1424;--sf:#181F36;--ink:#EEF1FA;--mu:#98A1BA;--ln:#262E4A;--ac:#8F91FF;--acs:#262A55;--g1:#2CC5A0;--g2:#7BC47E;--g3:#E0B034;--g4:#F08A55;--g5:#F06A6A}}
:root[data-theme="dark"]{--bg:#0F1424;--sf:#181F36;--ink:#EEF1FA;--mu:#98A1BA;--ln:#262E4A;--ac:#8F91FF;--acs:#262A55;--g1:#2CC5A0;--g2:#7BC47E;--g3:#E0B034;--g4:#F08A55;--g5:#F06A6A}
html{scroll-padding-top:env(safe-area-inset-top,0px)}
*{box-sizing:border-box}
body{margin:0 auto;max-width:560px;padding:20px 20px 104px;background:var(--bg);color:var(--ink);font:400 16px/1.45 Figtree,system-ui,sans-serif}
h1,h2,.num{font-family:"Bricolage Grotesque",system-ui,sans-serif;letter-spacing:-.02em;margin:0}
h1{font-size:1.5rem;font-weight:700}h2{font-size:1.15rem;font-weight:700;margin:32px 0 6px}
.mu{color:var(--mu);font-size:.9rem}
.hero{padding:28px 0 8px}.hero .num{font-size:5.5rem;line-height:1;font-weight:700}
.scale{position:relative;height:6px;border-radius:3px;margin:18px 0 8px;background:linear-gradient(90deg,var(--g1),var(--g2),var(--g3),var(--g4),var(--g5))}
.knob{position:absolute;top:50%;width:20px;height:20px;border-radius:50%;background:var(--bg);border:4px solid var(--ink);transform:translate(-50%,-50%)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:20px}
.two .num{font-size:1.6rem;font-weight:700}
.list>*{padding:14px 0;border-bottom:1px solid var(--ln)}.list>*:last-child{border:0}
.row{display:flex;justify-content:space-between;align-items:center;gap:12px}
.pill{display:inline-block;padding:2px 10px;border-radius:99px;font-size:.85rem;font-weight:600;background:var(--acs);color:var(--ac)}
.badge{min-width:30px;text-align:center;padding:2px 8px;border-radius:8px;font-weight:600;font-size:.9rem}
.track{position:relative;height:30px;margin:12px 4px 0}
.track:before{content:"";position:absolute;left:0;right:0;top:50%;height:2px;background:var(--ln)}
.tk{position:absolute;bottom:-14px;transform:translateX(-50%);font-size:.7rem;color:var(--mu)}
.dot{position:absolute;top:50%;transform:translate(-50%,-50%);border-radius:4px}
.dot.hyp{opacity:.55;outline:2px dashed var(--ink);outline-offset:1px}
.avgm{position:absolute;top:50%;width:18px;height:18px;border-radius:50%;border:3px solid;background:var(--bg);transform:translate(-50%,-50%)}
button,select{font:inherit;color:var(--ink);background:var(--sf);border:1px solid var(--ln);border-radius:10px;padding:7px 12px}
button{cursor:pointer}button.pri{background:var(--ac);border-color:var(--ac);color:#fff;font-weight:600}
.bare{background:none;border:0;padding:0;text-align:left;width:100%;border-radius:0}
.ctl{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:12px;font-size:.9rem}.ctl select{padding:4px 8px}
.bar{height:6px;border-radius:3px;background:var(--ln);overflow:hidden;margin-top:8px}.bar i{display:block;height:100%;border-radius:3px}
.ok{color:var(--g1)}.wn{color:var(--g3)}.er{color:var(--g5)}
.chk{width:24px;height:24px;border-radius:50%;border:2px solid var(--ln);padding:0;flex:none;display:grid;place-items:center}
.chk.on{background:var(--ac);border-color:var(--ac);color:#fff}
nav{position:fixed;left:0;right:0;bottom:0;background:var(--sf);border-top:1px solid var(--ln);display:flex;justify-content:center;padding:6px 8px calc(6px + env(safe-area-inset-bottom,0px))}
nav button{flex:1;max-width:110px;border:0;background:none;display:flex;flex-direction:column;align-items:center;gap:2px;font-size:.72rem;color:var(--mu);padding:6px 0}
nav button.on{color:var(--ac);font-weight:600}nav svg{width:24px;height:24px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.open{animation:op .2s ease}@keyframes op{from{opacity:0;transform:translateY(-4px)}}
@media(prefers-reduced-motion:reduce){.open{animation:none}}
input{font:inherit;color:var(--ink);background:var(--sf);border:1px solid var(--ln);border-radius:10px;padding:12px;width:100%;margin-bottom:10px}
nav:empty{display:none}
.list{background:var(--sf);border:1px solid var(--ln);border-radius:16px;padding:0 16px;overflow:hidden}
#top{margin-bottom:4px}#top:empty{display:none}.brand{font:700 1.15rem "Bricolage Grotesque",system-ui,sans-serif;letter-spacing:-.02em}
.days{display:flex;gap:8px;margin:14px 0}
.day{flex:1;display:flex;flex-direction:column;align-items:center;gap:2px;padding:8px 0;border-radius:14px;font-size:.8rem;color:var(--mu)}
.day b{font-size:1.1rem;color:var(--ink)}.day.on{background:var(--ac);border-color:var(--ac);color:#fff}.day.on b{color:#fff}
.lesson{display:flex;align-items:center;gap:14px}.lt{width:46px;display:flex;flex-direction:column;align-items:center;font-size:.75rem;color:var(--mu)}
.lt b{font:700 1.3rem "Bricolage Grotesque",system-ui,sans-serif;color:var(--ink)}
.lesson.now{background:var(--acs);margin:0 -16px;padding:14px 16px}.ls{font-weight:600}.lesson.cx .ls{text-decoration:line-through;color:var(--mu)}
.pill.bad{background:color-mix(in srgb,var(--g5) 15%,transparent);color:var(--g5)}
.enter>*{animation:up .4s cubic-bezier(.2,.7,.2,1) both}.enter>*:nth-child(2){animation-delay:.05s}.enter>*:nth-child(3){animation-delay:.1s}.enter>*:nth-child(n+4){animation-delay:.15s}
@keyframes up{from{opacity:0;transform:translateY(10px)}}
button{transition:transform .12s,opacity .12s}button:active{transform:scale(.97)}.bare:active{opacity:.6}
@media(prefers-reduced-motion:reduce){.enter>*{animation:none}button{transition:none}}
#login{position:relative;padding-top:6vh}
#login:before{content:"";position:absolute;left:-20px;right:-20px;top:-40px;height:300px;z-index:-1;background:radial-gradient(60% 90% at 50% 0,color-mix(in srgb,var(--ac) 25%,transparent),transparent)}
.logo{width:64px;height:64px;border-radius:20px;display:grid;place-items:center;color:#fff;font:700 2rem "Bricolage Grotesque",system-ui,sans-serif;background:linear-gradient(135deg,var(--ac),#9b6bff);box-shadow:0 10px 30px color-mix(in srgb,var(--ac) 35%,transparent)}
.ltitle{font-size:2.4rem;margin:20px 0 6px}.lsub{color:var(--mu);margin:0 0 28px}
.field{margin-bottom:14px}.field label{display:block;font-size:.8rem;font-weight:500;color:var(--mu);margin-bottom:6px}.field input{margin:0}
.pw{position:relative}.pw input{padding-right:90px}.pw button{position:absolute;right:6px;top:50%;transform:translateY(-50%);border:0;background:none;color:var(--ac);padding:8px}.pw button:active{transform:translateY(-50%)}
#go{width:100%;padding:14px;margin-top:6px;font-size:1.05rem}#go:disabled{opacity:.7}
.lnk{width:100%;border:0;background:none;color:var(--ac);margin-top:8px;padding:12px}
#msg{margin-top:10px;min-height:1.4em}.lock{margin-top:18px;font-size:.8rem;color:var(--mu);text-align:center}
.tag{font-size:.75rem;font-weight:600;padding:2px 8px;border-radius:99px}
.tag.test,.pill.bad{background:color-mix(in srgb,var(--g5) 15%,transparent);color:var(--g5)}
.tag.ukol{background:var(--acs);color:var(--ac)}.tag.akce{background:color-mix(in srgb,var(--g3) 18%,transparent);color:var(--g3)}
.pill.ok{background:color-mix(in srgb,var(--g1) 15%,transparent);color:var(--g1)}
@media print{nav,.noprint{display:none!important}}
</style></head><body>
<div id="login">
<div class="logo">Ž</div>
<h1 class="ltitle">Žákovka</h1>
<p class="lsub">Známky, absence a rozvrh z Bakalářů na jednom místě.</p>
<div class="field"><label for="base">Adresa školy</label><input id="base" placeholder="https://is.skola.cz/IS" inputmode="url" autocapitalize="off" autocorrect="off"></div>
<div class="field"><label for="user">Uživatelské jméno</label><input id="user" autocapitalize="off" autocorrect="off" autocomplete="username"></div>
<div class="field"><label for="pass">Heslo</label><div class="pw"><input id="pass" type="password" autocomplete="current-password"><button id="eye" type="button">Zobrazit</button></div></div>
<button id="go" class="pri">Zobrazit přehled</button>
<button id="demo" class="lnk">Vyzkoušet s ukázkovými daty</button>
<div id="msg" class="mu" role="status"></div>
<div class="lock">Údaje se posílají jen na server tvé školy a nikam se neukládají.</div>
</div>
<header id="top" class="noprint"></header><div id="out"></div><nav id="nav" class="noprint"></nav>
<script>
const val=t=>{const m=String(t||"").trim().match(/^([1-5])(-)?$/);return m?+m[1]+(m[2]?.5:0):null};
const fmt=v=>v%1?(v+.5)+"-":""+v;
const n2=v=>v.toFixed(2).replace(".",",");
const gc=v=>`var(--g${Math.min(5,Math.max(1,Math.round(v+.01)))})`;
function h(tag,props,...kids){const e=document.createElement(tag);Object.assign(e,props||{});kids.flat().forEach(k=>e.append(k));return e}
function sel(opts,v,fn){const e=h("select",{onchange:ev=>fn(ev.target.value)});
 opts.forEach(o=>{const[a,b]=Array.isArray(o)?o:[o,o];const op=h("option",{value:a},String(b));if(String(a)===String(v))op.selected=true;e.append(op)});return e}
const M=(id,t,w,c,d,n)=>({id,t,w,c,d,n});
function dayStr(n){const d=new Date();d.setDate(d.getDate()+n);return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0")}
function demoTodo(){return[
 {id:"a",date:dayStr(1),kind:"ukol",subj:"Fyzika",title:"Příklady 1–5 ze cvičebnice"},
 {id:"b",date:dayStr(3),kind:"test",subj:"Matematika",title:"Kvadratické rovnice",desc:"Písemný test, 30 minut"},
 {id:"c",date:dayStr(5),kind:"ukol",subj:"Český jazyk",title:"Přečíst 2. kapitolu"},
 {id:"d",date:dayStr(6),kind:"test",subj:"Fyzika",title:"Pohyb a síla"},
 {id:"e",date:dayStr(9),kind:"test",subj:"Angličtina",title:"Slovíčka, unit 5"},
 {id:"f",date:dayStr(12),kind:"akce",subj:"",title:"Exkurze do muzea techniky"},
 {id:"g",date:dayStr(-1),kind:"ukol",subj:"Dějepis",title:"Referát o středověku"}]}
function demoDays(){return[
 {date:dayStr(-2),ok:6,miss:0,late:0,soon:0,sch:0,un:false},{date:dayStr(-9),ok:2,miss:2,late:0,soon:0,sch:0,un:true},
 {date:dayStr(-20),ok:0,miss:0,late:1,soon:0,sch:0,un:false},{date:dayStr(-33),ok:5,miss:0,late:0,soon:1,sch:0,un:false}]}
function demoWeek(){const p=n=>String(n).padStart(2,"0");
 const N=[["Matematika","B12"],["Český jazyk","A5"],["Angličtina","J3"],["Fyzika","F1"],["Dějepis","A8"],["Programování","PC2"],["Tělesná výchova","Tělocvična"]];
 const T=[["7:55","8:40"],["8:50","9:35"],["9:55","10:40"],["10:50","11:35"],["11:45","12:30"],["12:40","13:25"]];
 const mon=new Date();mon.setDate(mon.getDate()-((mon.getDay()+6)%7));
 return[0,1,2,3,4].map(i=>{const d=new Date(mon);d.setDate(mon.getDate()+i);
  return{date:`${d.getFullYear()}-${p(d.getMonth()+1)}-${p(d.getDate())}`,items:T.slice(0,5+(i%2)).map((t,k)=>{const n=N[(i*2+k)%N.length];
   return{h:String(k+1),from:t[0],to:t[1],s:n[0],r:n[1],c:i==2&&k==1?"Suplování":i==2&&k==4?"Odpadá":"",x:i==2&&k==4}})}})}
const DEMO={thr:30,un:1,days:demoDays(),tot:{ok:20,miss:8,late:3,soon:1,sch:0},
 subs:[
  {name:"Matematika",prev:[1.8,1.6],marks:[M(1,"1",3,"Písemka","2026-09-20"),M(2,"2-",5,"Test","2026-10-10"),M(3,"1",2,"Ústní","2026-11-02"),M(4,"2",3,"Domácí úkol","2026-11-12",1)]},
  {name:"Český jazyk",prev:[2.4,2.8],marks:[M(5,"3",4,"Diktát","2026-09-25"),M(6,"2",3,"Slohová práce","2026-10-18"),M(7,"4-",5,"Test","2026-11-05"),M(8,"3",2,"Čtenářský deník","2026-11-13",1)]},
  {name:"Angličtina",prev:[1.4,1.3],marks:[M(9,"1",2,"Slovíčka","2026-09-30"),M(10,"1-",3,"Test","2026-10-22")]},
  {name:"Fyzika",prev:[2.2,2.5],marks:[M(11,"2",3,"Referát","2026-10-01"),M(12,"3-",4,"Test","2026-11-08")]},
  {name:"Dějepis",prev:[2.0,2.2],marks:[M(13,"2",3,"Ústní","2026-09-28"),M(14,"2-",4,"Test","2026-10-25"),M(15,"1",2,"Aktivita","2026-11-10")]}],
 abs:[{n:"Matematika",l:60,b:4},{n:"Český jazyk",l:50,b:9},{n:"Angličtina",l:45,b:2},{n:"Fyzika",l:30,b:10},{n:"Dějepis",l:28,b:3}],
 tt:demoWeek(),
 todo:demoTodo()};
let DATA=DEMO;
const S={tab:"over",open:null,goal:{},hypo:{},w:{},hm:{},hw:{},seen:new Set(),theme:0};
try{S.seen=new Set(JSON.parse(localStorage.getItem("seen")||"[]"))}catch(e){}
const isNew=m=>m.n&&!S.seen.has(m.id),all=s=>s.marks.concat(S.hypo[s.name]||[]);
function avg(ms){let s=0,w=0;ms.forEach(m=>{const v=val(m.t);if(v==null)return;s+=v;w+=1});return w?s/w:null}
function trend(s){const ms=s.marks.slice().sort((a,b)=>a.d.localeCompare(b.d));return ms.map((_,i)=>avg(ms.slice(0,i+1)))}
function spark(p){if(p.length<2)return"";const x=i=>4+i*112/(p.length-1),y=v=>4+(v-1)/4*22;
 const s=document.createElementNS("http://www.w3.org/2000/svg","svg");s.setAttribute("viewBox","0 0 120 30");s.setAttribute("width","120");
 s.innerHTML=`<polyline fill="none" stroke="${gc(p[p.length-1])}" stroke-width="2.5" stroke-linecap="round" points="${p.map((v,i)=>x(i)+","+y(v)).join(" ")}"/>`;return s}
function goalText(s,t){let sm=0,W=0;all(s).forEach(m=>{const v=val(m.t);if(v!=null){sm+=v;W+=1}});
 const x=((t+.5)*(W+1)-sm);
 if(x>=5)return["ok","Cíl už máš splněný, stačí i pětka."];
 if(x<1)return["er","Ani s jedničkou z další písemky cíl nedoženeš."];
 return["wn",`Z další známky potřebuješ aspoň ${fmt(Math.floor(x*2)/2)}.`]}
const mo=()=>[1,1.5,2,2.5,3,3.5,4,4.5,5].map(v=>[v,fmt(v)]);
function badge(t){const v=val(t);return h("span",{className:"badge",style:`color:${gc(v)};background:color-mix(in srgb,${gc(v)} 15%,transparent)`},t)}
function subject(s){
 const a=avg(all(s)),op=S.open===s.name,hy=S.hypo[s.name]||[];
 const tr=h("div",{className:"track"},...[1,2,3,4,5].map(i=>h("span",{className:"tk",style:`left:${(i-1)*25}%`},i)));
 all(s).forEach(m=>{const v=val(m.t);if(v!=null){const z=12;tr.append(h("i",{className:"dot"+(m.c=="Fiktivní"?" hyp":""),style:`left:${(v-1)/4*100}%;width:${z}px;height:${z}px;background:${gc(v)}`}))}});
 tr.append(h("b",{className:"avgm",style:`left:${(a-1)/4*100}%;border-color:${gc(a)}`}));
 const head=h("button",{className:"bare",onclick(){S.open=op?null:s.name;draw()}},
  h("div",{className:"row"},h("span",{style:"font-weight:600"},s.name),
   h("span",{className:"num",style:`font-size:1.5rem;font-weight:700;color:${gc(a)}`},n2(a))),tr,h("div",{style:"height:16px"}));
 const box=h("div",{},head);
 if(op){const g=S.goal[s.name]||2,hm=S.hm[s.name]||2,[c,t]=goalText(s,+g),base=avg(s.marks);
  box.append(h("div",{className:"open"},
   h("div",{className:"row"},h("span",{className:"mu"},"Vývoj průměru"),spark(trend(s))),
   h("div",{style:"margin-top:8px"},...s.marks.slice().sort((x,y)=>x.d.localeCompare(y.d)).map(m=>h("div",{className:"row mu",style:"padding:3px 0"},
    h("span",{},m.c),badge(m.t)))),
   hy.length?h("div",{className:"mu",style:"margin-top:6px"},`S fiktivními známkami: ${n2(base)} → ${n2(a)}`):"",
   h("div",{className:"ctl"},"Co když dostanu",sel(mo(),hm,v=>{S.hm[s.name]=+v}),
    h("button",{onclick(){(S.hypo[s.name]=S.hypo[s.name]||[]).push({t:fmt(+hm),w:1,d:"",c:"Fiktivní"});draw()}},"Přidat"),
    hy.length?h("button",{onclick(){S.hypo[s.name]=[];draw()}},"Zrušit"):""),
   h("div",{className:"ctl"},"Chci na vysvědčení",sel([1,2,3,4],g,v=>{S.goal[s.name]=+v;draw()})),
   h("div",{className:c,style:"margin-top:8px;font-weight:500"},t)))}
 return box}
function overview(o){
 const L=DATA.subs.map(s=>({s,a:avg(all(s))})),tot=L.reduce((x,y)=>x+y.a,0)/L.length,so=[...L].sort((x,y)=>x.a-y.a),
  b=Math.max(DATA.abs.reduce((x,y)=>x+y.b,0),DATA.tot?DATA.tot.ok+DATA.tot.miss:0),l=DATA.abs.reduce((x,y)=>x+y.l,0),p=l?b/l*100:0;
 o.append(h("div",{className:"hero"},h("div",{className:"mu"},"Celkový průměr"),h("div",{className:"num",style:"color:"+gc(tot)},n2(tot)),
  h("div",{className:"scale"},h("i",{className:"knob",style:`left:${(tot-1)/4*100}%`})),
  h("div",{className:"two"},
   h("div",{},h("div",{className:"mu"},"Nejlépe ti jde"),h("div",{className:"num"},so[0].s.name),h("div",{className:"mu"},n2(so[0].a))),
   h("div",{},h("div",{className:"mu"},"Nejvíc se vyplatí zabrat"),h("div",{className:"num"},so[so.length-1].s.name),h("div",{className:"mu"},n2(so[so.length-1].a))))));
 const bad=L.filter(x=>x.a>2.5),c1=tot<=1.5,okH=c1&&!bad.length;
 o.append(h("h2",{},"Vyznamenání"),h("div",{className:"list"},
  h("div",{className:"row"},h("b",{className:okH?"ok":"er"},okH?"Podmínky zatím splňuješ":"Podmínky zatím nesplňuješ")),
  h("div",{className:"row"},h("span",{},"Celkový průměr do 1,50"),h("span",{className:c1?"ok":"er"},(c1?"✓ ":"✕ ")+n2(tot))),
  h("div",{className:"row"},h("span",{},"Průměr každého předmětu do 2,50"),h("span",{className:bad.length?"er":"ok",style:"text-align:right"},bad.length?"✕ "+bad.map(x=>x.s.name).join(", "):"✓")),
  h("div",{className:"mu"},"Orientační údaj. Pravidla školy a hodnocení chování se mohou lišit.")));
 o.append(h("h2",{},"Absence"),h("div",{className:"list"},h("div",{},
  h("div",{className:"row"},h("span",{className:"num",style:"font-size:2rem;font-weight:700"},l?n2(p).replace(/,?0$/,"")+" %":b+" h"),h("span",{className:"mu"},`${b}${l?" z "+l:""} hodin${l?", limit "+DATA.thr+" %":""}`)),
  h("div",{className:"bar"},h("i",{style:`width:${Math.min(100,p/DATA.thr*100)}%;background:var(--${p>=DATA.thr?"g5":"g1"})`})),
  DATA.tot?h("div",{className:"mu",style:"margin-top:8px"},`Omluveno ${DATA.tot.ok} h, neomluveno ${DATA.tot.miss} h, pozdní příchody ${DATA.tot.late}`):"")));
 if(DATA.subs.every(s=>s.prev))o.append(h("h2",{},"Oproti loňsku"),h("div",{className:"list"},...L.map(({s,a})=>{const d=a-s.prev[1];
  return h("div",{className:"row"},h("span",{},s.name),h("span",{className:d<-.05?"ok":d>.05?"er":"mu"},d<-.05?"lepší o "+n2(-d):d>.05?"horší o "+n2(d):"stejné"))})))}
function daysBlock(o){const D=DATA.days||[];if(!D.length)return;
 o.append(h("h2",{},"Dny s absencí"),h("div",{className:"list"},...D.map(d=>{
  const parts=[d.ok&&`omluveno ${d.ok} h`,d.miss&&`neomluveno ${d.miss} h`,d.late&&`pozdní příchod ${d.late} h`,d.soon&&`předčasný odchod ${d.soon} h`,d.sch&&`škola ${d.sch} h`].filter(Boolean);
  return h("div",{className:"row"},h("span",{},h("div",{style:"font-weight:600"},new Date(d.date+"T12:00:00").toLocaleDateString("cs-CZ",{weekday:"long",day:"numeric",month:"long"})),h("div",{className:"mu"},parts.join(", ")||"bez zameškaných hodin")),
   d.un||d.miss?h("span",{className:"pill bad"},d.un?"k omluvení":"neomluveno"):h("span",{className:"pill ok"},"omluveno"))})))}
function absence(o){
 o.append(h("h1",{},"Absence"),h("div",{className:"mu"},`Limit je ${DATA.thr} % zameškaných hodin v předmětu.`),
  DATA.tot?h("div",{className:"list",style:"margin-top:12px"},...[["Omluvené hodiny",DATA.tot.ok],["Neomluvené hodiny",DATA.tot.miss],["Pozdní příchody",DATA.tot.late],["Předčasné odchody",DATA.tot.soon],["Školní akce",DATA.tot.sch]].map(([k,v])=>h("div",{className:"row"},h("span",{},k),h("b",{className:k=="Neomluvené hodiny"&&v?"er":""},String(v))))):"",h("div",{className:"list",style:"margin-top:12px"},
  ...DATA.abs.map(a=>({...a,p:a.l?a.b/a.l*100:0,left:Math.floor(DATA.thr/100*a.l-a.b+1e-9)})).sort((x,y)=>y.p-x.p).map(x=>
   h("div",{},h("div",{className:"row"},h("span",{style:"font-weight:600"},x.n),h("span",{className:x.p>=DATA.thr?"er":""},n2(x.p)+" %")),
    h("div",{className:"bar"},h("i",{style:`width:${Math.min(100,x.p/DATA.thr*100)}%;background:var(--${x.p>=DATA.thr?"g5":x.p>=DATA.thr*.6?"g3":"g1"})`})),
    h("div",{className:"mu",style:"margin-top:6px"},x.left<0?"Limit je překročený.":`Můžeš zameškat ještě ${x.left} ${x.left==1?"hodinu":x.left>=2&&x.left<=4?"hodiny":"hodin"}.`)))));
 daysBlock(o);if(DATA.un)o.append(h("div",{className:"er",style:"margin-top:16px;font-weight:600"},`Máš ${DATA.un} ${DATA.un==1?"neomluvený den":DATA.un<5?"neomluvené dny":"neomluvených dnů"}.`))}
function today(o){
 const days=DATA.tt.filter(d=>{const g=new Date(d.date+"T12:00:00").getDay();return g>=1&&g<=5});
 const n=new Date(),ds=`${n.getFullYear()}-${pad(n.getMonth()+1)}-${pad(n.getDate())}`;
 if(!S.day||!days.some(d=>d.date==S.day))S.day=(days.find(d=>d.date==ds)||days.find(d=>d.date>ds)||days[0]||{}).date;
 o.append(h("h1",{},"Rozvrh"));
 if(!days.length)o.append(h("div",{className:"mu",style:"margin-top:8px"},"Rozvrh se nepodařilo načíst."));
 else{
  o.append(h("div",{className:"days"},...days.map(d=>{const dt=new Date(d.date+"T12:00:00");
   return h("button",{className:"day"+(d.date==S.day?" on":""),onclick(){S.day=d.date;draw()}},h("span",{},dt.toLocaleDateString("cs-CZ",{weekday:"short"}).replace(".","")),h("b",{},String(dt.getDate())))})));
  const d=days.find(x=>x.date==S.day),hm=pad(n.getHours())+":"+pad(n.getMinutes()),tm=t=>(t||"").padStart(5,"0");
  o.append(d.items.length?h("div",{className:"list"},...d.items.map(r=>{const now=d.date==ds&&r.from&&tm(r.from)<=hm&&hm<tm(r.to);
   return h("div",{className:"lesson"+(now?" now":"")+(r.x?" cx":"")},
    h("div",{className:"lt"},h("b",{},r.h),h("span",{},r.from)),
    h("div",{style:"flex:1;min-width:0"},h("div",{className:"ls"},r.s),h("div",{className:"mu"},r.r)),
    r.c?h("span",{className:"pill"+(r.x?" bad":"")},r.c):now?h("span",{className:"pill"},"teď"):"")})):h("div",{className:"mu",style:"margin-top:12px"},"V tento den nejsou žádné hodiny."))}
 }
function todo(o){
 const f=S.tf||"all",today=dayStr(0),dd=x=>Math.round((new Date(x.date+"T12:00:00")-new Date(today+"T12:00:00"))/864e5);
 const dn=n=>n==1?"den":n<5?"dny":"dní";
 const items=DATA.todo.filter(x=>(f=="all"||x.kind==f)&&(x.kind=="ukol"||dd(x)>=0)).sort((a,b)=>a.date.localeCompare(b.date));
 const grp=x=>{const d=dd(x);return x.kind=="ukol"&&S.hw[x.id]?"Hotovo":d<0?"Po termínu":d==0?"Dnes":d==1?"Zítra":d<=7?"Tento týden":"Později"};
 o.append(h("h1",{},"To-do"),h("div",{className:"days",style:"margin:12px 0"},...[["all","Vše"],["test","Testy"],["ukol","Úkoly"],["akce","Akce"]].map(([k,n])=>
  h("button",{className:"day"+(f==k?" on":""),style:"padding:10px 0;font-size:.9rem",onclick(){S.tf=k;draw()}},n))));
 if(!items.length)o.append(h("div",{className:"mu"},"Nic naplánováno."));
 ["Po termínu","Dnes","Zítra","Tento týden","Později","Hotovo"].forEach(g=>{const L=items.filter(x=>grp(x)==g);if(!L.length)return;
  o.append(h("h2",{},g),h("div",{className:"list"},...L.map(x=>{const d=dd(x),done=x.kind=="ukol"&&S.hw[x.id];
   return h("div",{className:"row",style:"align-items:flex-start;"+(done?"opacity:.5":"")},
    h("span",{style:"flex:1;min-width:0"},
     h("div",{},h("span",{className:"tag "+x.kind},{test:"Test",ukol:"Úkol",akce:"Akce"}[x.kind]),x.subj?h("b",{style:"margin-left:8px"},x.subj):""),
     h("div",{style:"margin-top:4px;font-weight:500"+(done?";text-decoration:line-through":"")},x.title||"Bez popisu"),
     x.desc?h("div",{className:"mu"},x.desc):""),
    h("span",{style:"text-align:right;white-space:nowrap"},h("div",{style:"font-weight:600"},new Date(x.date+"T12:00:00").toLocaleDateString("cs-CZ",{weekday:"short",day:"numeric",month:"numeric"})),
     h("div",{className:"mu"},d<0?(d==-1?"včera":"před "+(-d)+" dny"):d==0?"dnes":d==1?"zítra":"za "+d+" "+dn(d))),
    x.kind=="ukol"?h("button",{className:"chk"+(done?" on":""),"aria-label":"Hotovo",onclick(){S.hw[x.id]=!S.hw[x.id];draw()}},done?"✓":""):"")})))})}
function more(o){
 const nm=["automatický","světlý","tmavý"];
 o.append(h("h1",{},"Více"),h("div",{className:"list",style:"margin-top:12px"},h("div",{className:"row"},h("span",{},"Účet"),h("button",{onclick(){location.reload()}},"Odhlásit")),
  
  DATA.raw?h("div",{},h("div",{style:"font-weight:500"},"Data absence ze školy"),h("pre",{style:"white-space:pre-wrap;word-break:break-all;font-size:.7rem;color:var(--mu)"},DATA.raw)):"",
  
  h("div",{className:"row"},h("span",{},"Vzhled: "+nm[S.theme]),h("button",{onclick(){S.theme=(S.theme+1)%3;const r=document.documentElement;S.theme?r.setAttribute("data-theme",S.theme==1?"light":"dark"):r.removeAttribute("data-theme");draw()}},"Změnit")),
  h("div",{className:"row"},h("span",{},"Uložit přehled jako PDF"),h("button",{onclick(){try{window.print()}catch(e){}}},"Tisk")),
  h("div",{},h("div",{style:"font-weight:500"},"Přidat na plochu iPhonu"),h("div",{className:"mu"},"V Safari ťukni na Sdílet a vyber „Přidat na plochu“."))))}
const IC={over:"M4 11l8-7 8 7v9H4zM10 20v-6h4v6",subj:"M5 6h14M5 12h14M5 18h9",abs:"M7 3v3M17 3v3M4 8h16v12H4zM9 13l6 4M15 13l-6 4",today:"M12 7v5l3 2M12 3a9 9 0 100 18 9 9 0 000-18",more:"M6 12h.01M12 12h.01M18 12h.01",todo:"M5 7l2 2 3-3M5 15l2 2 3-3M13 8h6M13 16h6"};
const TABS=[["over","Přehled"],["subj","Předměty"],["abs","Absence"],["today","Rozvrh"],["todo","To-do"],["more","Více"]];
function draw(){
 const nav=document.getElementById("nav");nav.replaceChildren(...TABS.map(([k,n])=>{const b=h("button",{className:S.tab==k?"on":"",onclick(){S.tab=k;draw();scrollTo(0,0)}});
  b.innerHTML=`<svg viewBox="0 0 24 24"><path d="${IC[k]}"/></svg>`;b.append(n);return b}));
 const top=document.getElementById("top");top.replaceChildren(h("div",{className:"row"},h("span",{className:"brand"},"Žákovka"),h("span",{className:"mu"},new Date().toLocaleDateString("cs-CZ",{weekday:"long",day:"numeric",month:"long"}))));
 const o=document.getElementById("out");o.replaceChildren();o.className=S.last!==S.tab?"enter":"";S.last=S.tab;
 ({over:overview,subj:o=>{o.append(h("h1",{},"Předměty"),h("div",{className:"mu"},"Každá tečka je jedna známka, kroužek je průměr. Ťukni na předmět."),
  h("div",{className:"list",style:"margin-top:12px"},...DATA.subs.slice().sort((a,b)=>avg(all(a))-avg(all(b))).map(subject)))},abs:absence,today,todo,more})[S.tab](o)}
const $=id=>document.getElementById(id);
const pad=n=>String(n).padStart(2,"0");
function convTT(t){
 if(!t||!t.Days)return[];
 const hrs={},sub={},room={};
 (t.Hours||[]).forEach(x=>hrs[x.Id]=x);(t.Subjects||[]).forEach(x=>sub[x.Id]=x.Name);(t.Rooms||[]).forEach(x=>room[x.Id]=x.Abbrev);
 return t.Days.map(d=>({date:(d.Date||"").slice(0,10),
  items:(d.Atoms||[]).slice().sort((a,b)=>a.HourId-b.HourId).map(a=>{const hr=hrs[a.HourId]||{},c=a.Change;
   return{h:hr.Caption||"",from:hr.BeginTime||"",to:hr.EndTime||"",s:sub[a.SubjectId]||(c&&c.Description)||"—",r:room[a.RoomId]||"",
    c:c?(c.TypeName||c.Description||"Změna"):"",x:!!(c&&/cancel|remov|odpad|zruš/i.test((c.ChangeType||"")+(c.TypeName||"")))}})})).filter(d=>d.date)}
function dIso(x){if(!x)return"";const d=new Date(x);return isNaN(d)?String(x).slice(0,10):`${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}`}
function convHW(r){const L=r&&(r.Homeworks||r.homeworks)||[];
 return L.filter(x=>!x.Done).map((x,i)=>({id:"h"+(x.ID||x.Id||i),date:dIso(x.DateEnd||x.Date),kind:"ukol",subj:(x.Subject&&x.Subject.Name)||x.SubjectName||"",title:x.Content||x.Text||x.Notice||"",desc:""})).filter(x=>x.date)}
function convEV(r){const L=r&&(r.Events||r.events)||[];
 return L.map((e,i)=>{const t=(e.Times&&e.Times[0])||{},typ=(e.EventType&&e.EventType.Name)||"",txt=(e.Title||"")+" "+typ+" "+(e.Description||"");
  return{id:"e"+(e.Id||i),date:dIso(t.StartTime||e.StartTime||e.Date),kind:/test|písemk|písemn|prověrk|zkoušen|kompozic|slohov|čtvrtletk|diktát/i.test(txt)?"test":"akce",
   subj:(e.Subject&&e.Subject.Name)||"",title:e.Title||typ,desc:e.Description||""}}).filter(x=>x.date)}
function convert(r){
 const subs=(r.marks.Subjects||[]).map(s=>({name:s.Subject.Name,prev:null,
  marks:(s.Marks||[]).filter(m=>!m.IsPoints).map(m=>M(m.Id,m.MarkText,1,m.TypeNote||m.Caption||m.Theme||"",(m.MarkDate||"").slice(0,10),m.IsNew?1:0))}))
  .filter(s=>s.marks.some(m=>val(m.t)!=null));
 if(!subs.length)throw new Error("Žádné známky k zobrazení.");
 const ab=r.absence||{};let thr=ab.PercentageThreshold??0.3;if(thr<=1)thr*=100;
 const days=ab.Absences||[],sum=k=>days.reduce((x,d)=>x+(+d[k]||0),0);
 const abs=(ab.AbsencesPerSubject||[]).map(a=>({n:a.SubjectName,l:+a.LessonsCount||0,b:+a.Base||0}));
 return{thr,subs,un:days.filter(a=>a.Unsolved).length,abs,
  tot:{ok:sum("Ok"),miss:sum("Missed"),late:sum("Late"),soon:sum("Soon"),sch:sum("School")},
  raw:JSON.stringify(ab).slice(0,1500),
  tt:convTT(r.timetable),todo:convEV(r.events).concat(convHW(r.homeworks)),
  days:days.filter(d=>["Ok","Missed","Late","Soon","School"].some(k=>+d[k]>0)||d.Unsolved).map(d=>({date:dIso(d.Date),ok:+d.Ok||0,miss:+d.Missed||0,late:+d.Late||0,soon:+d.Soon||0,sch:+d.School||0,un:!!d.Unsolved})).sort((a,b)=>b.date.localeCompare(a.date))}}
function start(d){DATA=d;S.tab="over";S.open=null;S.hypo={};S.goal={};S.hw={};$("login").style.display="none";draw()}
$("go").onclick=async()=>{
 $("go").disabled=true;$("go").textContent="Přihlašuji…";$("msg").className="mu";$("msg").textContent="První načtení může trvat až minutu.";
 try{const r=await fetch("/",{method:"POST",body:JSON.stringify({base:$("base").value.trim(),user:$("user").value.trim(),pass:$("pass").value})});
  const d=await r.json();if(d.error)throw new Error(d.error);
  $("pass").value="";try{localStorage.setItem("login",JSON.stringify({base:$("base").value.trim(),user:$("user").value.trim()}))}catch(e){}$("msg").textContent="";start(convert(d))}
 catch(e){$("msg").className="er";$("msg").textContent=e.message;$("go").disabled=false;$("go").textContent="Zobrazit přehled"}};
try{const sv=JSON.parse(localStorage.getItem("login")||"{}");$("base").value=sv.base||"";$("user").value=sv.user||""}catch(e){}
$("eye").onclick=()=>{const q=$("pass");q.type=q.type=="password"?"text":"password";$("eye").textContent=q.type=="password"?"Zobrazit":"Skrýt"};
$("demo").onclick=()=>start(DEMO);
</script></body></html>
'''

if __name__ == "__main__":
    local = HOST == "127.0.0.1"
    if not local and not PIN:
        raise SystemExit("Server je dostupný z internetu. Nastav proměnnou prostředí APP_PIN (přístupové heslo).")
    print(f"Běží na http://127.0.0.1:{PORT}  (Ctrl+C ukončí)" if local else f"Běží na portu {PORT}")
    if local:
        webbrowser.open(f"http://127.0.0.1:{PORT}")
    HTTPServer((HOST, PORT), H).serve_forever()
