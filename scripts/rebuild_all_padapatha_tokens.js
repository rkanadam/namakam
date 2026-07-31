const fs = require('fs');
const path = require('path');

const baseDir = path.join(__dirname, '../src/assets/word_analysis');
const gDictPath = path.join(baseDir, 'global_dictionary.json');
const gDict = JSON.parse(fs.readFileSync(gDictPath, 'utf8'));

// Helper to rebuild pada_tokens for a mantra from its full pada text string
function rebuildPadaTokens(anvNum, mNum) {
  const filePath = path.join(baseDir, `anuvakam${anvNum}`, `mantra${mNum}.json`);
  if (!fs.existsSync(filePath)) return;

  const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  const padaText = data.pada;
  if (!padaText) return;

  // Split by space keeping delimiters
  const rawParts = padaText.split(/(\s+|।+|॥+)/).filter(Boolean);
  const newTokens = [];

  rawParts.forEach(part => {
    if (part === ' । ' || part === ' ।' || part === '। ' || part === '।' || part === ' ॥' || part === '॥' || part === ' ') {
      newTokens.push({ text: part, word_ids: [] });
      return;
    }

    const trimmed = part.trim();
    if (!trimmed) return;

    // Find matching word_ids from global_dictionary or existing pada_tokens
    let matchedIds = [];

    // Check existing pada_tokens for exact text match first
    const existing = (data.pada_tokens || []).find(t => t.text.trim() === trimmed || trimmed.includes(t.text.trim()));
    if (existing && existing.word_ids && existing.word_ids.length > 0) {
      matchedIds = [...existing.word_ids];
    } else {
      // Search in global dictionary by clean_form or pada_form
      Object.keys(gDict).forEach(id => {
        const e = gDict[id];
        if (e.pada_form === trimmed || e.clean_form === trimmed) {
          if (!matchedIds.includes(e.id)) matchedIds.push(e.id);
        }
      });
      // Fallback for Veshṭana marker "इति"
      if (trimmed.includes('इति') && !matchedIds.includes(588)) {
        matchedIds.push(588);
      }
    }

    newTokens.push({ text: part, word_ids: matchedIds });
  });

  data.pada_tokens = newTokens;
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
}

// Rebuild for Anuvakam 1 Mantras 1-15
for (let m = 1; m <= 15; m++) {
  rebuildPadaTokens(1, m);
}

console.log('Rebuilt pada_tokens from authentic pada text for Anuvakam 1 Mantras 1-15!');
