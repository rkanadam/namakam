const fs = require('fs');
const path = require('path');

const baseDir = path.join(__dirname, '../src/assets/word_analysis');

const prefixMappings = [
  { keywords: ['परेति', 'परा'], word_ids: [22, 588] },
  { keywords: ['प्रेति', 'प्र'], word_ids: [11, 588] },
  { keywords: ['परिति', 'परि'], word_ids: [52, 588] },
  { keywords: ['नीति', 'नि'], word_ids: [64, 588] },
  { keywords: ['अधीति', 'अधि'], word_ids: [103, 588] },
  { keywords: ['अवेति', 'अव'], word_ids: [124, 588] }
];

for (let a = 1; a <= 11; a++) {
  const anvPath = path.join(baseDir, `anuvakam${a}`);
  if (!fs.existsSync(anvPath)) continue;

  const files = fs.readdirSync(anvPath).filter(f => f.startsWith('mantra') && f.endsWith('.json'));

  files.forEach(f => {
    const filePath = path.join(anvPath, f);
    const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    let modified = false;

    (data.pada_tokens || []).forEach(t => {
      const text = t.text.trim();
      if (!text || text === '(' || text === ')' || text === '।' || text === '॥') return;

      if (text.includes('परेति') || text.includes('परा')) {
        t.word_ids = [22, 588];
        modified = true;
      } else if (text.includes('प्रेति') || (text.includes('प्र') && text.length <= 4 && !text.includes('प्रथम'))) {
        t.word_ids = [11, 588];
        modified = true;
      } else if (text.includes('परिति') || (text.includes('परि') && text.length <= 5 && !text.includes('कपर्दि'))) {
        t.word_ids = [52, 588];
        modified = true;
      } else if (text.includes('नीति') || (text.includes('नि') && text.length <= 3 && !text.includes('निशी'))) {
        t.word_ids = [64, 588];
        modified = true;
      } else if (text.includes('अधीति')) {
        t.word_ids = [103, 588];
        modified = true;
      } else if (text.includes('अवेति')) {
        t.word_ids = [124, 588];
        modified = true;
      }
    });

    if (modified) {
      fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
    }
  });
}

console.log('Successfully mapped all Veshṭana sandhi prefix tokens (परेति, प्रेति, परिति, नीति, अधीति, अवेति)!');
