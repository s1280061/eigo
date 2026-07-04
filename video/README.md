# 🎬 解説動画: IELTS 弱点カード復習（カテゴリ別）

アプリの「カード」「クイズ」と同じ48項目を、送ってもらった画像のデザインで動画化したものです。
`data.js`（弱点カード）から自動生成しています。

## 出力（カテゴリ別に5本）
| ファイル | 内容 | 問題数 |
|---|---|---|
| `IELTS_1_WordForm.mp4` | 品詞 | 6 |
| `IELTS_2_Prepositions.mp4` | 前置詞 | 11 |
| `IELTS_3_Articles.mp4` | 冠詞 | 8 |
| `IELTS_4_Collocations.mp4` | コロケーション | 18 |
| `IELTS_5_SentenceStructure.mp4` | 文構造 | 5 |

## 1カードの画面（画像デザインを踏襲）
- 上部: カテゴリのタグ ＋ 場面（トピック）＋ 進捗
- **❌ 誤り**（グレーの取り消し線）
- **✅ 正しい**（大きな黒字。直した箇所を**赤下線**で自動ハイライト）
- **📍 場面**（青字の日本語）
- **💡 解説**ボックス（なぜ間違いか ＋ 📝 例文）

## 1カードの音声
1. 例文を英語で読み上げ（少しゆっくり）
2. 0.5秒あけてもう一度
3. 日本語で解説（なぜ間違いか）
4. 約2.5秒の間（画面を読む時間）

## 作り直し方
```bash
node build-video-content.js      # data.js → video-cards.json
python build-video.py slides     # スライドだけ（見た目調整）
python build-video.py audio      # 音声だけ（声・速度変更）
python build-video.py all        # 全部（5本のMP4を生成）
python build-video.py all 4      # カテゴリ4(コロケーション)だけ生成
```

- 声・速度: `build-video.py` 上部の `EN_VOICE` / `JA_VOICE` / `EN_RATE`
- 内容: `data.js` を編集すれば、アプリ・PDF・ノート・動画すべてに反映

## 素材フォルダ
- `slides/` スライドPNG ／ `audio/` 音声MP3 ／ `clips/` 結合前クリップ
