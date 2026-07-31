const fs = require('fs');
const path = require('path');

/**
 * Script to permanently apply exported Sanskrit text corrections to source JSON files on disk.
 * Usage: node scripts/apply_edits.js [path-to-corrections.json]
 */

const projectRoot = path.resolve(__dirname, '..');
const correctionsFilePath = process.argv[2] || path.join(projectRoot, 'sanskrit_corrections.json');

if (!fs.existsSync(correctionsFilePath)) {
  console.error(`Error: Corrections file not found at: ${correctionsFilePath}`);
  console.log(`Usage: node scripts/apply_edits.js <path-to-exported-corrections.json>`);
  process.exit(1);
}

const corrections = JSON.parse(fs.readFileSync(correctionsFilePath, 'utf8'));
const keys = Object.keys(corrections);

console.log(`Found ${keys.length} mantra correction(s) to apply to disk.`);

let updatedCount = 0;

for (const key of keys) {
  const [anuvakamId, mantraId] = key.split('_').map(Number);
  const edit = corrections[key];

  console.log(`Applying corrections for Anuvakam ${anuvakamId}, Mantra ${mantraId}...`);

  // 1. Update src/anuvakamX.json
  const anuvakamJsonPath = path.join(projectRoot, 'src', `anuvakam${anuvakamId}.json`);
  if (fs.existsSync(anuvakamJsonPath)) {
    const data = JSON.parse(fs.readFileSync(anuvakamJsonPath, 'utf8'));
    const mantra = data.mantras?.find(m => m.id === mantraId);
    if (mantra) {
      if (edit.samhita) mantra.samhita = edit.samhita;
      if (edit.pada) mantra.pada = edit.pada;
      if (edit.krama) mantra.krama = edit.krama;
      fs.writeFileSync(anuvakamJsonPath, JSON.stringify(data, null, 2), 'utf8');
      console.log(`  ✓ Updated ${path.relative(projectRoot, anuvakamJsonPath)}`);
    }
  }

  // 2. Update src/assets/word_analysis/anuvakamX/mantraY.json
  const mantraDetailPath = path.join(projectRoot, 'src', 'assets', 'word_analysis', `anuvakam${anuvakamId}`, `mantra${mantraId}.json`);
  if (fs.existsSync(mantraDetailPath)) {
    const data = JSON.parse(fs.readFileSync(mantraDetailPath, 'utf8'));
    if (edit.samhita) data.samhita = edit.samhita;
    if (edit.pada) data.pada = edit.pada;
    if (edit.krama) data.krama = edit.krama;
    fs.writeFileSync(mantraDetailPath, JSON.stringify(data, null, 2), 'utf8');
    console.log(`  ✓ Updated ${path.relative(projectRoot, mantraDetailPath)}`);
  }

  // 3. Update src/assets/correlated_namakam.json
  const correlatedPath = path.join(projectRoot, 'src', 'assets', 'correlated_namakam.json');
  if (fs.existsSync(correlatedPath)) {
    const data = JSON.parse(fs.readFileSync(correlatedPath, 'utf8'));
    const anuvaka = data.anuvakas?.find(a => a.id === anuvakamId);
    if (anuvaka) {
      const mantra = anuvaka.mantras?.find(m => m.id === mantraId);
      if (mantra && mantra.sanskrit) {
        if (edit.samhita) mantra.sanskrit.samhita = edit.samhita;
        if (edit.pada) mantra.sanskrit.pada = edit.pada;
        if (edit.krama) mantra.sanskrit.krama = edit.krama;
      }
    }
    fs.writeFileSync(correlatedPath, JSON.stringify(data, null, 2), 'utf8');
    console.log(`  ✓ Updated ${path.relative(projectRoot, correlatedPath)}`);
  }

  updatedCount++;
}

console.log(` Successfully applied ${updatedCount} mantra edit(s) permanently to disk files!`);
