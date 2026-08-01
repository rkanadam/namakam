const fs = require('fs');
const path = require('path');

const dir = "/Users/rkanadam/workspace/namakam/src/assets/rudrabhashya/translation";

// 1. Combine clean pages 47 to 72
let fullText = "";
for (let p = 47; p <= 72; p++) {
  const num = String(p).padStart(3, "0");
  const file = `page-${num}.txt`;
  const filePath = path.join(dir, file);
  if (fs.existsSync(filePath)) {
    let content = fs.readFileSync(filePath, "utf8");
    // Clean header lines and page numbers
    content = content.replace(/\d+\s+SRI RUDRA BHASHYAM[^\n]*/gi, "");
    content = content.replace(/SRI RUDRA BHASHYAM[^\n]*\d+/gi, "");
    content = content.replace(/Śrī Rudra Bhāṣyam[^\n]*/gi, "");
    content = content.replace(/^\s*---\s*$/gm, "");
    fullText += "\n" + content;
  }
}

fullText = fullText.replace(/\n{3,}/g, "\n\n");

// End markers for Mantras 1 to 15 of Anuvakam 1
const endMarkers = [
  /Thus\s*\[ends\]\s*the\s*first\s*mantra\./i,
  /Thus\s*\[ends\]\s*the\s*second\s*mantra\./i,
  /Thus\s*\[ends\]\s*the\s*third\s*mantra\./i,
  /Thus\s*\[ends\]\s*the\s*fourth\s*mantra\./i,
  /Thus\s*\[ends\]\s*the\s*fifth\s*mantra\./i,
  /Thus\s*\[ends\]\s*the\s*sixth\s*\[mantra\]\./i,
  /Thus\s*\[ends\]\s*the\s*seventh\s*\[mantra\]\./i,
  /Thus\s*\[ends\]\s*the\s*eighth\s*\[mantra\]\./i,
  /Thus\s*\[ends\]\s*the\s*ninth\s*\[mantra\]\./i,
  /Thus\s*\[ends\]\s*the\s*tenth\s*\[mantra\]\./i,
  /Thus\s*\[ends\]\s*the\s*eleventh\s*\[mantra\]\./i,
  /Thus\s*\[ends\]\s*the\s*twelfth\s*\[mantra\]\./i,
  /Thus\s*\[ends\]\s*the\s*thirteenth\s*\[mantra\]\./i,
  /Thus\s*\[ends\]\s*the\s*fourteenth\s*\[mantra\]\./i,
  /Thus\s*ends\s*the\s*First\s*Anuvāka/i
];

let lastIdx = 0;
const mantras = [];

for (let i = 0; i < 15; i++) {
  const marker = endMarkers[i];
  const match = fullText.substring(lastIdx).match(marker);
  if (!match) {
    console.error(`Could not find end marker for Mantra ${i + 1}`);
    continue;
  }
  const matchIdx = lastIdx + match.index + match[0].length;
  const mantraContent = fullText.substring(lastIdx, matchIdx).trim();
  mantras.push({ id: i + 1, text: mantraContent });
  lastIdx = matchIdx;
}

// 2. Load data.json and update ONLY abhinava_shankara (Rudra Bhashya) fields
const dataPath = path.join(__dirname, '../src/assets/data.json');
const masterData = JSON.parse(fs.readFileSync(dataPath, 'utf8'));

// Update correlated anuvakas[0]
const anv1Correlated = masterData.correlated.anuvakas.find(a => a.id === 1);

mantras.forEach(m => {
  const mId = m.id;
  const key = `1_${mId}`;

  // Update correlated.anuvakas[0].mantras[mId - 1].commentaries.abhinava_shankara
  const corrMantra = anv1Correlated.mantras.find(cm => cm.id === mId);
  if (corrMantra) {
    if (!corrMantra.commentaries) corrMantra.commentaries = {};
    corrMantra.commentaries.abhinava_shankara = m.text;
  }

  // Update data.mantras["1_X"].commentaries.abhinava_shankara
  if (masterData.mantras[key]) {
    const mObj = masterData.mantras[key];
    if (!mObj.commentaries) mObj.commentaries = {};
    if (typeof mObj.commentaries.abhinava_shankara === 'object' && mObj.commentaries.abhinava_shankara !== null) {
      mObj.commentaries.abhinava_shankara.text = m.text;
    } else {
      mObj.commentaries.abhinava_shankara = m.text;
    }
  }

  // Also update individual mantra JSON files if present
  const mantraFilePath = path.join(__dirname, `../src/assets/word_analysis/anuvakam1/mantra${mId}.json`);
  if (fs.existsSync(mantraFilePath)) {
    const mantraJson = JSON.parse(fs.readFileSync(mantraFilePath, 'utf8'));
    if (!mantraJson.commentaries) mantraJson.commentaries = {};
    if (typeof mantraJson.commentaries.abhinava_shankara === 'object' && mantraJson.commentaries.abhinava_shankara !== null) {
      mantraJson.commentaries.abhinava_shankara.text = m.text;
    } else {
      mantraJson.commentaries.abhinava_shankara = m.text;
    }
    fs.writeFileSync(mantraFilePath, JSON.stringify(mantraJson, null, 2), 'utf8');
  }
});

// Save updated data.json
fs.writeFileSync(dataPath, JSON.stringify(masterData, null, 2), 'utf8');
console.log("Successfully updated ONLY Rudra Bhashya (Abhinava Shankara) commentary translations for Anuvakam 1 (Mantras 1-15) in data.json!");
