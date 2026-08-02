import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, shareReplay, map, firstValueFrom } from 'rxjs';

import anuvakam1 from '../anuvakam1.json';
import anuvakam2 from '../anuvakam2.json';
import anuvakam3 from '../anuvakam3.json';
import anuvakam4 from '../anuvakam4.json';
import anuvakam5 from '../anuvakam5.json';
import anuvakam6 from '../anuvakam6.json';
import anuvakam7 from '../anuvakam7.json';
import anuvakam8 from '../anuvakam8.json';
import anuvakam9 from '../anuvakam9.json';
import anuvakam10 from '../anuvakam10.json';
import anuvakam11 from '../anuvakam11.json';

// Original type exports for routing components
export interface PrefaceSection {
  sanskrit: string;
  english: string;
}

export interface Preface {
  rudradhyaya: PrefaceSection;
  rudrabhashya: PrefaceSection;
}

export interface CorrelatedMantra {
  id: number;
  youtubeUrl?: string;
  audioUrl?: string;
  sanskrit: {
    samhita: string;
    pada: string;
    krama: string;
  };
  sources: {
    rudradhyaya_page: string;
    rudrabhashya_page: string;
  };
  translations: {
    sayana: string;
    bhatta_bhaskara: string;
    abhinava_shankara: string;
  };
  commentaries_sanskrit: {
    abhinava_shankara: string;
  };
}

export interface CorrelatedAnuvakam {
  id: number;
  title: string;
  mantras: CorrelatedMantra[];
}

export interface CorrelatedData {
  introduction: Preface;
  anuvakas: CorrelatedAnuvakam[];
  conclusion: Preface;
}

export interface Token {
  text: string;
  word_ids: number[];
}

export interface CommentaryDetail {
  rishi?: string;
  chandas?: string;
  devata?: string;
  dhyana?: string;
  text: string;
  sanskrit: string;
}

export interface MantraWordAnalysis {
  anuvakam: number;
  title: string;
  id: number;
  samhita: string;
  pada: string;
  krama: string;
  youtubeUrl?: string;
  audioUrl?: string;
  commentaries: {
    sayana: CommentaryDetail;
    bhatta_bhaskara: CommentaryDetail;
    abhinava_shankara: CommentaryDetail;
  };
  samhita_tokens: Token[];
  pada_tokens: Token[];
  krama_tokens: Token[];
  words: number[];
}

export interface DictionaryEntry {
  id: number;
  pada_form: string;
  clean_form: string;
  meanings: {
    english: string;
    nirukta: string;
    vedantic: string;
  };
  grammatical_references: {
    panini: string[];
    case_ending: string;
  };
  lexicographical_references: {
    nighantu: string;
    amara_kosha: string;
    abhidhana_ratnamala: string;
  };
}

export interface Dictionary {
  [id: string]: DictionaryEntry;
}

export interface MantraRef {
  anuvakam: number;
  mantra: number;
}

export interface WordIndex {
  [wordId: string]: MantraRef[];
}

interface CombinedData {
  correlated: CorrelatedData;
  dictionary: Dictionary;
  wordIndex: WordIndex;
  mantras: { [key: string]: MantraWordAnalysis };
}

// New types for AnuvakamDisplayComponent
export interface Mantra {
  id: number;
  samhita: string;
  pada: string;
  krama: string;
  youtubeUrl?: string;
  audioUrl?: string;
}

export interface Anuvakam {
  anuvakam: number;
  title: string;
  mantras: Mantra[];
}

import { SanskritEditorService } from './sanskrit-editor.service';

@Injectable({
  providedIn: 'root'
})
export class NamakamService {
  private data$: Observable<CombinedData>;
  
  private anuvakams: Anuvakam[] = [
    anuvakam1, anuvakam2, anuvakam3, anuvakam4, anuvakam5,
    anuvakam6, anuvakam7, anuvakam8, anuvakam9, anuvakam10, anuvakam11
  ] as Anuvakam[];

  private sidebarCollapsed = localStorage.getItem('namakam_sidebar_collapsed') === 'true';

  constructor(
    private http: HttpClient,
    private editorService: SanskritEditorService
  ) {
    this.data$ = this.http.get<CombinedData>('assets/data.json').pipe(shareReplay(1));
  }

  isSidebarCollapsed(): boolean {
    return this.sidebarCollapsed;
  }

  toggleSidebarCollapsed(): boolean {
    this.sidebarCollapsed = !this.sidebarCollapsed;
    localStorage.setItem('namakam_sidebar_collapsed', String(this.sidebarCollapsed));
    return this.sidebarCollapsed;
  }

  getMantraPrefix(samhitaText: string): string {
    if (!samhitaText) return '';
    const cleaned = samhitaText.trim().replace(/[॥।=]/g, '').trim();
    const words = cleaned.split(/\s+/).filter(Boolean);
    if (words.length === 0) return '';
    const prefix = words.slice(0, 3).join(' ');
    return prefix.length > 28 ? prefix.substring(0, 28) + '…' : prefix + '…';
  }

  // Original methods for other routed components
  getAnuvakas(): Observable<CorrelatedAnuvakam[]> {
    return this.data$.pipe(
      map(d => {
        const anuvakas = JSON.parse(JSON.stringify(d.correlated.anuvakas)) as CorrelatedAnuvakam[];
        for (const a of anuvakas) {
          for (const m of a.mantras) {
            const raw = d.mantras[`${a.id}_${m.id}`];
            if (raw) {
              m.youtubeUrl = raw.youtubeUrl;
              m.audioUrl = raw.audioUrl;
            }
            const edit = this.editorService.getMantraEdit(a.id, m.id);
            if (edit) {
              if (edit.samhita !== undefined) m.sanskrit.samhita = edit.samhita;
              if (edit.pada !== undefined) m.sanskrit.pada = edit.pada;
              if (edit.krama !== undefined) m.sanskrit.krama = edit.krama;
            }
          }
        }
        return anuvakas;
      })
    );
  }

  getAnuvakam(id: number): Observable<CorrelatedAnuvakam | undefined> {
    return this.getAnuvakas().pipe(map(a => a.find(x => x.id === id)));
  }

  getMantra(anuvakamId: number, mantraId: number): Observable<CorrelatedMantra | undefined> {
    return this.getAnuvakam(anuvakamId).pipe(
      map(a => a?.mantras.find(m => m.id === mantraId))
    );
  }

  getIntroduction(): Observable<Preface> {
    return this.data$.pipe(map(d => d.correlated.introduction));
  }

  getConclusion(): Observable<Preface> {
    return this.data$.pipe(map(d => d.correlated.conclusion));
  }

  getMantraWordAnalysis(anuvakamId: number, mantraId: number): Observable<MantraWordAnalysis> {
    return this.data$.pipe(
      map(d => {
        const item = d.mantras[`${anuvakamId}_${mantraId}`];
        if (!item) return item;
        const copy = JSON.parse(JSON.stringify(item)) as MantraWordAnalysis;
        const edit = this.editorService.getMantraEdit(anuvakamId, mantraId);
        if (edit) {
          if (edit.samhita !== undefined) {
            copy.samhita = edit.samhita;
            copy.samhita_tokens = this.rebuildTokens(copy.samhita_tokens, edit.samhita);
          }
          if (edit.pada !== undefined) {
            copy.pada = edit.pada;
            copy.pada_tokens = this.rebuildTokens(copy.pada_tokens, edit.pada);
          }
          if (edit.krama !== undefined) {
            copy.krama = edit.krama;
            copy.krama_tokens = this.rebuildTokens(copy.krama_tokens, edit.krama);
          }
        }
        return copy;
      })
    );
  }

  getDictionary(): Observable<Dictionary> {
    return this.data$.pipe(map(d => d.dictionary));
  }

  getWordIndex(): Observable<WordIndex> {
    return this.data$.pipe(map(d => d.wordIndex));
  }

  // Methods for AnuvakamDisplayComponent & general views
  getAnuvakams(): Anuvakam[] {
    const copy = JSON.parse(JSON.stringify(this.anuvakams)) as Anuvakam[];
    for (const a of copy) {
      for (const m of a.mantras) {
        const edit = this.editorService.getMantraEdit(a.anuvakam, m.id);
        if (edit) {
          if (edit.samhita !== undefined) m.samhita = edit.samhita;
          if (edit.pada !== undefined) m.pada = edit.pada;
          if (edit.krama !== undefined) m.krama = edit.krama;
        }
      }
    }
    return copy;
  }

  async getCorrelatedData(): Promise<any> {
    const data = await firstValueFrom(this.data$);
    if (data?.correlated?.anuvakas) {
      const copy = JSON.parse(JSON.stringify(data.correlated));
      for (const a of copy.anuvakas) {
        for (const m of a.mantras) {
          const edit = this.editorService.getMantraEdit(a.id, m.id);
          if (edit) {
            if (edit.samhita !== undefined) m.sanskrit.samhita = edit.samhita;
            if (edit.pada !== undefined) m.sanskrit.pada = edit.pada;
            if (edit.krama !== undefined) m.sanskrit.krama = edit.krama;
          }
        }
      }
      return copy;
    }
    return null;
  }

  getMantraYoutubeUrl(anuvakamId: number, mantraId: number): string {
    const timestamps: Record<string, number> = {
      '1_1': 690, '1_2': 701, '1_3': 711, '1_4': 722, '1_5': 733,
      '1_6': 745, '1_7': 758, '1_8': 773, '1_9': 789, '1_10': 803,
      '1_11': 814, '1_12': 825, '1_13': 837, '1_14': 849, '1_15': 862,
      '2_1': 900, '2_2': 905, '2_3': 910, '2_4': 915, '2_5': 920,
      '2_6': 926, '2_7': 932, '2_8': 936, '2_9': 941, '2_10': 948,
      '2_11': 953, '2_12': 961, '2_13': 965,
      '3_1': 976, '3_2': 985, '3_3': 992, '3_4': 998, '3_5': 1004,
      '3_6': 1011, '3_7': 1015, '3_8': 1021, '3_9': 1025, '3_10': 1030,
      '3_11': 1035, '3_12': 1040, '3_13': 1045, '3_14': 1050, '3_15': 1055,
      '3_16': 1060, '3_17': 1065,
      '4_1': 1070, '4_2': 1076, '4_3': 1082, '4_4': 1088, '4_5': 1094,
      '4_6': 1100, '4_7': 1106, '4_8': 1112, '4_9': 1118, '4_10': 1124,
      '4_11': 1130, '4_12': 1136, '4_13': 1142, '4_14': 1149, '4_15': 1155,
      '4_16': 1161, '4_17': 1167,
      '5_1': 1174, '5_2': 1180, '5_3': 1186, '5_4': 1192, '5_5': 1198,
      '5_6': 1204, '5_7': 1210, '5_8': 1216, '5_9': 1222, '5_10': 1228,
      '5_11': 1234, '5_12': 1240, '5_13': 1246, '5_14': 1252, '5_15': 1258,
      '6_1': 1265, '6_2': 1271, '6_3': 1277, '6_4': 1284, '6_5': 1290,
      '6_6': 1296, '6_7': 1302, '6_8': 1308, '6_9': 1314, '6_10': 1320,
      '6_11': 1326, '6_12': 1332, '6_13': 1338, '6_14': 1344, '6_15': 1350,
      '7_1': 1354, '7_2': 1360, '7_3': 1366, '7_4': 1372, '7_5': 1378,
      '7_6': 1384, '7_7': 1390, '7_8': 1396, '7_9': 1402, '7_10': 1408,
      '7_11': 1414, '7_12': 1420, '7_13': 1426, '7_14': 1432, '7_15': 1438,
      '7_16': 1444,
      '8_1': 1450, '8_2': 1456, '8_3': 1462, '8_4': 1468, '8_5': 1474,
      '8_6': 1480, '8_7': 1486, '8_8': 1492, '8_9': 1498, '8_10': 1504,
      '8_11': 1510, '8_12': 1516, '8_13': 1522, '8_14': 1528, '8_15': 1534,
      '8_16': 1540, '8_17': 1546,
      '9_1': 1552, '9_2': 1558, '9_3': 1564, '9_4': 1570, '9_5': 1576,
      '9_6': 1582, '9_7': 1588, '9_8': 1594, '9_9': 1600, '9_10': 1606,
      '9_11': 1612, '9_12': 1618, '9_13': 1624, '9_14': 1630, '9_15': 1636,
      '9_16': 1642, '9_17': 1650,
      '10_1': 1658, '10_2': 1672, '10_3': 1686, '10_4': 1700, '10_5': 1714,
      '10_6': 1728, '10_7': 1742, '10_8': 1756, '10_9': 1770, '10_10': 1784,
      '10_11': 1798, '10_12': 1812,
      '11_1': 1820, '11_2': 1826, '11_3': 1831, '11_4': 1835, '11_5': 1840,
      '11_6': 1845, '11_7': 1850, '11_8': 1855, '11_9': 1860, '11_10': 1866
    };
    const key = `${anuvakamId}_${mantraId}`;
    const sec = timestamps[key] || 685;
    return `https://www.youtube.com/watch?v=OQhyYdoKW1k&t=${sec}s`;
  }

  getMantraAudioUrl(anuvakamId: number, mantraId: number): string {
    return `assets/audio/mantra_${anuvakamId}_${mantraId}.mp3`;
  }

  getGlobalDictionary(): Promise<any> {
    return firstValueFrom(this.data$.pipe(map(d => d.dictionary)));
  }

  async getMantraDetails(anuvakamNum: number, mantraId: number): Promise<any> {
    const data = await firstValueFrom(this.data$);
    const key = `${anuvakamNum}_${mantraId}`;
    const details = data?.mantras ? data.mantras[key] : null;
    if (details) {
      const copy = JSON.parse(JSON.stringify(details));
      const edit = this.editorService.getMantraEdit(anuvakamNum, mantraId);
      if (edit) {
        if (edit.samhita !== undefined) {
          copy.samhita = edit.samhita;
          copy.samhita_tokens = this.rebuildTokens(copy.samhita_tokens, edit.samhita);
        }
        if (edit.pada !== undefined) {
          copy.pada = edit.pada;
          copy.pada_tokens = this.rebuildTokens(copy.pada_tokens, edit.pada);
        }
        if (edit.krama !== undefined) {
          copy.krama = edit.krama;
          copy.krama_tokens = this.rebuildTokens(copy.krama_tokens, edit.krama);
        }
      }
      return copy;
    }
    // Fallback HTTP request
    try {
      const httpDetails = await firstValueFrom(this.http.get<any>(`assets/word_analysis/anuvakam${anuvakamNum}/mantra${mantraId}.json`));
      if (httpDetails) {
        const edit = this.editorService.getMantraEdit(anuvakamNum, mantraId);
        if (edit) {
          if (edit.samhita !== undefined) {
            httpDetails.samhita = edit.samhita;
            httpDetails.samhita_tokens = this.rebuildTokens(httpDetails.samhita_tokens, edit.samhita);
          }
          if (edit.pada !== undefined) {
            httpDetails.pada = edit.pada;
            httpDetails.pada_tokens = this.rebuildTokens(httpDetails.pada_tokens, edit.pada);
          }
          if (edit.krama !== undefined) {
            httpDetails.krama = edit.krama;
            httpDetails.krama_tokens = this.rebuildTokens(httpDetails.krama_tokens, edit.krama);
          }
        }
      }
      return httpDetails;
    } catch {
      return null;
    }
  }

  private rebuildTokens(originalTokens: Token[], newText: string): Token[] {
    if (!newText) return [];
    if (!originalTokens || originalTokens.length === 0) {
      const parts = newText.split(/(\s+|[=()।॥])/g).filter(p => p.length > 0);
      return parts.map(p => ({ text: p, word_ids: [] }));
    }

    const cleanSanskrit = (t: string) => (t || '').replace(/[\u0951\u0952\u1CD0-\u1CFF]/g, '').trim();

    const normalizeForMatching = (t: string) => {
      let clean = cleanSanskrit(t);
      // Strip Padapatha iti suffixes (like नीत्य, नीति, इति, इत्य, इते)
      clean = clean.replace(/(नीत्य|नीति|इति|इ॒ति|इ॑ति|इत्य|इ॒त्य|इ॑त्य|-|=|\s|ऽ|॥|\||\(|\))/g, '');
      return clean
        .replace(/[ाीूेैोौ]/g, '') // Normalize vowel length matras for robust matching
        .replace(/म्$/, 'म')
        .replace(/ः$/, '')
        .trim();
    };

    const levenshtein = (a: string, b: string): number => {
      if (!a || !b) return Math.max((a || '').length, (b || '').length);
      const m: number[][] = [];
      for (let i = 0; i <= b.length; i++) m[i] = [i];
      for (let j = 0; j <= a.length; j++) m[0][j] = j;
      for (let i = 1; i <= b.length; i++) {
        for (let j = 1; j <= a.length; j++) {
          m[i][j] = b.charAt(i - 1) === a.charAt(j - 1)
            ? m[i - 1][j - 1]
            : Math.min(m[i - 1][j - 1] + 1, m[i][j - 1] + 1, m[i - 1][j] + 1);
        }
      }
      return m[b.length][a.length];
    };

    // Extract original non-empty, non-punctuation word tokens
    const originalWords = originalTokens.filter(t => {
      const clean = cleanSanskrit(t.text);
      return clean.length > 0 && !/^[=()।॥\s]+$/.test(clean);
    });

    // Split newText into words, whitespace, and punctuation
    const newParts = newText.split(/(\s+|[=()।॥])/g).filter(p => p.length > 0);

    let wordIdx = 0;

    return newParts.map((part, pIdx) => {
      const cleanPart = cleanSanskrit(part);
      const normPart = normalizeForMatching(part);

      // If whitespace or punctuation, no word_ids
      if (!cleanPart || /^[=()।॥\s]+$/.test(part)) {
        return {
          text: part,
          word_ids: []
        };
      }

      let assignedIds: number[] = [];

      if (wordIdx < originalWords.length) {
        let bestMatchIdx = -1;

        // 1. Search window starting from current wordIdx
        for (let w = wordIdx; w <= Math.min(originalWords.length - 1, wordIdx + 5); w++) {
          const candNorm = normalizeForMatching(originalWords[w].text);
          if (!candNorm || !normPart) continue;

          const minLen = Math.min(normPart.length, candNorm.length);
          if (
            normPart === candNorm ||
            (minLen >= 2 && (normPart.includes(candNorm) || candNorm.includes(normPart))) ||
            (normPart.length >= 3 && candNorm.length >= 3 && (normPart.startsWith(candNorm.slice(0, 3)) || candNorm.startsWith(normPart.slice(0, 3)))) ||
            (minLen >= 3 && levenshtein(normPart, candNorm) <= 2)
          ) {
            bestMatchIdx = w;
            break;
          }
        }

        // 2. Fallback: search window around wordIdx
        if (bestMatchIdx === -1 && wordIdx > 0) {
          for (let w = Math.max(0, wordIdx - 2); w <= Math.min(originalWords.length - 1, wordIdx + 5); w++) {
            const candNorm = normalizeForMatching(originalWords[w].text);
            if (!candNorm || !normPart) continue;

            const minLen = Math.min(normPart.length, candNorm.length);
            if (
              normPart === candNorm ||
              (minLen >= 2 && (normPart.includes(candNorm) || candNorm.includes(normPart))) ||
              (minLen >= 3 && levenshtein(normPart, candNorm) <= 2)
            ) {
              bestMatchIdx = w;
              break;
            }
          }
        }

        if (bestMatchIdx !== -1) {
          assignedIds = [...(originalWords[bestMatchIdx].word_ids || [])];
          wordIdx = bestMatchIdx + 1;
        } else {
          assignedIds = [];
        }
      }

      return {
        text: part,
        word_ids: assignedIds
      };
    });
  }
}
