import type { Dictionary, DictionaryEntry, MantraMeaning, Token } from '../namakam.service';
import wordLinks from './word-meaning-links.json';

export interface MeaningWordRow {
  word: string;
  meaning: string;
  token: Token;
}

const aliases: Readonly<Record<string, number[]>> = wordLinks;

function normalizeForm(word: string): string {
  return word.normalize('NFC').replace(/[\u0951\u0952\u1cda\u200b\s=\-।॥]/g, '').replace(/:/g, 'ः');
}

/** Match word identity, never table position. Explicit links cover pada spellings and split verbs. */
export function linkMeaningWords(words: MantraMeaning['words'], dictionary: Dictionary): {
  rows: MeaningWordRow[];
  dictionary: Dictionary;
} {
  const linkedDictionary = { ...dictionary };
  const byForm = new Map(Object.values(dictionary).map(entry => [normalizeForm(entry.clean_form), entry.id]));
  const rows = words.map((item, index) => {
    const exactId = byForm.get(normalizeForm(item.word));
    const wordIds = exactId !== undefined ? [exactId] : (aliases[item.word] || []).filter(id => dictionary[String(id)]);
    if (wordIds.length === 0) {
      // Keep the word usable without fabricating etymology, grammar or citations.
      const id = -(index + 1);
      linkedDictionary[String(id)] = {
        id, clean_form: item.word, pada_form: item.word,
        meanings: { english: item.meaning, nirukta: '', vedantic: '' },
        grammatical_references: { case_ending: '', panini: [] },
        lexicographical_references: { nighantu: '', amara_kosha: '', abhidhana_ratnamala: '' }
      };
      wordIds.push(id);
    }
    return { ...item, token: { text: item.word, word_ids: wordIds } };
  });
  return { rows, dictionary: linkedDictionary };
}

/** Older data contains both string and array grammar references. */
export function normalizeWordDetails(entry: DictionaryEntry): DictionaryEntry {
  const refs = entry.grammatical_references?.panini;
  return {
    ...entry,
    grammatical_references: {
      ...entry.grammatical_references,
      case_ending: entry.grammatical_references?.case_ending || '',
      panini: typeof refs === 'string' ? [refs] : refs || []
    }
  };
}
