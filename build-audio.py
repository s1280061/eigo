# -*- coding: utf-8 -*-
# audio_content.json から MP3 を生成する（edge-tts ニューラル音声 + pydub）
# 使い方: python build-audio.py [voice] [rate]
#   例: python build-audio.py en-GB-SoniaNeural -8%
import os, sys, json, asyncio, tempfile
import edge_tts
from pydub import AudioSegment

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "audio")
os.makedirs(OUT, exist_ok=True)

VOICE = sys.argv[1] if len(sys.argv) > 1 else "en-GB-SoniaNeural"
RATE  = sys.argv[2] if len(sys.argv) > 2 else "-8%"
ALBUM = "IELTS Listening Practice (Kaito)"
ARTIST = "IELTS Practice"

with open(os.path.join(BASE, "audio_content.json"), encoding="utf-8") as f:
    C = json.load(f)

tmp = tempfile.mkdtemp(prefix="ielts_tts_")
_counter = [0]

async def synth(text):
    """1つのテキストを合成して AudioSegment を返す"""
    _counter[0] += 1
    p = os.path.join(tmp, f"seg_{_counter[0]}.mp3")
    comm = edge_tts.Communicate(text, VOICE, rate=RATE)
    await comm.save(p)
    return AudioSegment.from_file(p, format="mp3")

def sil(ms):
    return AudioSegment.silent(duration=ms)

def export(seg, fname, title, track):
    out = os.path.join(OUT, fname)
    seg.export(out, format="mp3", bitrate="128k",
               tags={"title": title, "artist": ARTIST, "album": ALBUM, "track": str(track)})
    print(f"  -> {fname}  ({len(seg)/1000:.0f}s)")

async def build_model(m, track):
    # 導入（英語タイトル）→ 段落ごとに合成し、段落間に0.6秒の無音
    audio = await synth(m["enTitle"] + ".")
    audio += sil(800)
    for para in m["text"].split("\n\n"):
        para = para.strip()
        if not para:
            continue
        audio += await synth(para)
        audio += sil(600)
    slug = m["enTitle"].split(":")[0].replace(" ", "_").replace(",", "")
    fname = f"{track:02d}_Model_{slug}.mp3"
    export(audio, fname, f"Model: {m['enTitle']}", track)

async def build_sentences(group, track):
    # 導入 → 各例文を合成し、文間に1.3秒の無音（シャドーイング/リピート用）
    audio = await synth(f"Example sentences. {group['catEn']}.")
    audio += sil(1000)
    for s in group["sentences"]:
        audio += await synth(s["ex"])
        audio += sil(1300)
    slug = group["catEn"].replace(" ", "_")
    fname = f"{track:02d}_Sentences_{slug}.mp3"
    export(audio, fname, f"Sentences: {group['catEn']}", track)

async def main():
    print(f"voice={VOICE} rate={RATE}")
    track = 1
    print("Model answers:")
    for m in C["models"]:
        await build_model(m, track); track += 1
    print("Example sentences:")
    for g in C["sentenceGroups"]:
        await build_sentences(g, track); track += 1
    print("done. files in:", OUT)

asyncio.run(main())
