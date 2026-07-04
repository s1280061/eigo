// data.js を読み込み、印刷用 print.html を生成する（Node実行）
const fs = require('fs');
const path = require('path');
const dir = __dirname;
const window = {};
eval(fs.readFileSync(path.join(dir, 'data.js'), 'utf8'));
const D = window.IELTS_DATA;
const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

const cats = ["品詞","前置詞","冠詞","コロケーション"];
const catDesc = {
  "品詞":"Word Form — 名詞を無理に動詞化しない。形容詞と名詞を使い分ける。",
  "前置詞":"Prepositions — 動詞・形容詞は前置詞ごとセットで覚える。",
  "冠詞":"Articles — 抽象名詞＝無冠詞 / 可算単数＝a / 複数国名＝the。",
  "コロケーション":"Collocations — 自然に結びつく語の組み合わせ（have a conversation 等）。"
};

function mistakeBlock(m){
  return `<div class="m">
    <div class="mid">${esc(m.id)}</div>
    <div class="row"><span class="lab bad">❌ 誤り</span><span class="txt">${esc(m.wrong)}</span></div>
    <div class="row"><span class="lab good">✅ 正しい</span><span class="txt">${esc(m.right)}</span></div>
    <div class="why"><b>💡 なぜ:</b> ${esc(m.why)}</div>
    <div class="ex"><b>📝 例文:</b> <i>${esc(m.ex)}</i></div>
  </div>`;
}

const catSections = cats.map(c=>{
  const items = D.mistakes.filter(m=>m.cat===c).map(mistakeBlock).join('');
  return `<section class="cat"><h2>${esc(c)}</h2><p class="cdesc">${esc(catDesc[c])}</p>${items}</section>`;
}).join('');

const top5 = D.top5.map(t=>`<tr><td class="rank">${t.rank}</td><td><b>${esc(t.title)}</b><br><span class="sym">例: ${esc(t.symptom)}</span></td><td>${esc(t.fix)}</td></tr>`).join('');
const week = D.week.map(w=>`<tr><td class="day">${esc(w.day)}</td><td><b>${esc(w.theme)}</b></td><td>${esc(w.task)}</td></tr>`).join('');
const prio = D.priority.map(p=>`<div class="pr"><h3>${esc(p.tier)} <span class="pd">(${esc(p.desc)})</span></h3><ul>${p.items.map(i=>`<li>${esc(i)}</li>`).join('')}</ul></div>`).join('');
const essays = D.essays.map(e=>`<div class="es"><h3>${esc(e.title)}</h3><p>${esc(e.after)}</p></div>`).join('');

const html = `<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8">
<title>IELTS 弱点改善ノート</title>
<style>
@page { size: A4; margin: 16mm 14mm; }
* { box-sizing: border-box; }
body { font-family: "Yu Gothic","Meiryo","Segoe UI",sans-serif; color:#1a1a1a; font-size:10.5pt; line-height:1.6; margin:0; }
.cover { text-align:center; padding:40mm 0 20mm; }
.cover h1 { font-size:26pt; margin:0 0 6mm; color:#0b4f8a; }
.cover .sub { font-size:12pt; color:#555; }
.cover .goal { display:inline-block; margin-top:10mm; padding:4mm 8mm; background:#0b4f8a; color:#fff; border-radius:6px; font-size:14pt; font-weight:bold; }
h2 { color:#0b4f8a; border-bottom:2px solid #0b4f8a; padding-bottom:2mm; font-size:15pt; margin-top:8mm; }
h3 { font-size:11.5pt; margin:4mm 0 2mm; }
.cdesc { color:#555; font-style:italic; margin:0 0 4mm; font-size:9.5pt; }
.intro { background:#eef4fb; border-left:4px solid #0b4f8a; padding:4mm 6mm; border-radius:4px; }
.cat { break-inside:avoid; }
.m { border:1px solid #d8d8d8; border-radius:6px; padding:3mm 4mm; margin:3mm 0; break-inside:avoid; }
.mid { font-weight:bold; color:#0b4f8a; font-size:9pt; }
.row { display:flex; gap:3mm; margin:1mm 0; }
.lab { flex:0 0 20mm; font-weight:bold; font-size:9pt; }
.lab.bad { color:#c0392b; }
.lab.good { color:#1e8449; }
.txt { flex:1; }
.row .txt { font-family:"Consolas","Courier New",monospace; }
.why { font-size:9.5pt; margin-top:1.5mm; }
.ex { font-size:9.5pt; margin-top:1mm; color:#333; }
table { width:100%; border-collapse:collapse; margin:3mm 0; break-inside:avoid; }
th,td { border:1px solid #ccc; padding:2.5mm 3mm; text-align:left; vertical-align:top; font-size:9.5pt; }
th { background:#0b4f8a; color:#fff; }
.rank,.day { text-align:center; font-weight:bold; color:#0b4f8a; width:12mm; }
.sym { color:#777; font-size:8.5pt; }
.pr { break-inside:avoid; margin:3mm 0; }
.pr ul { margin:1mm 0 0; padding-left:6mm; }
.es { break-inside:avoid; background:#f7f9fc; border-radius:6px; padding:3mm 4mm; margin:3mm 0; }
.es p { margin:1mm 0 0; }
.pagebreak { break-before:page; }
footer { text-align:center; color:#999; font-size:8pt; margin-top:8mm; }
</style></head><body>

<div class="cover">
  <h1>IELTS Writing<br>弱点改善ノート</h1>
  <div class="sub">Kaito 専用 &nbsp;/&nbsp; 作成日 ${esc(D.updated)}</div>
  <div class="goal">目標: ${esc(D.goal)}</div>
</div>

<div class="pagebreak"></div>
<h2>はじめに</h2>
<div class="intro">
あなたのアイデア・構成はすでに Band 7 級。<b>負けているのは「文法の正確さ」だけ</b>です。<br>
本ノートは、あなたの英作文5本から抽出したミスを <b>①品詞 ②前置詞 ③冠詞 ④コロケーション</b> の4カテゴリに整理し、
各ミスに「なぜ間違いか」と「IELTSで使える例文」を付けたものです。まずは主語↔動詞の一致を制すること。
</div>

<h2>カテゴリ別 ミス一覧（全${D.mistakes.length}項目）</h2>
${catSections}

<div class="pagebreak"></div>
<h2>あなたが特に苦手なポイント TOP5</h2>
<table><tr><th>順位</th><th>弱点 / 症状</th><th>対策</th></tr>${top5}</table>

<h2>1週間 練習メニュー</h2>
<p style="font-size:9.5pt;color:#555;">1日30〜40分。「①インプット10分 → ②書く15分 → ③自己添削10分」。</p>
<table><tr><th>曜日</th><th>テーマ</th><th>やること</th></tr>${week}</table>

<h2>Band 6.5 達成のための優先順位</h2>
${prio}

<div class="pagebreak"></div>
<h2>修正済み 全文（After 模範）</h2>
${essays}

<footer>IELTS 弱点改善ノート — ${esc(D.updated)} — 通勤ウェブアプリ版も同梱</footer>
</body></html>`;

fs.writeFileSync(path.join(dir,'print.html'), html, 'utf8');
console.log('print.html generated:', D.mistakes.length, 'mistakes');
