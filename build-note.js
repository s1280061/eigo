// data.js から Markdownノート（IELTS_弱点改善ノート.md）を生成する（Node実行）
const fs = require('fs');
const path = require('path');
const dir = __dirname;
const window = {};
eval(fs.readFileSync(path.join(dir, 'data.js'), 'utf8'));
const D = window.IELTS_DATA;

const cats = ["品詞","前置詞","冠詞","コロケーション","文構造"];
const catDesc = {
  "品詞":"Word Form — 名詞を無理に動詞化しない。形容詞と名詞を使い分ける。",
  "前置詞":"Prepositions — 動詞・形容詞は前置詞ごとセットで覚える。",
  "冠詞":"Articles — 抽象名詞＝無冠詞 / 可算単数＝a / 特定・最上級＝the。",
  "コロケーション":"Collocations — 自然に結びつく語の組み合わせ。",
  "文構造":"Sentence Structure — 動詞・be動詞・語順の欠落を直す。"
};
const num = n => String(n);

let md = `# IELTS Writing 弱点改善ノート（Kaito 専用）

作成日: ${D.updated}
目標: **${D.goal}**
出典: あなたの英作文6本 ＋ 公式添削（自然な表現・番号解説）

> このノートは \`data.js\` から自動生成されています。ウェブアプリ・印刷PDFと内容は完全に同期しています。

---

## 目次
1. [全体講評](#1-全体講評)
2. [カテゴリ別 ミス一覧（全${D.mistakes.length}項目）](#2-カテゴリ別-ミス一覧全${D.mistakes.length}項目)
3. [模範解答（原文 → 自然な表現 → 改良版）](#3-模範解答原文--自然な表現--改良版)
4. [苦手ポイント TOP5](#4-苦手ポイント-top5)
5. [1週間 練習メニュー](#5-1週間-練習メニュー)
6. [Band 6.5 優先順位](#6-band-65-優先順位)

---

## 1. 全体講評

あなたのアイデア・構成はすでに **Band 7 級**。負けているのは **「文法の正確さ」だけ** です。
本ノートは、あなたの英作文6本と公式添削から抽出したミスを **①品詞 ②前置詞 ③冠詞 ④コロケーション ⑤文構造** の5カテゴリに整理しました。各ミスには「どんな場面か（状況）」「なぜ間違いか」「IELTSで使える例文」を付けています。まずは主語↔動詞の一致を制すること。

---

## 2. カテゴリ別 ミス一覧（全${D.mistakes.length}項目）

`;

cats.forEach(c=>{
  const items = D.mistakes.filter(m=>m.cat===c);
  md += `### ${c}（${items.length}項目）\n_${catDesc[c]}_\n\n`;
  items.forEach(m=>{
    md += `#### ${m.id}. ${m.topic}\n`;
    md += `📍 **状況**: ${m.ctx}\n\n`;
    md += `- ❌ **誤り**: ${m.wrong}\n`;
    md += `- ✅ **正しい**: **${m.right}**\n`;
    md += `- 💡 **なぜ**: ${m.why}\n`;
    md += `- 📝 **例文**: *${m.ex}*\n\n`;
  });
  md += `---\n\n`;
});

md += `## 3. 模範解答（原文 → 自然な表現 → 改良版）\n\n`;
D.essays.forEach(e=>{
  md += `### ${e.title}（${e.words||''}）\n`;
  md += `> 🖊 **設問**: ${e.prompt}\n\n`;
  md += `**① あなたの原文**\n\n> ${e.original}\n\n`;
  md += `**② 自然な表現**\n\n> ${e.natural}\n\n`;
  if(e.improved){ md += `**③ 改良版（Band 7+）**\n\n> ${e.improved}\n\n`; }
  md += `---\n\n`;
});

md += `## 4. 苦手ポイント TOP5\n\n`;
md += `| 順位 | 弱点 | 症状 | 対策 |\n|:---:|---|---|---|\n`;
D.top5.forEach(t=>{ md += `| **${t.rank}** | **${t.title}** | \`${t.symptom}\` | ${t.fix} |\n`; });
md += `\n---\n\n## 5. 1週間 練習メニュー\n\n`;
md += `1日30〜40分：①インプット10分 → ②書く15分 → ③自己添削10分\n\n`;
md += `| 曜日 | テーマ | やること |\n|:---:|---|---|\n`;
D.week.forEach(w=>{ md += `| **${w.day}** | ${w.theme} | ${w.task} |\n`; });
md += `\n---\n\n## 6. Band 6.5 優先順位\n\n`;
D.priority.forEach(p=>{
  md += `### ${p.tier}（${p.desc}）\n`;
  p.items.forEach(i=>{ md += `- ${i}\n`; });
  md += `\n`;
});
md += `---\n\n_このノートはMarkdownです。VS Codeの「Markdown PDF」拡張、または \`node build-pdf.js\` → Chrome印刷でPDF化できます。_\n`;

fs.writeFileSync(path.join(dir,'IELTS_弱点改善ノート.md'), md, 'utf8');
console.log('note.md generated:', D.mistakes.length, 'mistakes,', D.essays.length, 'essays');
