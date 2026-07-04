# -*- coding: utf-8 -*-
# video-cards.json から「弱点カード復習」動画(MP4)をカテゴリ別に生成する
#   スライド: Chrome headless スクショ / 音声: edge-tts(英+日) / 結合: ffmpeg
# 使い方: python build-video.py [slides|audio|all] [カテゴリ番号(1-5, 省略で全部)]
import os, re, sys, json, asyncio, subprocess, tempfile, html, pathlib
import edge_tts
from pydub import AudioSegment

BASE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.join(BASE, "video")
SLIDES = os.path.join(VID, "slides")
ACLIPS = os.path.join(VID, "audio")
CLIPS = os.path.join(VID, "clips")
for d in (VID, SLIDES, ACLIPS, CLIPS):
    os.makedirs(d, exist_ok=True)

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
EN_VOICE = "en-US-JennyNeural"
JA_VOICE = "ja-JP-NanamiNeural"
EN_RATE = "-6%"

with open(os.path.join(BASE, "video-cards.json"), encoding="utf-8") as f:
    C = json.load(f)

# ---- 差分ハイライト: wrong に無い語（＝直した箇所）を赤下線にする ----
def _norm(w): return re.sub(r"[^0-9a-zA-Z]", "", w).lower()
def diffwords(wrong, right):
    wset = set(_norm(w) for w in wrong.split() if _norm(w))
    return set(_norm(w) for w in right.split() if _norm(w) and _norm(w) not in wset)
def hl_words(text, dset):
    out = []
    for w in text.split():
        n = _norm(w)
        if n and n in dset:
            out.append(f'<span class="hl">{html.escape(w)}</span>')
        else:
            out.append(html.escape(w))
    return " ".join(out)

def title_html(g):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">{_css(g['color'])}</head><body>
    <div class="deco1"></div><div class="deco2"></div><div class="deco3" style="background:{g['color']}22"></div>
    <div class="title-wrap">
      <div class="cat-pill" style="background:{g['color']}">{html.escape(g['catEn'])}</div>
      <div class="big-title">{html.escape(g['cat'])}</div>
      <div class="sub">IELTS 弱点カード復習 ・ 全{len(g['slides'])}問</div>
    </div></body></html>"""

def card_html(g, s, idx, total):
    dset = diffwords(s['wrong'], s['right'])
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">{_css(g['color'])}</head><body>
    <div class="deco1"></div><div class="deco2"></div><div class="deco3" style="background:{g['color']}22"></div>
    <div class="brand">IELTS 弱点カード</div>
    <div class="head">
      <span class="cat-pill sm" style="background:{g['color']}">{html.escape(g['cat'])}</span>
      <span class="topic">{html.escape(s['topic'])}</span>
      <span class="count">{idx} / {total}</span>
    </div>
    <div class="wrap">
      <div class="fx-wrong">&#10060; {html.escape(s['wrong'])}</div>
      <div class="fx-right">&#9989; {hl_words(s['right'], dset)}</div>
      <div class="hero">&#128266; {hl_words(s['ex'], dset)}</div>
      <div class="ctx">&#128205; {html.escape(s['ctx'])}</div>
    </div>
    <div class="kaisetsu"><span class="k-label" style="color:{g['color']}">&#128161; 解説</span>{html.escape(s['why'])}</div>
    </body></html>"""

def _css(color):
    return f"""<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:1280px;height:720px;overflow:hidden;background:#fff;
  font-family:"Segoe UI","Yu Gothic","Meiryo",sans-serif;color:#141414;}}
.deco1,.deco2,.deco3{{position:absolute;background:#eef1f6;transform:rotate(-20deg);border-radius:6px;}}
.deco1{{width:520px;height:70px;top:-24px;right:-90px;}}
.deco2{{width:360px;height:34px;top:56px;right:60px;background:#f4f6fa;}}
.deco3{{width:150px;height:14px;top:32px;right:360px;}}
.brand{{position:absolute;top:20px;right:34px;color:#c9d2e0;font-size:15px;font-weight:600;}}
.head{{position:absolute;top:40px;left:80px;right:80px;display:flex;align-items:center;gap:16px;}}
.cat-pill{{color:#fff;font-weight:800;border-radius:999px;padding:6px 18px;font-size:20px;}}
.cat-pill.sm{{font-size:17px;padding:4px 14px;}}
.head .topic{{color:#5b6472;font-size:20px;font-weight:600;}}
.head .count{{margin-left:auto;color:#aab3c0;font-size:18px;font-weight:700;}}
.wrap{{position:absolute;top:92px;left:80px;right:80px;}}
.fx-wrong{{font-size:25px;font-weight:600;color:#9aa4b2;text-decoration:line-through;text-decoration-color:#d9a0a0;}}
.fx-right{{margin-top:6px;font-size:28px;font-weight:800;color:#3a4048;}}
.fx-right .hl{{color:#d81f1f;}}
.hero{{margin-top:26px;font-size:56px;font-weight:800;color:#111;line-height:1.2;}}
.hero .hl{{color:#d81f1f;text-decoration:underline;text-decoration-thickness:6px;text-underline-offset:8px;}}
.ctx{{margin-top:26px;font-size:28px;font-weight:800;color:#1731c8;line-height:1.4;}}
.kaisetsu{{position:absolute;top:520px;left:80px;right:80px;background:#f1f4f9;border-left:8px solid {color};
  border-radius:10px;padding:18px 24px;font-size:23px;line-height:1.5;color:#2a2a2a;}}
.kaisetsu .k-label{{font-weight:800;margin-right:10px;}}
.title-wrap{{position:absolute;top:0;left:0;width:1280px;height:720px;display:flex;flex-direction:column;
  align-items:center;justify-content:center;}}
.cat-pill{{margin-bottom:22px;}}
.big-title{{font-size:88px;font-weight:900;color:#141414;text-align:center;}}
.sub{{margin-top:22px;font-size:32px;color:#5b6472;font-weight:700;text-align:center;}}
</style>"""

def shoot(html_str, png_path):
    hp = os.path.join(VID, "_slide.html")
    with open(hp, "w", encoding="utf-8") as f:
        f.write(html_str)
    url = pathlib.Path(hp).as_uri()
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
        "--force-device-scale-factor=1", "--default-background-color=ffffffff",
        f"--screenshot={png_path}", "--window-size=1280,720", url],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def gkey(g): return g["file"]

def build_slides(groups):
    print("slides:")
    for g in groups:
        shoot(title_html(g), os.path.join(SLIDES, f"{gkey(g)}_00.png"))
        for i, s in enumerate(g["slides"], 1):
            shoot(card_html(g, s, i, len(g["slides"])), os.path.join(SLIDES, f"{gkey(g)}_{i:02d}.png"))
        print(f"  {g['cat']}: {len(g['slides'])+1} slides")

# ---------- audio ----------
_tmp = tempfile.mkdtemp(prefix="vid_tts_")
_n = [0]
async def tts(text, voice, rate="+0%"):
    _n[0]+=1
    p = os.path.join(_tmp, f"a{_n[0]}.mp3")
    await edge_tts.Communicate(text, voice, rate=rate).save(p)
    return AudioSegment.from_file(p, format="mp3")
def sil(ms): return AudioSegment.silent(duration=ms)

async def build_audio(groups):
    print("audio:")
    for g in groups:
        # title
        a = await tts(f"{g['catEn']}.", EN_VOICE, EN_RATE) + sil(300) + await tts(f"{g['cat']}の復習です。", JA_VOICE) + sil(700)
        a.export(os.path.join(ACLIPS, f"{gkey(g)}_00.mp3"), format="mp3", bitrate="128k")
        for i, s in enumerate(g["slides"], 1):
            en = await tts(s["ex"], EN_VOICE, EN_RATE)
            seg = en + sil(500) + en + sil(700) + await tts(s["why"], JA_VOICE) + sil(2500)
            seg.export(os.path.join(ACLIPS, f"{gkey(g)}_{i:02d}.mp3"), format="mp3", bitrate="128k")
        print(f"  {g['cat']}: audio done")

# ---------- assemble ----------
def make_clip(png, mp3, out):
    subprocess.run(["ffmpeg","-y","-loop","1","-framerate","30","-i",png,"-i",mp3,
        "-c:v","libx264","-tune","stillimage","-c:a","aac","-b:a","192k","-ar","44100",
        "-pix_fmt","yuv420p","-vf","scale=1280:720,format=yuv420p","-shortest",out],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def assemble(groups):
    print("assemble:")
    for g in groups:
        listf = os.path.join(VID, f"concat_{gkey(g)}.txt")
        with open(listf, "w", encoding="utf-8") as lf:
            for k in range(0, len(g["slides"])+1):
                png = os.path.join(SLIDES, f"{gkey(g)}_{k:02d}.png")
                mp3 = os.path.join(ACLIPS, f"{gkey(g)}_{k:02d}.mp3")
                out = os.path.join(CLIPS, f"{gkey(g)}_{k:02d}.mp4")
                make_clip(png, mp3, out)
                lf.write(f"file '{out.replace(chr(92),'/')}'\n")
        final = os.path.join(VID, f"IELTS_{gkey(g)}.mp4")
        subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",listf,"-c","copy",final],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"  -> IELTS_{gkey(g)}.mp4")

def main():
    mode = sys.argv[1] if len(sys.argv)>1 else "all"
    groups = C["groups"]
    if len(sys.argv)>2:
        idx = int(sys.argv[2]) - 1
        groups = [C["groups"][idx]]
    if mode in ("slides","all"): build_slides(groups)
    if mode in ("audio","all"): asyncio.run(build_audio(groups))
    if mode in ("assemble","all"): assemble(groups)

main()
