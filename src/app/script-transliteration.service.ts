import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

export interface LanguageOption {
  code: string;
  label: string;
  native: string;
}

@Injectable({
  providedIn: 'root'
})
export class ScriptTransliterationService {
  readonly languages: LanguageOption[] = [
    { code: 'sanskrit', label: 'संस्कृतम् (Sanskrit)', native: 'संस्कृतम्' },
    { code: 'hindi', label: 'हिन्दी (Hindi)', native: 'हिन्दी' },
    { code: 'english', label: 'English (IAST)', native: 'English (IAST)' },
    { code: 'kannada', label: 'ಕನ್ನಡ (Kannada)', native: 'ಕನ್ನಡ' },
    { code: 'telugu', label: 'తెలుగు (Telugu)', native: 'తెలుగు' },
    { code: 'tamil', label: 'தமிழ் (Tamil)', native: 'தமிழ்' },
    { code: 'malayalam', label: 'മലയാളം (Malayalam)', native: 'മലയാളം' }
  ];

  private currentLangSubject = new BehaviorSubject<string>(
    localStorage.getItem('namakam_selected_lang') || 'sanskrit'
  );

  currentLanguage$: Observable<string> = this.currentLangSubject.asObservable();

  constructor() {
    this.updateBodyDataLang(this.currentLanguage);
  }

  get currentLanguage(): string {
    return this.currentLangSubject.value;
  }

  setLanguage(code: string): void {
    const valid = this.languages.some(l => l.code === code);
    if (valid) {
      this.currentLangSubject.next(code);
      localStorage.setItem('namakam_selected_lang', code);
      this.updateBodyDataLang(code);
    }
  }

  private updateBodyDataLang(code: string): void {
    if (typeof document !== 'undefined' && document.body) {
      document.body.setAttribute('data-lang', code);
    }
  }

  transliterate(text: string, langCode?: string): string {
    if (!text) return '';
    const lang = langCode || this.currentLanguage;

    if (lang === 'sanskrit' || lang === 'hindi') {
      return text;
    }

    if (lang === 'english') {
      return this.toIAST(text);
    }

    if (lang === 'tamil') {
      return this.toTamil(text);
    }

    const offsets: { [key: string]: number } = {
      telugu: 0x0C00 - 0x0900,
      kannada: 0x0C80 - 0x0900,
      malayalam: 0x0D00 - 0x0900
    };

    const offset = offsets[lang];
    if (offset === undefined) return text;

    let result = '';
    for (let i = 0; i < text.length; i++) {
      const code = text.charCodeAt(i);

      // Preserve Danda | and || (0x0964, 0x0965)
      if (code === 0x0964 || code === 0x0965) {
        result += text[i];
        continue;
      }

      // Spacing Modifier Letters for Svara Accents in Indic Scripts
      // Prevents browser OpenType font engines from collapsing base consonants (e.g. namaste -> naste)
      // Preserve inline Vedic svara marks (Udatta 0x0951 and Anudatta 0x0952) for Indic scripts
      if (code === 0x0951 || code === 0x0952 || (code >= 0x1CD0 && code <= 0x1CF9)) {
        result += text[i];
      } else if (code >= 0x0901 && code <= 0x0963) {
        result += String.fromCharCode(code + offset);
      } else {
        result += text[i];
      }
    }
    return result;
  }

  private toIAST(text: string): string {
    const vowels: { [k: string]: string } = {
      'अ':'a','आ':'ā','इ':'i','ई':'ī','उ':'u','ऊ':'ū','ऋ':'ṛ','ॠ':'ṝ','ए':'e','ऐ':'ai','ओ':'o','औ':'au'
    };
    const matras: { [k: string]: string } = {
      'ा':'ā','ि':'i','ी':'ī','ु':'u','ू':'ū','ृ':'ṛ','ॄ':'ṝ','े':'e','ै':'ai','ो':'o','ौ':'au'
    };
    const consonants: { [k: string]: string } = {
      'क':'k','ख':'kh','ग':'g','घ':'gh','ङ':'ṅ',
      'च':'c','छ':'ch','ज':'j','झ':'jh','ञ':'ñ',
      'ट':'ṭ','ठ':'ṭh','ड':'ḍ','ढ':'ḍh','ण':'ṇ',
      'त':'t','थ':'th','द':'d','ध':'dh','न':'n',
      'प':'p','फ':'ph','ब':'b','भ':'bh','म':'m',
      'य':'y','र':'r','ल':'l','व':'v',
      'श':'ś','ष':'ṣ','स':'sa','ह':'h'
    };
    const others: { [k: string]: string } = {
      'ं':'ṁ', 'ः':'ḥ', 'ऽ':"'"
    };

    let out = '';
    let i = 0;
    while (i < text.length) {
      const char = text[i];
      const code = char.charCodeAt(0);

      // Vedic Svara Intonations (Combining Marks for elegant IAST typography)
      if (code === 0x0951) {
        out += '\u030D'; // Udatta: Combining Vertical Line Above (e.g. a̍)
        i++;
        continue;
      }
      if (code === 0x0952) {
        out += '\u0331'; // Anudatta: Combining Macron Below (e.g. a̱)
        i++;
        continue;
      }

      if (vowels[char]) {
        out += vowels[char];
        i++;
      } else if (consonants[char]) {
        let cons = consonants[char];
        if (char === 'स') cons = 's'; // Ensure clean s for sa
        const next = text[i + 1];
        if (next && matras[next]) {
          out += cons + matras[next];
          i += 2;
        } else if (next === '्') {
          out += cons;
          i += 2;
        } else {
          out += cons + 'a';
          i++;
        }
      } else if (others[char]) {
        out += others[char];
        i++;
      } else {
        out += char;
        i++;
      }
    }
    return out;
  }

  private toTamil(text: string): string {
    const tamilMap: { [k: string]: string } = {
      'अ':'அ','आ':'ஆ','इ':'இ','ई':'ஈ','उ':'உ','ऊ':'ஊ','ऋ':'ரு','ॠ':'ரூ','ए':'ஏ','ऐ':'ஐ','ओ':'ஒ','औ':'ஔ',
      'ा':'ா','ि':'ி','ी':'ீ','ु':'ு','ू':'ூ','ृ':'்ரு','े':'ே','ै':'ை','ो':'ொ','ौ':'ௌ','्':'்',
      'ं':'ம்','ः':'ஹ்',
      'क':'க','ख':'க','ग':'க','घ':'க','ङ':'ங',
      'च':'ச','छ':'ச','ज':'ஜ','झ':'ச','ञ':'ஞ',
      'ट':'ட','ठ':'ட','ड':'ட','ढ':'ட','ण':'ண',
      'त':'த','थ':'த','द':'த','ध':'த','न':'ந',
      'प':'ப','फ':'ப','ब':'ப','भ':'ப','म':'ம',
      'य':'ய','र':'ர','ल':'ல','व':'வ',
      'श':'ஶ','ष':'ஷ','स':'ஸ','ह':'ஹ'
    };

    let result = '';
    for (let i = 0; i < text.length; i++) {
      const char = text[i];
      const code = char.charCodeAt(0);

      if (code === 0x0964 || code === 0x0965) {
        result += text[i];
        continue;
      }
      if (code === 0x0951) {
        result += '\u02C8'; // Spacing Modifier Letter Vertical Line (Udatta)
      } else if (code === 0x0952) {
        result += '\u02CD'; // Spacing Modifier Letter Low Macron (Anudatta)
      } else if (code >= 0x1CD0 && code <= 0x1CF9) {
        result += char;
      } else if (tamilMap[char]) {
        result += tamilMap[char];
      } else {
        result += char;
      }
    }
    return result;
  }
}
