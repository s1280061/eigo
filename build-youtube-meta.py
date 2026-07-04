# -*- coding: utf-8 -*-
# 各カテゴリ動画の YouTube 用メタデータ（タイトル/説明/タグ）を生成する
#   チャプターのタイムスタンプは video/audio の各MP3の長さから実測
import os, json
from pydub import AudioSegment

BASE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.join(BASE, "video")
ACLIPS = os.path.join(VID, "audio")
OUT = os.path.join(VID, "youtube")
os.makedirs(OUT, exist_ok=True)
APP = "https://s1280061.github.io/eigo/"

with open(os.path.join(BASE, "video-cards.json"), encoding="utf-8") as f:
    C = json.load(f)

titles = {
    "1_WordForm":        "【IELTS英作文】品詞ミス6選｜do communication はNG？音声つきで復習",
    "2_Prepositions":    "【IELTS英作文】前置詞ミス11選｜inform of / at risk / adapt to を直す",
    "3_Articles":        "【IELTS英作文】冠詞ミス8選｜a / the / 無冠詞の使い分け",
    "4_Collocations":    "【IELTS英作文】自然な英語コロケーション18選｜言い換えで得点UP",
    "5_SentenceStructure":"【IELTS英作文】文構造ミス5選｜be動詞・語順の抜けを直す",
}

def mmss(ms):
    s = int(ms/1000); return f"{s//60}:{s%60:02d}"

def dur(path):
    return len(AudioSegment.from_file(path, format="mp3"))

for g in C["groups"]:
    fk = g["file"]
    # 各クリップ長 = 各MP3長（-shortest で結合しているため）
    t = 0
    lines = []
    # 00 = タイトル
    lines.append(f"0:00 イントロ（{g['cat']}）")
    t += dur(os.path.join(ACLIPS, f"{fk}_00.mp3"))
    for i, s in enumerate(g["slides"], 1):
        lines.append(f"{mmss(t)} ✅ {s['right']}")
        t += dur(os.path.join(ACLIPS, f"{fk}_{i:02d}.mp3"))
    chapters = "\n".join(lines)
    total = mmss(t)

    desc = f"""IELTS Writing でやりがちな【{g['cat']}（{g['catEn']}）】のミスを、❌誤り → ✅正しい → 💡解説 の順に、英語音声つきでまとめました（全{len(g['slides'])}問／{total}）。通勤・スキマ時間の復習にどうぞ。

各カードは「読み上げる例文」を大きく表示し、直した箇所を赤下線でハイライトしています。

▼ チャプター
{chapters}

▼ 復習アプリ（無料・スマホ対応）
カード / クイズ / 模範解答が使えます:
{APP}

#IELTS #英語学習 #英作文 #IELTSWriting #English #英語 #ライティング #TOEIC #英文法"""

    tags = "IELTS, IELTS Writing, 英語学習, 英作文, 英文法, English learning, grammar, 前置詞, 冠詞, コロケーション, 品詞, 英語 やり直し, 社会人 英語"

    body = f"=== TITLE ===\n{titles[fk]}\n\n=== DESCRIPTION ===\n{desc}\n\n=== TAGS ===\n{tags}\n\n=== FILE ===\nvideo/IELTS_{fk}.mp4\n"
    with open(os.path.join(OUT, f"{fk}.txt"), "w", encoding="utf-8") as f:
        f.write(body)
    print(f"{fk}: {len(g['slides'])} cards, total {total} -> youtube/{fk}.txt")

print("done ->", OUT)
