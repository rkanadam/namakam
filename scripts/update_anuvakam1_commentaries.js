const fs = require('fs');
const path = require('path');

const scratchDir = "/Users/rkanadam/.gemini/antigravity-cli/brain/4274b45b-5130-4cf4-b57a-1a1520bee02f/scratch";
const rawText = fs.readFileSync(path.join(scratchDir, "anuvakam1_combined.txt"), "utf8");

// Clean page headers and running headers
let cleanText = rawText
  .replace(/--- PAGE \d+ ---\n/g, "")
  .replace(/Sayanacharya—Bhatta-Bhaskara-Bhashya-Sahita—[^\n]*/gi, "")
  .replace(/\[Na\.\s*[A-Za-z\.]+\s*Am\.\][^\n]*/gi, "");

// Split by [Word-for-word]:
const wfwRegex = /\[Word-for-word\]:/gi;
let match;
const positions = [];
while ((match = wfwRegex.exec(cleanText)) !== null) {
  positions.push(match.index);
}

console.log(`Found ${positions.length} [Word-for-word] occurrences for Anuvakam 1.`);

const parsedMantras = [];

for (let i = 0; i < positions.length; i++) {
  const mantraId = i + 1;
  let start = positions[i];
  const end = (i < positions.length - 1) ? positions[i + 1] : cleanText.length;
  let chunk = cleanText.substring(start, end);

  // Clean chunk of trailing verse headers for next verse
  const nextVerseHeaderMatch = chunk.match(/\|\|\s*He speaks the \w+ verse\s*\|\|/i);
  if (nextVerseHeaderMatch && nextVerseHeaderMatch.index > chunk.length / 2) {
    chunk = chunk.substring(0, nextVerseHeaderMatch.index);
  }

  const sayanaMatch = chunk.match(/Sayana'?s Commentary:/i);
  const bhattaMatch = chunk.match(/Bhatta[\s\-]Bhaskara'?s?\s*Commentary:|Bhatta[\s\-]Bhaskara[\s\-]Bhashya:/i);
  const dhyanaMatch = chunk.match(/Meditation\s*\(Dhyanam\):|Meditation:/i);

  const sayanaIdx = sayanaMatch ? sayanaMatch.index : -1;
  const bhattaIdx = bhattaMatch ? bhattaMatch.index : -1;
  const dhyanaIdx = dhyanaMatch ? dhyanaMatch.index : -1;

  let sayanaText = "";
  let bhattaText = "";
  let dhyanaText = "";

  if (sayanaIdx >= 0) {
    const endSayana = (bhattaIdx > sayanaIdx) ? bhattaIdx : ((dhyanaIdx > sayanaIdx) ? dhyanaIdx : chunk.length);
    sayanaText = chunk.substring(sayanaIdx + sayanaMatch[0].length, endSayana).trim();
  }

  if (bhattaIdx >= 0) {
    const endBhatta = (dhyanaIdx > bhattaIdx) ? dhyanaIdx : chunk.length;
    bhattaText = chunk.substring(bhattaIdx + bhattaMatch[0].length, endBhatta).trim();
  }

  if (dhyanaIdx >= 0) {
    dhyanaText = chunk.substring(dhyanaIdx + dhyanaMatch[0].length).trim();
  }

  let rishi = "";
  let chandas = "";
  let devata = "";

  const rishiMatch = bhattaText.match(/Rishi is ([^\.\,\;]+)/i) || sayanaText.match(/Rishi is ([^\.\,\;]+)/i);
  if (rishiMatch) rishi = rishiMatch[1].trim();

  const chandasMatch = bhattaText.match(/Metre is ([^\.\,\;]+)/i) || bhattaText.match(/metre is ([^\.\,\;]+)/i) || sayanaText.match(/Metre is ([^\.\,\;]+)/i);
  if (chandasMatch) chandas = chandasMatch[1].trim();

  const devataMatch = bhattaText.match(/Deity is ([^\.\,\;]+)/i) || sayanaText.match(/Deity is ([^\.\,\;]+)/i);
  if (devataMatch) devata = devataMatch[1].trim();

  parsedMantras.push({
    mantraId,
    sayanaText,
    bhattaText,
    dhyanaText,
    rishi,
    chandas,
    devata
  });
}

// Update data.json
const dataPath = path.join(__dirname, '../src/assets/data.json');
const masterData = JSON.parse(fs.readFileSync(dataPath, 'utf8'));

// Update correlated anuvakas[0]
const anv1Correlated = masterData.correlated.anuvakas.find(a => a.id === 1);

parsedMantras.forEach(pm => {
  const mId = pm.mantraId;
  const key = `1_${mId}`;

  // Update correlated
  const corrMantra = anv1Correlated.mantras.find(m => m.id === mId);
  if (corrMantra) {
    if (!corrMantra.commentaries) corrMantra.commentaries = {};
    if (pm.sayanaText) corrMantra.commentaries.sayana = pm.sayanaText;
    if (pm.bhattaText) corrMantra.commentaries.bhatta_bhaskara = pm.bhattaText;
  }

  // Update data.mantras["1_X"]
  if (masterData.mantras[key]) {
    const mObj = masterData.mantras[key];
    if (!mObj.commentaries) mObj.commentaries = {};

    if (!mObj.commentaries.sayana) mObj.commentaries.sayana = {};
    if (pm.sayanaText) mObj.commentaries.sayana.text = pm.sayanaText;

    if (!mObj.commentaries.bhatta_bhaskara) mObj.commentaries.bhatta_bhaskara = {};
    if (pm.bhattaText) mObj.commentaries.bhatta_bhaskara.text = pm.bhattaText;
    if (pm.dhyanaText) mObj.commentaries.bhatta_bhaskara.dhyana = pm.dhyanaText;
    if (pm.rishi) mObj.commentaries.bhatta_bhaskara.rishi = pm.rishi;
    if (pm.chandas) mObj.commentaries.bhatta_bhaskara.chandas = pm.chandas;
    if (pm.devata) mObj.commentaries.bhatta_bhaskara.devata = pm.devata;
  }

  // Update individual JSON file src/assets/word_analysis/anuvakam1/mantraX.json
  const mantraFilePath = path.join(__dirname, `../src/assets/word_analysis/anuvakam1/mantra${mId}.json`);
  if (fs.existsSync(mantraFilePath)) {
    const mantraJson = JSON.parse(fs.readFileSync(mantraFilePath, 'utf8'));
    if (!mantraJson.commentaries) mantraJson.commentaries = {};

    if (!mantraJson.commentaries.sayana) mantraJson.commentaries.sayana = {};
    if (pm.sayanaText) mantraJson.commentaries.sayana.text = pm.sayanaText;

    if (!mantraJson.commentaries.bhatta_bhaskara) mantraJson.commentaries.bhatta_bhaskara = {};
    if (pm.bhattaText) mantraJson.commentaries.bhatta_bhaskara.text = pm.bhattaText;
    if (pm.dhyanaText) mantraJson.commentaries.bhatta_bhaskara.dhyana = pm.dhyanaText;
    if (pm.rishi) mantraJson.commentaries.bhatta_bhaskara.rishi = pm.rishi;
    if (pm.chandas) mantraJson.commentaries.bhatta_bhaskara.chandas = pm.chandas;
    if (pm.devata) mantraJson.commentaries.bhatta_bhaskara.devata = pm.devata;

    fs.writeFileSync(mantraFilePath, JSON.stringify(mantraJson, null, 2), 'utf8');
  }
});

// Save master data.json
fs.writeFileSync(dataPath, JSON.stringify(masterData, null, 2), 'utf8');
console.log("Successfully updated Anuvakam 1 English commentary translations in data.json and individual mantra files!");
