# IELTS Writing 弱点改善ノート（Kaito 専用）

自分の英作文5本から抽出した文法ミスを **①品詞 ②前置詞 ③冠詞 ④コロケーション** の4カテゴリに整理した学習教材。目標は **IELTS Band 6.5**。

## 📱 通勤用ウェブアプリ

**→ https://s1280061.github.io/eigo/**

スマホ最適化。ホーム画面に追加するとアプリのように使えます。

- **📇 カード** … ミスを1枚ずつ復習（❌→✅、タップで解説）／習得済みチェック
- **⚡ クイズ** … ❌を見て正しい英語を頭の中で言う → 答え合わせ（進捗は自動保存）
- **🎯 TOP5** … 特に苦手なポイント
- **📅 練習** … 1週間メニュー・優先順位・模範文

進捗はブラウザに保存されます（localStorage）。

## 📄 ファイル

| ファイル | 用途 |
|---|---|
| `index.html` + `data.js` | 通勤用ウェブアプリ本体 |
| `IELTS_弱点改善ノート.md` | ノート全文（Markdown） |
| `IELTS_弱点改善ノート.pdf` | 印刷用（A4・14ページ） |
| `build-pdf.js` | `data.js` から印刷HTMLを生成するスクリプト |

## 🔧 PDFの再生成

```bash
node build-pdf.js
# 生成された print.html を Chrome で印刷 → PDF
chrome --headless --print-to-pdf="IELTS_弱点改善ノート.pdf" --no-pdf-header-footer print.html
```

ミス項目や例文を増やすときは **`data.js` だけ編集** すれば、アプリ・PDF両方に反映されます。

---
目標: **Band 6.5** ／ まずは「主語↔動詞の一致」を制する。
