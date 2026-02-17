#!/usr/bin/env python3
"""
Reaction.py - God Level Hacker-Style Bio with Admin Panel
Single file Flask application with full admin control
"""

import json
import os
import time
import hashlib
from functools import wraps
from flask import (
    Flask, render_template_string, request, redirect,
    url_for, session, flash
)

app = Flask(__name__)
app.secret_key = os.urandom(32).hex()

DATA_FILE = "data.json"

DEFAULT_DATA = {
    "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
    "visitor_count": 0,
    "maintenance_mode": False,
    "theme_color": "#00ff55",
    "profile": {
        "name": "DRAGON X AYUSH",
        "hero_title": "AYUSH X DRAGON OWNER",
        "subtitle": "Creative Developer & Tech Enthusiast",
        "image_url": "https://uploads.onecompiler.io/44dsza56z/44dsz8je5/IMG_20260216_144927_493.webp",
        "about": "I design All design-style websites with animations and modern UI effects|| Caution: My attitude is as bold as my dreams.."
    },
    "bio_text": (
        "WELCOME TO MY BIO\n\n"
        "MY NAME - RAJESH PALECHA\n"
        "MY WORK - GAME HACK DEVELOPER\n"
        "MY AGE - 16\n"
        "MY BIRTHDAY - 3 SEPTEMBER\n"
        "MY LOCATION - KHEJRALA JODHPUR RAJSTHAN\n"
        "MY BEST FRIEND - AYUSH SINGH\n"
        "MY RELIGION - HINDU\n"
        "RAJSTHANI BOY"
    ),
    "skills": ["HTML", "CSS", "JavaScript", "Java", "C++", "FF Mod Maker", "UI Design", "Animations", "Python"],
    "links": [
        {"label": "BEST FRIEND", "url": "https://t.me/thakurayu45", "style": "yt"},
        {"label": "TELEGRAM", "url": "https://t.me/ayushmodsyt", "style": "tg"},
        {"label": "FEEDBACK GROUP", "url": "https://t.me/+0-YDWZ49UjxmZDM1", "style": "ig"},
        {"label": "CONTACT DRAGON X AYUSH", "url": "https://t.me/dragon_x_ayush", "style": "ti"},
        {"label": "PANNEL KEY GENERAT", "url": "https://t.me/dragon_x_ayush", "style": "ta"}
    ],
    "music_url": "",
    "links_section_title": "NO ADDISON ONLY DARK"
}

login_attempts = {}


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
            for key in DEFAULT_DATA:
                if key not in saved:
                    saved[key] = DEFAULT_DATA[key]
            if "profile" in saved:
                for pk in DEFAULT_DATA["profile"]:
                    if pk not in saved["profile"]:
                        saved["profile"][pk] = DEFAULT_DATA["profile"][pk]
            return saved
        except Exception:
            pass
    save_data(DEFAULT_DATA)
    return DEFAULT_DATA.copy()


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def check_brute_force(ip):
    if ip in login_attempts:
        info = login_attempts[ip]
        if info.get("locked_until"):
            remaining = info["locked_until"] - time.time()
            if remaining > 0:
                return True, int(remaining)
            else:
                login_attempts[ip] = {"count": 0, "locked_until": None}
                return False, 0
    return False, 0


def record_failed_attempt(ip):
    if ip not in login_attempts:
        login_attempts[ip] = {"count": 0, "locked_until": None}
    login_attempts[ip]["count"] += 1
    if login_attempts[ip]["count"] >= 3:
        login_attempts[ip]["locked_until"] = time.time() + 300


def clear_attempts(ip):
    if ip in login_attempts:
        del login_attempts[ip]


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated


def build_frontend_html(data):
    tc = data.get("theme_color", "#00ff55")
    profile = data.get("profile", {})
    name = profile.get("name", "DRAGON X AYUSH")
    hero_title = profile.get("hero_title", "AYUSH X DRAGON OWNER")
    subtitle = profile.get("subtitle", "")
    image_url = profile.get("image_url", "")
    about = profile.get("about", "")
    bio_text = data.get("bio_text", "")
    skills = data.get("skills", [])
    links = data.get("links", [])
    links_title = data.get("links_section_title", "")
    music_url = data.get("music_url", "")
    visitor_count = data.get("visitor_count", 0)
    maintenance = data.get("maintenance_mode", False)

    bio_html = bio_text.replace("\n", "<br>")
    about_escaped = about.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    bio_escaped = bio_html

    skills_tags = ""
    for s in skills:
        skills_tags += '<div class="tag">' + s + '</div>'

    links_html = ""
    for lnk in links:
        links_html += '<a class="btn-link" target="_blank" href="' + lnk.get("url", "#") + '">' + lnk.get("label", "") + '</a>'

    music_section = ""
    if music_url:
        music_section = '''
<audio id="bgMusic" loop>
<source src="''' + music_url + '''" type="audio/mpeg">
</audio>
<button id="musicBtn" onclick="toggleMusicFn()">MUSIC</button>
<script>
function toggleMusicFn(){var m=document.getElementById("bgMusic");if(!m)return;if(m.paused)m.play();else m.pause();}
</script>'''

    if maintenance:
        return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>UNDER MAINTENANCE</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Orbitron',sans-serif;}
body{background:#000;display:flex;flex-direction:column;align-items:center;justify-content:center;height:100vh;overflow:hidden;}
canvas{position:fixed;top:0;left:0;width:100%;height:100%;z-index:-1;}
h1{color:#8b0000;font-size:48px;z-index:1;text-shadow:3px 2px darkred,-2px 1px cyan;animation:glitch 0.5s infinite;}
p{color:''' + tc + ''';font-size:18px;margin-top:20px;z-index:1;}
@keyframes glitch{0%{text-shadow:3px 2px darkred,-2px 1px cyan}50%{text-shadow:-2px 0 red,2px 0 cyan}100%{text-shadow:2px 0 red,-2px 0 cyan}}
</style>
</head>
<body>
<canvas id="matrix"></canvas>
<h1>UNDER MAINTENANCE</h1>
<p>System is being upgraded. Come back later.</p>
<script>
var c=document.getElementById("matrix");var x=c.getContext("2d");c.width=innerWidth;c.height=innerHeight;
var fs=16;var cols=Math.floor(c.width/fs);var drops=[];for(var i=0;i<cols;i++)drops[i]=1;
setInterval(function(){x.fillStyle="rgba(0,0,0,0.05)";x.fillRect(0,0,c.width,c.height);x.fillStyle="''' + tc + '''";x.font=fs+"px monospace";for(var i=0;i<drops.length;i++){var t="01"[Math.floor(Math.random()*2)];x.fillText(t,i*fs,drops[i]*fs);if(drops[i]*fs>c.height&&Math.random()>0.975)drops[i]=0;drops[i]++;}},35);
</script>
</body>
</html>'''

    return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>''' + name + '''</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Orbitron',sans-serif}
body{background:#000;color:#add8e6;overflow:hidden}
canvas{position:fixed;top:0;left:0;width:100%;height:100%;z-index:-1}

.hero-name{
font-size:60px;text-align:center;margin:20px 0;color:#8b0000;letter-spacing:6px;
text-shadow:0 0 20px #00008b, 0 0 40px #8b0000;
animation:glitch 1s infinite;
}

@keyframes glow{0%{box-shadow:0 0 11px ''' + tc + '''}50%{box-shadow:0 0 30px ''' + tc + '''}100%{box-shadow:0 0 10px ''' + tc + '''}}
@keyframes glitch{0%{text-shadow:3px 2px darkred,-2px 1px cyan}50%{text-shadow:-2px 0 red,2px 0 cyan}100%{text-shadow:2px 0 red,-2px 0 cyan}}
@keyframes bioGlow{0%{text-shadow:0 0 8px #8b0000}100%{text-shadow:0 0 25px #8b0000}}
@keyframes up{from{transform:translateY(20px);opacity:0}to{transform:none;opacity:1}}

@media(max-width:768px){.hero-name{font-size:36px;}}

#access{height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:15px;}
#access img{width:220px;height:220px;border-radius:50%;border:4px solid #ff1493;animation:glow 2s infinite;object-fit:cover;}
#access h1{font-size:43px;animation:glitch 0.5s infinite;letter-spacing:5px}
@media(max-width:768px){#access h1{font-size:24px;}}
#btn{padding:16px 50px;font-size:18px;border:2px solid ''' + tc + ''';background:#000;color:''' + tc + ''';border-radius:10px;cursor:pointer;box-shadow:0 0 10px ''' + tc + ''';transition:.3s}
#btn:hover{box-shadow:0 0 25px ''' + tc + ''';transform:scale(1.08)}

#barBox{width:300px;height:10px;border:2px solid #8b0000;margin-top:20px;box-shadow:0 0 15px #add8e6}
#bar{height:100%;width:0;background:linear-gradient(90deg, #ff1493, #ffb6c1, #ff1493);box-shadow:0 0 15px ''' + tc + '''}
#txt{margin-top:10px}

#main{display:none;overflow:auto;height:100vh}
.wrap{max-width:900px;margin:auto;padding:20px;animation:up 0.7s}
.title{font-size:32px;text-align:center;margin:20px 0;animation:glitch 1.5s infinite}
@media(max-width:768px){.title{font-size:20px;}}
.card{border:2px solid #add8e6;border-radius:12px;padding:20px;margin:20px 0;background:rgba(0,0,0,.8)}
.profile img{width:240px;height:240px;border-radius:50%;border:3px solid ''' + tc + ''';animation:glow 1s infinite;object-fit:cover;}
.tags{display:flex;flex-wrap:wrap;gap:10px}
.tag{border:1px solid ''' + tc + ''';padding:8px;border-radius:6px;font-size:13px;}
.bio-text{font-size:18px;line-height:1.8;color:#add8e6;animation:bioGlow 2s infinite alternate;}

.btn-link{display:block;width:280px;margin:10px auto;padding:14px;text-align:center;border-radius:10px;text-decoration:none;font-weight:600;border:3px solid #00008b;color:#6ec6ff;box-shadow:0 0 22px #1bcefa;transition:.3s;font-size:13px;font-family:'Orbitron';}
.btn-link:hover{box-shadow:0 0 40px #1bcefa;transform:scale(1.05);}

.visitor-badge{position:fixed;top:10px;right:10px;background:rgba(0,0,0,0.8);border:1px solid ''' + tc + ''';padding:8px 14px;border-radius:8px;font-size:11px;color:''' + tc + ''';z-index:999;}

#musicBtn{position:fixed;bottom:20px;right:20px;padding:12px 20px;background:#000;color:#00008b;border:2px solid ''' + tc + ''';border-radius:8px;cursor:pointer;box-shadow:0 0 10px ''' + tc + ''';z-index:100;font-family:'Orbitron';font-size:12px;}
</style>
</head>
<body>

<canvas id="matrix"></canvas>
<div class="visitor-badge">VISITORS: ''' + str(visitor_count) + '''</div>

<div id="access">
<img src="''' + image_url + '''" alt="Profile">
<h1>SYSTEM ACCESS</h1>
<button id="btn" onclick="go()">ENTER SYSTEM</button>
<div id="barBox"><div id="bar"></div></div>
<div id="txt">WAITING...</div>
</div>

<div id="main">
<div class="wrap">
<div class="hero-name">''' + name + '''</div>
<div class="title">''' + hero_title + '''</div>

<div class="card profile" style="text-align:center">
<img src="''' + image_url + '''" alt="Profile">
<h2>WELCOME TO ''' + name + ''' BIO</h2>
<p>''' + subtitle + '''</p>
</div>

<div class="card">
<h3>ABOUT ME</h3>
<p>''' + about_escaped + '''</p>
</div>

<div class="card">
<h3>MY BIO</h3>
<p class="bio-text">''' + bio_escaped + '''</p>
</div>

<div class="card">
<h3>SKILLS</h3>
<div class="tags">''' + skills_tags + '''</div>
</div>

<div class="card" style="text-align:center">
<h3>''' + links_title + '''</h3>
''' + links_html + '''
</div>

</div>
</div>

''' + music_section + '''

<script>
function go(){
var m=document.getElementById("bgMusic");
if(m)try{m.play();}catch(e){}
var p=0,bar=document.getElementById("bar"),t=document.getElementById("txt");
var iv=setInterval(function(){
p+=4;bar.style.width=p+"%";t.innerText="LOADING SYSTEM... "+p+"%";
if(p>=100){clearInterval(iv);
document.body.style.background="rgba(0,255,85,1)";
setTimeout(function(){document.body.style.background="#000";
document.getElementById("access").style.display="none";
document.getElementById("main").style.display="block";},200);}
},100);
}
var c=document.getElementById("matrix");
var x=c.getContext("2d");c.width=innerWidth;c.height=innerHeight;
var letters="0101110100101010HACKEDBYYOU010101";
var fs=16;var cols=Math.floor(c.width/fs);var drops=[];
for(var i=0;i<cols;i++)drops[i]=1;
setInterval(function(){x.fillStyle="rgba(0,0,0,0.05)";x.fillRect(0,0,c.width,c.height);
x.fillStyle="''' + tc + '''";x.font=fs+"px monospace";
for(var i=0;i<drops.length;i++){var t=letters[Math.floor(Math.random()*letters.length)];
x.fillText(t,i*fs,drops[i]*fs);if(drops[i]*fs>c.height&&Math.random()>0.975)drops[i]=0;drops[i]++;}},35);
window.addEventListener("resize",function(){c.width=innerWidth;c.height=innerHeight;});
</script>

</body>
</html>'''


def build_login_html(data, locked, remaining):
    tc = data.get("theme_color", "#00ff55")
    flash_msgs = ""
    for cat, msg in session.get("_flashes", []):
        css_class = "success" if cat == "success" else "error"
        flash_msgs += '<div class="flash ' + css_class + '">' + msg + '</div>'

    locked_html = ""
    if locked:
        locked_html = '<div class="locked">LOCKED FOR ' + str(remaining) + ' SECONDS</div>'

    form_html = ""
    if not locked:
        form_html = '''<form method="POST">
<input type="password" name="password" placeholder="ENTER PASSWORD" required autocomplete="off">
<button type="submit">ACCESS SYSTEM</button>
</form>'''

    return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ADMIN ACCESS</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Orbitron',sans-serif;}
body{background:#000;display:flex;align-items:center;justify-content:center;height:100vh;overflow:hidden;}
canvas{position:fixed;top:0;left:0;width:100%;height:100%;z-index:-1;}
.login-box{background:rgba(0,0,0,0.9);border:2px solid ''' + tc + ''';border-radius:16px;padding:40px;width:400px;max-width:90vw;text-align:center;box-shadow:0 0 30px ''' + tc + ''';z-index:1;}
.login-box h1{color:''' + tc + ''';font-size:24px;margin-bottom:8px;text-shadow:0 0 15px ''' + tc + ''';}
.login-box h2{color:#8b0000;font-size:14px;margin-bottom:30px;}
.login-box input{width:100%;padding:14px;margin:10px 0;background:#111;border:2px solid #333;border-radius:8px;color:''' + tc + ''';font-family:'Orbitron';font-size:14px;text-align:center;outline:none;}
.login-box input:focus{border-color:''' + tc + ''';box-shadow:0 0 15px ''' + tc + ''';}
.login-box button{width:100%;padding:14px;margin-top:16px;background:transparent;border:2px solid ''' + tc + ''';color:''' + tc + ''';font-family:'Orbitron';font-size:16px;border-radius:8px;cursor:pointer;box-shadow:0 0 10px ''' + tc + ''';}
.login-box button:hover{background:''' + tc + ''';color:#000;}
.flash{padding:12px;border-radius:8px;margin:10px 0;font-size:12px;}
.flash.error{background:rgba(139,0,0,0.3);border:1px solid #8b0000;color:#ff6b6b;}
.flash.success{background:rgba(0,255,85,0.1);border:1px solid ''' + tc + ''';color:''' + tc + ''';}
.locked{color:#ff1493;font-size:12px;margin:10px 0;}
</style>
</head>
<body>
<canvas id="matrix"></canvas>
<div class="login-box">
<h1>ADMIN ACCESS</h1>
<h2>AUTHORIZED PERSONNEL ONLY</h2>
''' + locked_html + '''
''' + form_html + '''
</div>
<script>
var c=document.getElementById("matrix");var x=c.getContext("2d");c.width=innerWidth;c.height=innerHeight;
var fs=16;var cols=Math.floor(c.width/fs);var drops=[];for(var i=0;i<cols;i++)drops[i]=1;
setInterval(function(){x.fillStyle="rgba(0,0,0,0.05)";x.fillRect(0,0,c.width,c.height);
x.fillStyle="''' + tc + '''";x.font=fs+"px monospace";
for(var i=0;i<drops.length;i++){var t="01"[Math.floor(Math.random()*2)];
x.fillText(t,i*fs,drops[i]*fs);if(drops[i]*fs>c.height&&Math.random()>0.975)drops[i]=0;drops[i]++;}},35);
</script>
</body>
</html>'''


# ============================================================
# ADMIN DASHBOARD - Using Jinja2 safely
# ============================================================

ADMIN_DASHBOARD_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ADMIN PANEL</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Orbitron',sans-serif;}
body{background:#0a0a0a;color:#add8e6;min-height:100vh;}
.topbar{background:#000;border-bottom:2px solid {{tc}};padding:15px 25px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;box-shadow:0 0 20px {{tc}};}
.topbar h1{color:{{tc}};font-size:20px;text-shadow:0 0 10px {{tc}};}
.topbar-right{display:flex;gap:10px;align-items:center;flex-wrap:wrap;}
.topbar a{padding:8px 18px;border:1px solid {{tc}};background:transparent;color:{{tc}};border-radius:6px;text-decoration:none;font-family:'Orbitron';font-size:11px;cursor:pointer;transition:.3s;}
.topbar a:hover{background:{{tc}};color:#000;}
.container{max-width:1000px;margin:20px auto;padding:0 15px;}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:15px;margin-bottom:25px;}
.stat-card{background:#111;border:1px solid #333;border-radius:12px;padding:20px;text-align:center;transition:.3s;}
.stat-card:hover{border-color:{{tc}};box-shadow:0 0 15px {{tc}};}
.stat-card h3{color:#888;font-size:11px;margin-bottom:8px;}
.stat-card .value{color:{{tc}};font-size:28px;text-shadow:0 0 10px {{tc}};}
.tabs{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:20px;border-bottom:2px solid #222;padding-bottom:10px;}
.tab{padding:10px 20px;background:#111;border:1px solid #333;border-radius:8px 8px 0 0;cursor:pointer;color:#888;font-size:11px;transition:.3s;font-family:'Orbitron';}
.tab:hover,.tab.active{color:{{tc}};border-color:{{tc}};background:#1a1a1a;}
.panel{display:none;}
.panel.active{display:block;}
.card{background:#111;border:1px solid #333;border-radius:12px;padding:25px;margin-bottom:20px;}
.card h2{color:{{tc}};font-size:16px;margin-bottom:20px;padding-bottom:10px;border-bottom:1px solid #333;text-shadow:0 0 8px {{tc}};}
label{display:block;color:#aaa;font-size:11px;margin-bottom:6px;margin-top:14px;}
input[type="text"],input[type="password"],input[type="url"],input[type="color"],textarea{
width:100%;padding:12px;background:#0a0a0a;border:2px solid #333;border-radius:8px;
color:{{tc}};font-family:'Orbitron';font-size:13px;outline:none;transition:.3s;}
input:focus,textarea:focus{border-color:{{tc}};box-shadow:0 0 10px {{tc}};}
textarea{resize:vertical;min-height:120px;line-height:1.6;}
input[type="color"]{height:50px;cursor:pointer;padding:5px;}
.btn{padding:12px 30px;border:2px solid {{tc}};background:transparent;color:{{tc}};
border-radius:8px;cursor:pointer;font-family:'Orbitron';font-size:13px;transition:.3s;margin-top:16px;}
.btn:hover{background:{{tc}};color:#000;box-shadow:0 0 20px {{tc}};}
.btn-danger{border-color:#8b0000;color:#ff6b6b;}
.btn-danger:hover{background:#8b0000;color:#fff;box-shadow:0 0 20px #8b0000;}
.btn-sm{padding:8px 16px;font-size:11px;margin:4px;}
.link-item{background:#0a0a0a;border:1px solid #333;border-radius:8px;padding:15px;margin:10px 0;display:flex;flex-wrap:wrap;align-items:center;gap:10px;}
.link-item input{flex:1;min-width:150px;}
.skill-tags{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0;}
.skill-tag{background:#1a1a1a;border:1px solid {{tc}};padding:8px 14px;border-radius:20px;display:flex;align-items:center;gap:8px;font-size:11px;}
.skill-tag button{background:none;border:none;color:#ff6b6b;cursor:pointer;font-size:14px;font-family:'Orbitron';}
.flash{padding:12px 20px;border-radius:8px;margin-bottom:15px;font-size:12px;}
.flash-success{background:rgba(0,255,85,0.1);border:1px solid {{tc}};color:{{tc}};}
.flash-error{background:rgba(139,0,0,0.2);border:1px solid #8b0000;color:#ff6b6b;}
@media(max-width:600px){.topbar{padding:10px;}.topbar h1{font-size:14px;}.card{padding:15px;}.stats{grid-template-columns:1fr 1fr;}}
</style>
</head>
<body>

<div class="topbar">
<h1>ADMIN PANEL - GOD MODE</h1>
<div class="topbar-right">
<a href="/" target="_blank">VIEW SITE</a>
<a href="/admin/logout">LOGOUT</a>
</div>
</div>

<div class="container">

{% for category, message in get_flashed_messages(with_categories=true) %}
<div class="flash flash-{{ category }}">{{ message }}</div>
{% endfor %}

<div class="stats">
<div class="stat-card"><h3>TOTAL VISITORS</h3><div class="value">{{ d.visitor_count }}</div></div>
<div class="stat-card"><h3>TOTAL LINKS</h3><div class="value">{{ d.links|length }}</div></div>
<div class="stat-card"><h3>TOTAL SKILLS</h3><div class="value">{{ d.skills|length }}</div></div>
<div class="stat-card"><h3>STATUS</h3><div class="value" style="font-size:14px;">{% if d.maintenance_mode %}MAINTENANCE{% else %}LIVE{% endif %}</div></div>
</div>

<div class="tabs">
<div class="tab active" onclick="showTab('profile',this)">PROFILE</div>
<div class="tab" onclick="showTab('bio',this)">BIO</div>
<div class="tab" onclick="showTab('skills',this)">SKILLS</div>
<div class="tab" onclick="showTab('links',this)">LINKS</div>
<div class="tab" onclick="showTab('theme',this)">THEME</div>
<div class="tab" onclick="showTab('settings',this)">SETTINGS</div>
</div>

<div class="panel active" id="tab-profile">
<div class="card">
<h2>EDIT PROFILE</h2>
<form method="POST" action="/admin/update/profile">
<label>DISPLAY NAME</label>
<input type="text" name="name" value="{{ d.profile.name }}" required>
<label>HERO TITLE</label>
<input type="text" name="hero_title" value="{{ d.profile.hero_title }}" required>
<label>SUBTITLE</label>
<input type="text" name="subtitle" value="{{ d.profile.subtitle }}">
<label>PROFILE IMAGE URL</label>
<input type="url" name="image_url" value="{{ d.profile.image_url }}" required>
<label>ABOUT ME</label>
<textarea name="about">{{ d.profile.about }}</textarea>
<button type="submit" class="btn">SAVE PROFILE</button>
</form>
</div>
</div>

<div class="panel" id="tab-bio">
<div class="card">
<h2>EDIT BIO TEXT</h2>
<form method="POST" action="/admin/update/bio">
<label>BIO CONTENT</label>
<textarea name="bio_text" rows="15">{{ d.bio_text }}</textarea>
<button type="submit" class="btn">SAVE BIO</button>
</form>
</div>
</div>

<div class="panel" id="tab-skills">
<div class="card">
<h2>MANAGE SKILLS</h2>
<div class="skill-tags">
{% for skill in d.skills %}
<div class="skill-tag">
{{ skill }}
<form method="POST" action="/admin/delete/skill" style="display:inline;">
<input type="hidden" name="skill" value="{{ skill }}">
<button type="submit">X</button>
</form>
</div>
{% endfor %}
</div>
<form method="POST" action="/admin/add/skill" style="display:flex;gap:10px;margin-top:16px;flex-wrap:wrap;">
<input type="text" name="skill" placeholder="NEW SKILL NAME" required style="flex:1;min-width:200px;">
<button type="submit" class="btn" style="margin-top:0;">ADD SKILL</button>
</form>
</div>
</div>

<div class="panel" id="tab-links">
<div class="card">
<h2>LINKS SECTION TITLE</h2>
<form method="POST" action="/admin/update/links_title">
<div style="display:flex;gap:10px;flex-wrap:wrap;">
<input type="text" name="links_title" value="{{ d.links_section_title }}" style="flex:1;min-width:200px;">
<button type="submit" class="btn" style="margin-top:0;">SAVE</button>
</div>
</form>
</div>
<div class="card">
<h2>EXISTING LINKS</h2>
{% for link in d.links %}
<div class="link-item">
<form method="POST" action="/admin/update/link" style="display:flex;flex-wrap:wrap;gap:10px;width:100%;align-items:center;">
<input type="hidden" name="index" value="{{ loop.index0 }}">
<input type="text" name="label" value="{{ link.label }}" placeholder="Label">
<input type="url" name="url" value="{{ link.url }}" placeholder="URL">
<button type="submit" class="btn btn-sm" style="margin-top:0;">SAVE</button>
</form>
<form method="POST" action="/admin/delete/link" style="display:inline;">
<input type="hidden" name="index" value="{{ loop.index0 }}">
<button type="submit" class="btn btn-sm btn-danger" style="margin-top:0;">DEL</button>
</form>
</div>
{% endfor %}
</div>
<div class="card">
<h2>ADD NEW LINK</h2>
<form method="POST" action="/admin/add/link">
<label>LINK LABEL</label>
<input type="text" name="label" placeholder="e.g. MY CHANNEL" required>
<label>LINK URL</label>
<input type="url" name="url" placeholder="https://..." required>
<button type="submit" class="btn">ADD LINK</button>
</form>
</div>
</div>

<div class="panel" id="tab-theme">
<div class="card">
<h2>THEME AND MEDIA</h2>
<form method="POST" action="/admin/update/theme">
<label>NEON ACCENT COLOR</label>
<input type="color" name="theme_color" value="{{ d.theme_color }}">
<label>BACKGROUND MUSIC URL (direct .mp3 link, leave empty to disable)</label>
<input type="url" name="music_url" value="{{ d.music_url }}" placeholder="https://example.com/music.mp3">
<button type="submit" class="btn">SAVE THEME</button>
</form>
</div>
</div>

<div class="panel" id="tab-settings">
<div class="card">
<h2>CHANGE PASSWORD</h2>
<form method="POST" action="/admin/change-password">
<label>CURRENT PASSWORD</label>
<input type="password" name="current_password" required>
<label>NEW PASSWORD</label>
<input type="password" name="new_password" required>
<label>CONFIRM NEW PASSWORD</label>
<input type="password" name="confirm_password" required>
<button type="submit" class="btn">UPDATE PASSWORD</button>
</form>
</div>
<div class="card">
<h2>MAINTENANCE MODE</h2>
<p style="font-size:12px;color:#888;margin-bottom:15px;">When enabled, visitors see an Under Maintenance page.</p>
<form method="POST" action="/admin/toggle/maintenance">
<p style="font-size:14px;margin-bottom:10px;">Currently: {% if d.maintenance_mode %}ENABLED{% else %}DISABLED{% endif %}</p>
<button type="submit" class="btn">{% if d.maintenance_mode %}DISABLE MAINTENANCE{% else %}ENABLE MAINTENANCE{% endif %}</button>
</form>
</div>
<div class="card">
<h2>RESET VISITOR COUNT</h2>
<form method="POST" action="/admin/reset/visitors">
<p style="font-size:12px;color:#888;">Current count: {{ d.visitor_count }}</p>
<button type="submit" class="btn btn-danger">RESET TO ZERO</button>
</form>
</div>
</div>

</div>

<script>
function showTab(name,el){
document.querySelectorAll('.panel').forEach(function(p){p.classList.remove('active');});
document.querySelectorAll('.tab').forEach(function(t){t.classList.remove('active');});
document.getElementById('tab-'+name).classList.add('active');
el.classList.add('active');
}
</script>
</body>
</html>'''


# ============================================================
# ROUTES
# ============================================================

@app.route("/")
def index():
    data = load_data()
    data["visitor_count"] += 1
    save_data(data)
    return build_frontend_html(data)


@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    data = load_data()
    ip = request.remote_addr
    locked, remaining = check_brute_force(ip)

    if request.method == "POST":
        if locked:
            flash("Account locked. Try again later.", "error")
            return build_login_html(data, True, remaining)

        password = request.form.get("password", "")
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        if password_hash == data["password_hash"]:
            session["admin_logged_in"] = True
            clear_attempts(ip)
            flash("Access granted! Welcome, Admin.", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            record_failed_attempt(ip)
            locked, remaining = check_brute_force(ip)
            if locked:
                flash("Too many failed attempts! Locked for " + str(remaining) + " seconds.", "error")
            else:
                attempts_left = 3 - login_attempts.get(ip, {}).get("count", 0)
                flash("Wrong password! " + str(attempts_left) + " attempts remaining.", "error")

    return build_login_html(data, locked, remaining)


@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    data = load_data()
    tc = data.get("theme_color", "#00ff55")
    return render_template_string(ADMIN_DASHBOARD_HTML, d=data, tc=tc)


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_login"))


@app.route("/admin/update/profile", methods=["POST"])
@login_required
def update_profile():
    data = load_data()
    data["profile"]["name"] = request.form.get("name", data["profile"]["name"])
    data["profile"]["hero_title"] = request.form.get("hero_title", data["profile"]["hero_title"])
    data["profile"]["subtitle"] = request.form.get("subtitle", data["profile"]["subtitle"])
    data["profile"]["image_url"] = request.form.get("image_url", data["profile"]["image_url"])
    data["profile"]["about"] = request.form.get("about", data["profile"]["about"])
    save_data(data)
    flash("Profile updated successfully!", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/update/bio", methods=["POST"])
@login_required
def update_bio():
    data = load_data()
    data["bio_text"] = request.form.get("bio_text", data["bio_text"])
    save_data(data)
    flash("Bio updated successfully!", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/add/skill", methods=["POST"])
@login_required
def add_skill():
    data = load_data()
    skill = request.form.get("skill", "").strip()
    if skill and skill not in data["skills"]:
        data["skills"].append(skill)
        save_data(data)
        flash("Skill added!", "success")
    else:
        flash("Skill already exists or empty.", "error")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/delete/skill", methods=["POST"])
@login_required
def delete_skill():
    data = load_data()
    skill = request.form.get("skill", "")
    if skill in data["skills"]:
        data["skills"].remove(skill)
        save_data(data)
        flash("Skill removed!", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/add/link", methods=["POST"])
@login_required
def add_link():
    data = load_data()
    label = request.form.get("label", "").strip()
    url_val = request.form.get("url", "").strip()
    if label and url_val:
        data["links"].append({"label": label, "url": url_val, "style": "tg"})
        save_data(data)
        flash("Link added!", "success")
    else:
        flash("Label and URL are required.", "error")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/update/link", methods=["POST"])
@login_required
def update_link():
    data = load_data()
    try:
        idx = int(request.form.get("index", -1))
        if 0 <= idx < len(data["links"]):
            data["links"][idx]["label"] = request.form.get("label", data["links"][idx]["label"])
            data["links"][idx]["url"] = request.form.get("url", data["links"][idx]["url"])
            save_data(data)
            flash("Link updated!", "success")
    except (ValueError, IndexError):
        flash("Invalid link index.", "error")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/delete/link", methods=["POST"])
@login_required
def delete_link():
    data = load_data()
    try:
        idx = int(request.form.get("index", -1))
        if 0 <= idx < len(data["links"]):
            removed = data["links"].pop(idx)
            save_data(data)
            flash("Link deleted!", "success")
    except (ValueError, IndexError):
        flash("Invalid link index.", "error")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/update/links_title", methods=["POST"])
@login_required
def update_links_title():
    data = load_data()
    data["links_section_title"] = request.form.get("links_title", data["links_section_title"])
    save_data(data)
    flash("Links section title updated!", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/update/theme", methods=["POST"])
@login_required
def update_theme():
    data = load_data()
    data["theme_color"] = request.form.get("theme_color", data["theme_color"])
    data["music_url"] = request.form.get("music_url", "").strip()
    save_data(data)
    flash("Theme and Music updated!", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/toggle/maintenance", methods=["POST"])
@login_required
def toggle_maintenance():
    data = load_data()
    data["maintenance_mode"] = not data["maintenance_mode"]
    save_data(data)
    status = "ENABLED" if data["maintenance_mode"] else "DISABLED"
    flash("Maintenance mode " + status + "!", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/change-password", methods=["POST"])
@login_required
def change_password():
    data = load_data()
    current = request.form.get("current_password", "")
    new_pass = request.form.get("new_password", "")
    confirm = request.form.get("confirm_password", "")

    current_hash = hashlib.sha256(current.encode()).hexdigest()

    if current_hash != data["password_hash"]:
        flash("Current password is incorrect!", "error")
    elif len(new_pass) < 4:
        flash("New password must be at least 4 characters!", "error")
    elif new_pass != confirm:
        flash("New passwords do not match!", "error")
    else:
        data["password_hash"] = hashlib.sha256(new_pass.encode()).hexdigest()
        save_data(data)
        flash("Password changed successfully!", "success")

    return redirect(url_for("admin_dashboard"))


@app.route("/admin/reset/visitors", methods=["POST"])
@login_required
def reset_visitors():
    data = load_data()
    data["visitor_count"] = 0
    save_data(data)
    flash("Visitor count reset to 0!", "success")
    return redirect(url_for("admin_dashboard"))


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
