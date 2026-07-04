# 🎧 IELTS リスニング音声（YouTube Music 用）

`data.js` の模範解答と例文を、ニューラル音声（英国発音 en-GB-Sonia）で読み上げたMP3です。
アルバム名 **「IELTS Listening Practice (Kaito)」** でタグ付けしてあるので、YouTube Music で1つのアルバムとして並びます。

## 🎵 トラック一覧（全11曲）

| # | ファイル | 内容 | 長さ |
|---|---|---|---|
| 01 | Model_Email_to_a_friend | 手紙: 病気の友人へ（模範） | 64s |
| 02 | Model_Globalisation | Task2 グローバル化（模範） | 106s |
| 03 | Model_A_successful_multicultural_country | 多文化都市の成功例（模範） | 37s |
| 04 | Model_The_most_popular_festival_in_Japan | 祭り（模範） | 21s |
| 05 | Model_Facebook_users_by_age_group | Task1 円グラフ（模範） | 91s |
| 06 | Model_Application_letter | 手紙: 塾への応募（模範） | 38s |
| 07 | Sentences_Word_Form | 例文: 品詞 | 39s |
| 08 | Sentences_Prepositions | 例文: 前置詞 | 64s |
| 09 | Sentences_Articles | 例文: 冠詞 | 45s |
| 10 | Sentences_Collocations | 例文: コロケーション | 108s |
| 11 | Sentences_Sentence_Structure | 例文: 文構造 | 31s |

- **模範解答（01〜06）**: 段落の切れ目に短い無音。ディクテーションや音読の手本に。
- **例文（07〜11）**: 各文の後に約1.3秒の無音 → **聞いて、間で口に出して真似る（シャドーイング）** 用。

## 📲 YouTube Music への入れ方（自分の音源をアップロード）

1. パソコンのブラウザで **https://music.youtube.com** を開く（Googleにログイン）
2. 右上のプロフィールアイコン → **「音楽をアップロード」**
3. この `audio` フォルダの **MP3を全部選んでドラッグ＆ドロップ**
4. アップロード後、スマホの YouTube Music アプリ → **ライブラリ → アップロード** に表示され、通勤中に再生できます

> ※ アップロードした曲の再生は無料でOK（オフライン保存はYouTube Music Premiumが必要）。

## 🔧 声・速度を変えて作り直す

```bash
node build-audio-content.js          # data.js → audio_content.json
python build-audio.py [声] [速度]
```

例:
- 米国女性・ふつうの速さ: `python build-audio.py en-US-JennyNeural +0%`
- 米国男性・少しゆっくり: `python build-audio.py en-US-GuyNeural -10%`
- 英国男性: `python build-audio.py en-GB-RyanNeural -8%`

声の候補: `en-GB-SoniaNeural` / `en-GB-RyanNeural` / `en-GB-LibbyNeural` / `en-US-JennyNeural` / `en-US-GuyNeural` / `en-US-AriaNeural`
