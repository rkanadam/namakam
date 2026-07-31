import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ItransService {

  /**
   * Converts ITRANS / Phonetic QWERTY text into Devanagari Sanskrit.
   * Example: "namaste rudra manyave" -> "नमस्ते रुद्र मन्यवे"
   */
  toDevanagari(text: string): string {
    if (!text) return '';

    let out = '';
    let i = 0;
    const len = text.length;

    while (i < len) {
      // 1. Preserve existing Devanagari characters, spaces, punctuation, and Vedic swaras (\u0951, \u0952, \u1CDA)
      const code = text.charCodeAt(i);
      if ((code >= 0x0900 && code <= 0x097F) || (code >= 0x1CD0 && code <= 0x1CFF) || text[i] === ' ' || text[i] === '\n' || text[i] === '\t') {
        out += text[i];
        i++;
        continue;
      }

      // Check Danda / Double Danda / Avagraha
      if (text.substr(i, 2) === '||') { out += '॥'; i += 2; continue; }
      if (text[i] === '|') { out += '।'; i++; continue; }
      if (text.substr(i, 2) === '.a') { out += 'ऽ'; i += 2; continue; }
      if (text[i] === 'H') { out += 'ः'; i++; continue; }
      if (text[i] === 'M' || text.substr(i, 2) === '.n') {
        out += 'ं';
        i += (text[i] === 'M' ? 1 : 2);
        continue;
      }

      // Consonant mappings (longest match first)
      const consMatch = this.matchConsonant(text, i);
      if (consMatch) {
        const consDev = consMatch.dev;
        i += consMatch.len;

        // Look ahead for vowel attached to this consonant
        const vowelMatch = this.matchVowelMatra(text, i);
        if (vowelMatch) {
          out += consDev + vowelMatch.matra;
          i += vowelMatch.len;
        } else if (i < len && (text[i] === 'a' || text[i] === 'A')) {
          if (text[i] === 'a') {
            out += consDev; // inherent 'a' vowel
            i += 1;
          } else {
            out += consDev + 'ा'; // 'A' matra
            i += 1;
          }
        } else {
          // No vowel following: add Virama (्) unless at end of word or before punctuation/space
          if (i < len && /[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]/.test(text[i])) {
            out += consDev + '्';
          } else {
            out += consDev + '्';
          }
        }
        continue;
      }

      // Independent Vowels
      const indVowel = this.matchIndependentVowel(text, i);
      if (indVowel) {
        out += indVowel.dev;
        i += indVowel.len;
        continue;
      }

      // Fallback: pass character as is
      out += text[i];
      i++;
    }

    // Clean up trailing virama before space or punctuation if user typed full word
    return out.replace(/्(?=[\s।॥]|$)/g, '');
  }

  private matchConsonant(text: string, i: number): { dev: string; len: number } | null {
    const sub3 = text.substr(i, 3);
    const sub2 = text.substr(i, 2);
    const sub1 = text.substr(i, 1);

    if (sub3 === 'chh') return { dev: 'छ', len: 3 };
    if (sub3 === 'RRi') return { dev: 'ऋ', len: 3 };

    if (sub2 === 'kh') return { dev: 'ख', len: 2 };
    if (sub2 === 'gh') return { dev: 'घ', len: 2 };
    if (sub2 === 'ch' || sub2 === 'Ch') return { dev: 'छ', len: 2 };
    if (sub2 === 'jh') return { dev: 'झ', len: 2 };
    if (sub2 === 'Th') return { dev: 'ठ', len: 2 };
    if (sub2 === 'Dh') return { dev: 'ढ', len: 2 };
    if (sub2 === 'th') return { dev: 'थ', len: 2 };
    if (sub2 === 'dh') return { dev: 'ध', len: 2 };
    if (sub2 === 'ph') return { dev: 'फ', len: 2 };
    if (sub2 === 'bh') return { dev: 'भ', len: 2 };
    if (sub2 === 'sh') return { dev: 'श', len: 2 };
    if (sub2 === 'Sh' || sub2 === 'sS') return { dev: 'ष', len: 2 };
    if (sub2 === '~N') return { dev: 'ङ', len: 2 };
    if (sub2 === '~n') return { dev: 'ञ', len: 2 };
    if (sub2 === 'GY') return { dev: 'ज्ञ', len: 2 };

    const c1 = sub1;
    if (c1 === 'k') return { dev: 'क', len: 1 };
    if (c1 === 'g') return { dev: 'ग', len: 1 };
    if (c1 === 'c') return { dev: 'च', len: 1 };
    if (c1 === 'j') return { dev: 'ज', len: 1 };
    if (c1 === 'T') return { dev: 'ट', len: 1 };
    if (c1 === 'D') return { dev: 'ड', len: 1 };
    if (c1 === 'N') return { dev: 'ण', len: 1 };
    if (c1 === 't') return { dev: 'त', len: 1 };
    if (c1 === 'd') return { dev: 'द', len: 1 };
    if (c1 === 'n') return { dev: 'न', len: 1 };
    if (c1 === 'p') return { dev: 'प', len: 1 };
    if (c1 === 'b') return { dev: 'ब', len: 1 };
    if (c1 === 'm') return { dev: 'म', len: 1 };
    if (c1 === 'y') return { dev: 'य', len: 1 };
    if (c1 === 'r') return { dev: 'र', len: 1 };
    if (c1 === 'l') return { dev: 'ल', len: 1 };
    if (c1 === 'v' || c1 === 'w') return { dev: 'व', len: 1 };
    if (c1 === 's') return { dev: 'स', len: 1 };
    if (c1 === 'h') return { dev: 'ह', len: 1 };

    return null;
  }

  private matchVowelMatra(text: string, i: number): { matra: string; len: number } | null {
    const sub2 = text.substr(i, 2);
    if (sub2 === 'aa') return { matra: 'ा', len: 2 };
    if (sub2 === 'ii') return { matra: 'ी', len: 2 };
    if (sub2 === 'uu') return { matra: 'ू', len: 2 };
    if (sub2 === 'ai') return { matra: 'ै', len: 2 };
    if (sub2 === 'au') return { matra: 'ौ', len: 2 };

    const c1 = text[i];
    if (c1 === 'A') return { matra: 'ा', len: 1 };
    if (c1 === 'i') return { matra: 'ि', len: 1 };
    if (c1 === 'I') return { matra: 'ी', len: 1 };
    if (c1 === 'u') return { matra: 'ु', len: 1 };
    if (c1 === 'U') return { matra: 'ू', len: 1 };
    if (c1 === 'R') return { matra: 'ृ', len: 1 };
    if (c1 === 'e') return { matra: 'े', len: 1 };
    if (c1 === 'o') return { matra: 'ो', len: 1 };

    return null;
  }

  private matchIndependentVowel(text: string, i: number): { dev: string; len: number } | null {
    const sub2 = text.substr(i, 2);
    if (sub2 === 'aa') return { dev: 'आ', len: 2 };
    if (sub2 === 'ii') return { dev: 'ई', len: 2 };
    if (sub2 === 'uu') return { dev: 'ऊ', len: 2 };
    if (sub2 === 'ai') return { dev: 'ऐ', len: 2 };
    if (sub2 === 'au') return { dev: 'औ', len: 2 };

    const c1 = text[i];
    if (c1 === 'a') return { dev: 'अ', len: 1 };
    if (c1 === 'A') return { dev: 'आ', len: 1 };
    if (c1 === 'i') return { dev: 'इ', len: 1 };
    if (c1 === 'I') return { dev: 'ई', len: 1 };
    if (c1 === 'u') return { dev: 'उ', len: 1 };
    if (c1 === 'U') return { dev: 'ऊ', len: 1 };
    if (c1 === 'R') return { dev: 'ऋ', len: 1 };
    if (c1 === 'e') return { dev: 'ए', len: 1 };
    if (c1 === 'o') return { dev: 'ओ', len: 1 };

    return null;
  }
}
