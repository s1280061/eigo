# 🎬 解説動画: ネイティブの音の変化 12選（English Reductions）

`video-content.json` から自動生成した解説動画です。各フレーズを **英文（音が変わる箇所に下線）→ 赤字で崩れた発音 → 日本語訳 → 💡解説** の順でスライド表示し、
**英語ナレーション（2回）＋日本語ナレーション**が付きます。

## 出力
- `English_Reductions_12.mp4` … 本編（1280×720 / タイトル＋12フレーズ）

## 収録フレーズ
Wouldja / wanna / gonna / gotta / didja / whatcha / lemme / gimme / doncha / kinda / outta / cuz

## 構成（1フレーズあたり）
1. 英文を読み上げ（少しゆっくり）
2. 0.5秒あけてもう一度
3. 日本語訳を読み上げ
4. 約3秒の間（画面の💡解説を読む時間）

## 作り直し方
```bash
python build-video.py slides   # スライド画像だけ再生成（見た目調整用）
python build-video.py audio    # 音声だけ再生成（声・速度変更用）
python build-video.py all      # 全部（スライド＋音声＋MP4結合）
```

- 声の変更は `build-video.py` 上部の `EN_VOICE` / `JA_VOICE` / `EN_RATE` を編集
  - 例: `EN_VOICE = "en-GB-SoniaNeural"`（英国発音）, `EN_RATE = "-10%"`（もっとゆっくり）
- フレーズの追加・修正は `video-content.json` を編集するだけ

## 素材
- `slides/` … 各スライドPNG
- `audio/` … 各スライドの音声MP3
- `clips/` … 各スライドの動画クリップ（結合前）
