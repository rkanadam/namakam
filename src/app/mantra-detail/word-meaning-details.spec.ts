import { linkMeaningWords } from './word-meaning-details';
import { DictionaryEntry } from '../namakam.service';

describe('Word meaning dictionary links', () => {
  const all: DictionaryEntry = {
    id: 99, clean_form: 'सर्वम्', pada_form: 'सर्व॑म्',
    meanings: { english: 'All', nirukta: '', vedantic: '' },
    grammatical_references: { case_ending: 'Neuter singular', panini: [] },
    lexicographical_references: { nighantu: '', amara_kosha: '', abhidhana_ratnamala: '' }
  };

  it('does not borrow the grammar of a different inflection for an unmatched word', () => {
    const linked = linkMeaningWords([{ word: 'सर्वाः', meaning: 'All' }], { '99': all });
    const entry = linked.dictionary[String(linked.rows[0].token.word_ids[0])];
    expect(entry.clean_form).toBe('सर्वाः');
    expect(entry.meanings.english).toBe('All');
    expect(entry.grammatical_references.case_ending).not.toContain('Neuter singular');
  });

  it('matches the same word despite accent marks and leaves the source dictionary unchanged', () => {
    const dictionary = { '99': all };
    const linked = linkMeaningWords([{ word: 'सर्व॑म्', meaning: 'All' }], dictionary);
    expect(linked.rows[0].token.word_ids).toEqual([99]);
    expect(dictionary['99']).toBe(all);
    expect(Object.keys(dictionary)).toEqual(['99']);
  });
});
