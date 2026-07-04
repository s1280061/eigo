// data.js から音声化用のテキスト(JSON)を書き出す（Node実行）
const fs = require('fs');
const path = require('path');
const dir = __dirname;
const window = {};
eval(fs.readFileSync(path.join(dir, 'data.js'), 'utf8'));
const D = window.IELTS_DATA;

// 英語ラベル（音声の頭出し用。日本語タイトルはTTSで読めないため）
const enTitle = {
  E1: "Email to a friend",
  E2: "Globalisation: advantages and disadvantages",
  E3: "A successful multicultural country",
  E4: "The most popular festival in Japan",
  E5: "Facebook users by age group",
  E6: "Application letter"
};
const catEn = {
  "品詞": "Word Form",
  "前置詞": "Prepositions",
  "冠詞": "Articles",
  "コロケーション": "Collocations",
  "文構造": "Sentence Structure"
};

const models = D.essays.map(e => ({
  id: e.id,
  enTitle: enTitle[e.id] || e.id,
  jaTitle: e.title,
  // 段落は \n\n で保持（Python側で段落間に無音を入れる）
  text: e.natural
}));

const cats = ["品詞","前置詞","冠詞","コロケーション","文構造"];
const sentenceGroups = cats.map(c => ({
  cat: c,
  catEn: catEn[c],
  sentences: D.mistakes.filter(m => m.cat === c).map(m => ({ id: m.id, ex: m.ex }))
}));

const out = { updated: D.updated, models, sentenceGroups };
fs.writeFileSync(path.join(dir, 'audio_content.json'), JSON.stringify(out, null, 2), 'utf8');
console.log('audio_content.json:', models.length, 'models,', sentenceGroups.reduce((a,g)=>a+g.sentences.length,0), 'sentences');
