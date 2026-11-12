const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.join(__dirname, '..');
const read = name => JSON.parse(fs.readFileSync(path.join(root, name), 'utf8'));

test('every routed mantra has its own complete summary and ordered word table', () => {
  const file = path.join(root, 'src/mantra-meanings.json');
  assert.ok(fs.existsSync(file), 'Curated mantra meanings must exist');
  const meanings = read('src/mantra-meanings.json');
  const expected = Array.from({ length: 11 }, (_, i) => read(`src/anuvakam${i + 1}.json`))
    .flatMap(a => a.mantras.map(m => `${a.anuvakam}_${m.id}`));
  assert.deepEqual(Object.keys(meanings).sort(), expected.sort());
  for (const [key, entry] of Object.entries(meanings)) {
    assert.ok(entry.summary.trim().length > 20, `${key}: meaningful summary`);
    assert.ok(entry.words.length >= 2, `${key}: word list`);
    assert.equal(new Set(entry.words.map(w => w.word)).size, entry.words.length, `${key}: no duplicate forms`);
    for (const row of entry.words) {
      assert.match(row.word, /[\u0900-\u097f]/, `${key}: Sanskrit word`);
      assert.ok(row.meaning.trim(), `${key}: meaning for ${row.word}`);
      assert.doesNotMatch(row.meaning, /^(?:TBD|TODO|unknown|meaning unavailable)$/i);
    }
  }
});

test('opening mantra uses correct word meanings instead of shifted dictionary entries', () => {
  const file = path.join(root, 'src/mantra-meanings.json');
  assert.ok(fs.existsSync(file), 'Curated mantra meanings must exist');
  const first = read('src/mantra-meanings.json')['1_1'];
  const words = Object.fromEntries(first.words.map(w => [w.word, w.meaning]));
  assert.match(words['इषवे'], /arrow/i);
  assert.match(words['अस्तु'], /may.*be|let.*be/i);
  assert.match(words['धन्वने'], /bow/i);
  assert.match(words['बाहुभ्याम्'], /arms/i);
  assert.match(first.summary, /anger|wrath/i);
});

test('protection prayer includes the unborn child identified by both local commentaries', () => {
  const prayer = read('src/mantra-meanings.json')['10_5'];
  assert.match(prayer.words.find(row => row.word === 'उक्षितम्').meaning, /unborn/i);
  assert.match(prayer.summary, /unborn/i);
});

test('table dictionary links reference existing entries and account for every word form', () => {
  const dictionary = read('src/assets/data.json').dictionary;
  const links = read('src/app/mantra-detail/word-meaning-links.json');
  for (const [word, ids] of Object.entries(links)) {
    assert.ok(ids.length, `${word}: dictionary links`);
    for (const id of ids) assert.ok(dictionary[String(id)], `${word}: missing entry ${id}`);
  }
  const normalize = word => word.normalize('NFC').replace(/[\u0951\u0952\u1cda\u200b\s=\-।॥]/g, '').replace(/:/g, 'ः');
  const forms = new Set(Object.values(dictionary).map(entry => normalize(entry.clean_form)));
  const missing = Object.entries(read('src/mantra-meanings.json')).flatMap(([key, entry]) =>
    entry.words.filter(row => !forms.has(normalize(row.word)) && !links[row.word]).map(row => `${key}:${row.word}`));
  // These forms have brief definitions, but no matching detailed analysis in the source dictionary.
  assert.deepEqual(missing, ['1_6:सर्वाः', '10_4:योः']);
});
