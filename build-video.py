# -*- coding: utf-8 -*-
# video-content.json から解説動画(MP4)を生成する
#   スライド: Chrome headless スクショ / 音声: edge-tts(英+日) / 結合: ffmpeg
# 使い方: python build-video.py [slides|audio|all]
import os, sys, json, asyncio, subprocess, tempfile, html, pathlib
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

with open(os.path.join(BASE, "video-content.json"), encoding="utf-8") as f:
    C = json.load(f)

def slide_html(title=None, subtitle=None, s=None):
    if title is not None:
        body = f"""
        <div class="title-wrap">
          <div class="big-title">{html.escape(title)}</div>
          <div class="sub">{html.escape(subtitle or '')}</div>
        </div>"""
    else:
        en = html.escape(s["en"])
        u = html.escape(s["underline"])
        en_u = en.replace(u, f'<u>{u}</u>', 1)
        body = f"""
        <div class="brand">English Reductions</div>
        <div class="wrap">
          <div class="en">{en_u}</div>
          <div class="reduction">「{html.escape(s['underline'])}」 → <span class="red">({html.escape(s['reduction'])})</span></div>
          <div class="ja">{html.escape(s['ja'])}</div>
          <div class="kaisetsu"><span class="k-label">💡 解説</span>{html.escape(s['kaisetsu'])}</div>
        </div>"""
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:1280px;height:720px;overflow:hidden;background:#fff;
  font-family:"Segoe UI","Yu Gothic","Meiryo",sans-serif;color:#111;}}
.deco1,.deco2,.deco3{{position:absolute;background:#eef1f6;transform:rotate(-20deg);border-radius:6px;}}
.deco1{{width:520px;height:70px;top:-20px;right:-80px;}}
.deco2{{width:360px;height:34px;top:60px;right:60px;background:#f4f6fa;}}
.deco3{{width:140px;height:14px;top:34px;right:360px;background:#e3ecff;}}
.brand{{position:absolute;top:22px;right:34px;color:#c9d2e0;font-size:16px;font-weight:600;letter-spacing:.5px;}}
.wrap{{position:absolute;top:96px;left:80px;right:80px;}}
.en{{font-size:60px;font-weight:800;line-height:1.18;color:#141414;}}
.en u{{text-decoration:underline;text-decoration-thickness:6px;text-underline-offset:8px;}}
.reduction{{margin-top:18px;font-size:30px;font-weight:700;color:#333;}}
.reduction .red{{color:#d81f1f;}}
.ja{{position:absolute;top:398px;left:80px;right:80px;font-size:42px;font-weight:800;color:#1731c8;}}
.kaisetsu{{position:absolute;top:486px;left:80px;right:80px;background:#f1f4f9;border-left:8px solid #1731c8;
  border-radius:10px;padding:20px 26px;font-size:24px;line-height:1.5;color:#2a2a2a;font-weight:500;}}
.kaisetsu .k-label{{display:inline-block;color:#1731c8;font-weight:800;margin-right:10px;}}
.title-wrap{{position:absolute;top:0;left:0;width:1280px;height:720px;display:flex;flex-direction:column;
  align-items:center;justify-content:center;}}
.big-title{{font-size:76px;font-weight:900;color:#141414;text-align:center;}}
.sub{{margin-top:26px;font-size:34px;color:#1731c8;font-weight:700;text-align:center;}}
</style></head><body>
<div class="deco1"></div><div class="deco2"></div><div class="deco3"></div>
{body}
</body></html>"""

def shoot(html_str, png_path):
    hp = os.path.join(VID, "_slide.html")
    with open(hp, "w", encoding="utf-8") as f:
        f.write(html_str)
    url = pathlib.Path(hp).as_uri()
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
        "--force-device-scale-factor=1", "--default-background-color=ffffffff",
        f"--screenshot={png_path}", "--window-size=1280,720", url],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def build_slides():
    print("slides:")
    shoot(slide_html(title=C["title"], subtitle=C["subtitle"]), os.path.join(SLIDES, "slide_00.png"))
    print("  slide_00 (title)")
    for i, s in enumerate(C["slides"], 1):
        shoot(slide_html(s=s), os.path.join(SLIDES, f"slide_{i:02d}.png"))
        print(f"  slide_{i:02d}  {s['reduction']}")

# ---------- audio ----------
_tmp = tempfile.mkdtemp(prefix="vid_tts_")
_n = [0]
async def tts(text, voice, rate="+0%"):
    _n[0]+=1
    p = os.path.join(_tmp, f"a{_n[0]}.mp3")
    await edge_tts.Communicate(text, voice, rate=rate).save(p)
    return AudioSegment.from_file(p, format="mp3")
def sil(ms): return AudioSegment.silent(duration=ms)

async def build_audio():
    print("audio:")
    # title
    a = await tts("Native English reductions. Twelve common phrases.", EN_VOICE, EN_RATE)
    a += sil(400) + await tts("ネイティブがよく使う音の変化を、12フレーズで練習しましょう。", JA_VOICE)
    a += sil(800)
    a.export(os.path.join(ACLIPS, "slide_00.mp3"), format="mp3", bitrate="128k")
    print("  slide_00 (title)")
    for i, s in enumerate(C["slides"], 1):
        en = await tts(s["en"], EN_VOICE, EN_RATE)
        seg = en + sil(500) + en + sil(700) + await tts(s["ja"], JA_VOICE) + sil(3000)
        seg.export(os.path.join(ACLIPS, f"slide_{i:02d}.mp3"), format="mp3", bitrate="128k")
        print(f"  slide_{i:02d}  ({len(seg)/1000:.0f}s)")

# ---------- assemble ----------
def make_clip(png, mp3, out):
    subprocess.run(["ffmpeg","-y","-loop","1","-framerate","30","-i",png,"-i",mp3,
        "-c:v","libx264","-tune","stillimage","-c:a","aac","-b:a","192k","-ar","44100",
        "-pix_fmt","yuv420p","-vf","scale=1280:720,format=yuv420p","-shortest",out],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def assemble():
    print("clips:")
    n = len(C["slides"])
    order = [f"{i:02d}" for i in range(0, n+1)]
    listf = os.path.join(VID, "concat.txt")
    with open(listf, "w", encoding="utf-8") as lf:
        for k in order:
            png = os.path.join(SLIDES, f"slide_{k}.png")
            mp3 = os.path.join(ACLIPS, f"slide_{k}.mp3")
            out = os.path.join(CLIPS, f"clip_{k}.mp4")
            make_clip(png, mp3, out)
            lf.write(f"file '{out.replace(chr(92),'/')}'\n")
            print(f"  clip_{k}")
    final = os.path.join(VID, "English_Reductions_12.mp4")
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",listf,"-c","copy",final],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("DONE ->", final)

def main():
    mode = sys.argv[1] if len(sys.argv)>1 else "all"
    if mode in ("slides","all"): build_slides()
    if mode in ("audio","all"): asyncio.run(build_audio())
    if mode == "all": assemble()

main()
