const fs = require('fs');
const path = require('path');

const baseDir = path.join(__dirname, '../src/assets/word_analysis');
const dataPath = path.join(__dirname, '../src/assets/data.json');

console.log('Regenerating src/assets/data.json...');

// 1. Read global dictionary
const gDict = JSON.parse(fs.readFileSync(path.join(baseDir, 'global_dictionary.json'), 'utf8'));

// 2. Read word index
const wordIndex = JSON.parse(fs.readFileSync(path.join(baseDir, 'word_index.json'), 'utf8'));

// 3. Build mantras map across all 11 anuvakams
const mantrasMap = {};
const dirs = fs.readdirSync(baseDir).filter(d => d.startsWith('anuvakam'));
dirs.sort((a, b) => parseInt(a.replace('anuvakam', ''), 10) - parseInt(b.replace('anuvakam', ''), 10));

dirs.forEach(anvDir => {
  const anvNum = parseInt(anvDir.replace('anuvakam', ''), 10);
  const anvPath = path.join(baseDir, anvDir);
  const files = fs.readdirSync(anvPath).filter(f => f.startsWith('mantra') && f.endsWith('.json'));
  files.sort((a, b) => parseInt(a.replace('mantra', ''), 10) - parseInt(b.replace('mantra', ''), 10));

  files.forEach(file => {
    const mantraNum = parseInt(file.replace('mantra', '').replace('.json', ''), 10);
    const content = JSON.parse(fs.readFileSync(path.join(anvPath, file), 'utf8'));
    const key = `${anvNum}_${mantraNum}`;
    mantrasMap[key] = content;
  });
});

// 4. Load correlated data if present in existing data.json
let correlatedData = {};
if (fs.existsSync(dataPath)) {
  const oldData = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
  if (oldData.correlated) correlatedData = oldData.correlated;
}

const fullData = {
  correlated: correlatedData,
  dictionary: gDict,
  wordIndex: wordIndex,
  mantras: mantrasMap
};

fs.writeFileSync(dataPath, JSON.stringify(fullData, null, 2), 'utf8');
const stats = fs.statSync(dataPath);
console.log(`Re-generated src/assets/data.json successfully! Total size: ${(stats.size / 1024 / 1024).toFixed(2)} MB (${Object.keys(mantrasMap).length} mantras, ${Object.keys(gDict).length} dictionary entries).`);
