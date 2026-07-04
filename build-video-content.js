// data.js から動画用データ(video-cards.json)を書き出す（Node実行）
// カテゴリごとにまとめ、各カード = 誤り/正しい/場面/解説/例文
const fs = require('fs');
const path = require('path');
const dir = __dirname;
const window = {};
eval(fs.readFileSync(path.join(dir, 'data.js'), 'utf8'));
const D = window.IELTS_DATA;

const cats = ["品詞","前置詞","冠詞","コロケーション","文構造"];
const catEn = {
  "品詞":"Word Form", "前置詞":"Prepositions", "冠詞":"Articles",
  "コロケーション":"Collocations", "文構造":"Sentence Structure"
};
const catColor = {
  "品詞":"#2f7de1", "前置詞":"#d98a00", "冠詞":"#1f9d63",
  "コロケーション":"#d4488a", "文構造":"#7c53e0"
};
const catFile = {
  "品詞":"1_WordForm", "前置詞":"2_Prepositions", "冠詞":"3_Articles",
  "コロケーション":"4_Collocations", "文構造":"5_SentenceStructure"
};

// 例文の日本語訳（別ファイル）を合流
const exja = JSON.parse(fs.readFileSync(path.join(dir, "ex-ja.json"), "utf8"));

const groups = cats.map(c => ({
  cat: c,
  catEn: catEn[c],
  color: catColor[c],
  file: catFile[c],
  slides: D.mistakes.filter(m => m.cat === c).map(m => ({
    id: m.id, topic: m.topic, wrong: m.wrong, right: m.right, why: m.why,
    ex: m.ex, exja: exja[m.id] || "", ctx: m.ctx
  }))
}));

const out = { updated: D.updated, title: "IELTS 弱点カード復習", groups };
fs.writeFileSync(path.join(dir, "video-cards.json"), JSON.stringify(out, null, 2), "utf8");
console.log("video-cards.json:", groups.map(g=>g.cat+":"+g.slides.length).join(" "));
