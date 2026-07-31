const fs = require('fs');
const path = require('path');

const baseDir = path.join(__dirname, '../src/assets/word_analysis');
const gDictPath = path.join(baseDir, 'global_dictionary.json');
const gDict = JSON.parse(fs.readFileSync(gDictPath, 'utf8'));

const dictList = Object.values(gDict);

function stripAccentsAndPunct(str) {
  return str
    .replace(/[\u0951\u0952\u0901\u0902\u0903\u093C]/g, '') // remove svara accents
    .replace(/[-=()]/g, '')
    .replace(/म्$/, 'म') // normalize anusvara/m-halanta
    .replace(/ं$/, 'म')
    .trim();
}

function mapTokensForMantra(anvNum, mNum) {
  const filePath = path.join(baseDir, `anuvakam${anvNum}`, `mantra${mNum}.json`);
  if (!fs.existsSync(filePath)) return;

  const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));

  ['samhita_tokens', 'pada_tokens', 'krama_tokens'].forEach(tType => {
    if (!data[tType]) return;

    data[tType].forEach(t => {
      const text = t.text.trim();
      if (!text || text === '।' || text === '॥' || text === '=' || text === '-' || text === '(' || text === ')') {
        t.word_ids = [];
        return;
      }

      const normText = stripAccentsAndPunct(text);
      if (!normText || normText.length === 0) {
        t.word_ids = [];
        return;
      }

      const matched = [];

      // 1. Exact match against clean_form or pada_form
      dictList.forEach(entry => {
        const normClean = stripAccentsAndPunct(entry.clean_form);
        const normPada = stripAccentsAndPunct(entry.pada_form);

        if (normText === normClean || normText === normPada) {
          if (!matched.includes(entry.id)) matched.push(entry.id);
        }
      });

      // 2. Substring match for compound words if no exact match found
      if (matched.length === 0 && normText.length >= 2) {
        dictList.forEach(entry => {
          const normClean = stripAccentsAndPunct(entry.clean_form);
          if (!normClean || normClean.length < 2) return;

          if (normText.includes(normClean) || normClean.includes(normText)) {
            if (!matched.includes(entry.id)) matched.push(entry.id);
          }
        });
      }

      // 3. Special handling for Veshṭana "इति" in pada_tokens
      if (text.includes('इति') || text.includes('इत्य') || text.includes('इती')) {
        if (!matched.includes(588)) matched.push(588);
      }

      // DO NOT FALL BACK TO 588 BLINDLY!
      t.word_ids = matched;
    });
  });

  fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
}

for (let a = 1; a <= 11; a++) {
  const anvPath = path.join(baseDir, `anuvakam${a}`);
  if (!fs.existsSync(anvPath)) continue;
  const files = fs.readdirSync(anvPath).filter(f => f.startsWith('mantra') && f.endsWith('.json'));

  files.forEach(f => {
    const mNum = parseInt(f.replace('mantra', '').replace('.json', ''), 10);
    mapTokensForMantra(a, mNum);
  });
}

console.log('Cleanly mapped all tokens across all 11 Anuvakams without false 588 fallback!');
