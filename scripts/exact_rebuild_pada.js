const fs = require('fs');
const path = require('path');

const baseDir = path.join(__dirname, '../src/assets/word_analysis');

for (let a = 1; a <= 11; a++) {
  const anvPath = path.join(baseDir, `anuvakam${a}`);
  if (!fs.existsSync(anvPath)) continue;

  const files = fs.readdirSync(anvPath).filter(f => f.startsWith('mantra') && f.endsWith('.json'));

  files.forEach(f => {
    const filePath = path.join(anvPath, f);
    const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    const padaText = data.pada;
    if (!padaText) return;

    // Split on space, danda, double danda keeping delimiters
    const parts = padaText.split(/(\s+|।|॥)/).filter(Boolean);
    const tokens = [];

    parts.forEach(p => {
      tokens.push({ text: p, word_ids: [] });
    });

    data.pada_tokens = tokens;
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
  });
}

console.log('Rebuilt exact pada_tokens character-for-character for all mantras!');
