const fs = require('fs');
const path = require('path');

const scratchDir = "/Users/rkanadam/.gemini/antigravity-cli/brain/4274b45b-5130-4cf4-b57a-1a1520bee02f/scratch";
const text = fs.readFileSync(path.join(scratchDir, "anuvakam1_combined.txt"), "utf8");

// Remove PAGE headers
const cleanText = text.replace(/--- PAGE \d+ ---\n/g, "");

// We want to slice from beginning of Mantra 1 up to end of Mantra 15
// Note that page-018-en.txt starts before Mantra 1 [Word-for-word].
const wfwRegex = /\[Word-for-word\]:/gi;
let match;
const positions = [];
while ((match = wfwRegex.exec(cleanText)) !== null) {
  positions.push(match.index);
}

console.log(`Found ${positions.length} [Word-for-word] occurrences.`);

const parsedMantras = [];

for (let i = 0; i < positions.length; i++) {
  const mantraId = i + 1;
  // Look back a bit to catch verse text / header if any
  let start = positions[i];
  // If there is preceding text before [Word-for-word] for this mantra
  if (i > 0) {
    // start from end of previous block
  }
  const end = (i < positions.length - 1) ? positions[i + 1] : cleanText.length;
  let chunk = cleanText.substring(start, end);

  // Clean chunk: remove trailing verse headers like "|| He speaks the X verse ||" at the very end of chunk
  const nextVerseHeaderMatch = chunk.match(/\|\|\s*He speaks the \w+ verse\s*\|\|/i);
  if (nextVerseHeaderMatch && nextVerseHeaderMatch.index > chunk.length / 2) {
    chunk = chunk.substring(0, nextVerseHeaderMatch.index);
  }

  // Find sections within chunk
  const sayanaMatch = chunk.match(/Sayana'?s Commentary:|Sayanacharya—Bhatta-Bhaskara-Bhashya-Sahita—/i);
  const bhattaMatch = chunk.match(/Bhatta-Bhaskara-Bhashya:|Bhatta Bhaskara Bhashya:/i);
  const dhyanaMatch = chunk.match(/Meditation\s*\(Dhyanam\):|Meditation:/i);

  let wfwText = "";
  let sayanaText = "";
  let bhattaText = "";
  let dhyanaText = "";

  const sayanaIdx = sayanaMatch ? sayanaMatch.index : -1;
  const bhattaIdx = bhattaMatch ? bhattaMatch.index : -1;
  const dhyanaIdx = dhyanaMatch ? dhyanaMatch.index : -1;

  // WFW is from start of chunk up to Sayana or Bhatta
  const firstCommentaryIdx = [sayanaIdx, bhattaIdx, dhyanaIdx].filter(x => x >= 0).sort((a,b)=>a-b)[0] || chunk.length;
  wfwText = chunk.substring(0, firstCommentaryIdx).trim();

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

  parsedMantras.push({
    mantraId,
    wfwText,
    sayanaText,
    bhattaText,
    dhyanaText
  });
}

parsedMantras.forEach(m => {
  console.log(`\n=================== MANTRA ${m.mantraId} ===================`);
  console.log("WFW:", m.wfwText.substring(0, 100).replace(/\n/g, " "));
  console.log("SAYANA:", m.sayanaText.substring(0, 120).replace(/\n/g, " "));
  console.log("BHATTA:", m.bhattaText.substring(0, 120).replace(/\n/g, " "));
  if (m.dhyanaText) console.log("DHYANA:", m.dhyanaText.substring(0, 100).replace(/\n/g, " "));
});
