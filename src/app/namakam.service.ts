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
