const fs = require('fs');
const path = require('path');

const baseDir = path.join(__dirname, '../src/assets/word_analysis');
const gDictPath = path.join(baseDir, 'global_dictionary.json');
const gDict = JSON.parse(fs.readFileSync(gDictPath, 'utf8'));

// 1. Add entry 588 for "iti"
gDict["588"] = {
  id: 588,
  pada_form: "इति॑",
  clean_form: "इति",
  meanings: {
    english: "Indeclinable particle; thus; so; Vedic Padapatha Veshṭana pause marker",
    nirukta: "Indicates the end of a padapatha word or compound unstringing (veshṭana). Sāyaṇa: iti = evam (thus/so).",
    vedantic: "In Vedic recitation, iti marks the definitive separation of compound words into their essential roots."
  },
  grammatical_references: {
    panini: ["P 1.4.57 — Ca-ādayo 'sattve (nipāta / avyaya)"],
    case_ending: "Avyaya (indeclinable particle)"
  },
  lexicographical_references: {
    nighantu: "Nighaṇṭu 3.22 — avyaya section.",
    amara_kosha: "Amarakośa 3.4.14 — iti is listed under avyayas.",
    abhidhana_ratnamala: ""
  }
};

fs.writeFileSync(gDictPath, JSON.stringify(gDict, null, 2), 'utf8');

// 2. Map word_ids: [588] to all "इति॑" tokens in pada_tokens across all anuvakams
const dirs = fs.readdirSync(baseDir).filter(d => d.startsWith('anuvakam'));
dirs.forEach(anvDir => {
  const anvPath = path.join(baseDir, anvDir);
  const files = fs.readdirSync(anvPath).filter(f => f.startsWith('mantra') && f.endsWith('.json'));

  files.forEach(file => {
    const filePath = path.join(anvPath, file);
    const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    let modified = false;

    (data.pada_tokens || []).forEach(t => {
      if (t.text.trim() === 'इति॑' && (!t.word_ids || t.word_ids.length === 0)) {
        t.word_ids = [588];
        modified = true;
      }
    });

    if (modified) {
      fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
    }
  });
});

// 3. Sync root src/anuvakamN.json files
for (let a = 1; a <= 11; a++) {
  const rootFile = path.join(__dirname, `../src/anuvakam${a}.json`);
  if (!fs.existsSync(rootFile)) continue;
  const rootData = JSON.parse(fs.readFileSync(rootFile, 'utf8'));
  const anvPath = path.join(baseDir, `anuvakam${a}`);
  const files = fs.readdirSync(anvPath).filter(f => f.startsWith('mantra') && f.endsWith('.json'));

  files.forEach(file => {
    const mId = parseInt(file.replace('mantra', '').replace('.json', ''), 10);
    const mData = JSON.parse(fs.readFileSync(path.join(anvPath, file), 'utf8'));
    const rootMantra = rootData.mantras.find(m => m.id === mId);
    if (rootMantra) {
      if (mData.samhita_tokens) rootMantra.samhita_tokens = mData.samhita_tokens;
      if (mData.pada_tokens) rootMantra.pada_tokens = mData.pada_tokens;
      if (mData.krama_tokens) rootMantra.krama_tokens = mData.krama_tokens;
    }
  });
  fs.writeFileSync(rootFile, JSON.stringify(rootData, null, 2), 'utf8');
}

console.log('Added entry 588 (iti) and mapped all iti tokens in pada_tokens across all anuvakams!');
