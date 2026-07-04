import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, shareReplay, map } from 'rxjs';

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

@Injectable({
  providedIn: 'root'
})
export class NamakamService {
  private data$: Observable<CombinedData>;

  constructor(private http: HttpClient) {
    this.data$ = this.http.get<CombinedData>('assets/data.json').pipe(shareReplay(1));
  }

  getAnuvakas(): Observable<CorrelatedAnuvakam[]> {
    return this.data$.pipe(map(d => d.correlated.anuvakas));
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
    return this.data$.pipe(map(d => d.mantras[`${anuvakamId}_${mantraId}`]));
  }

  getDictionary(): Observable<Dictionary> {
    return this.data$.pipe(map(d => d.dictionary));
  }

  getWordIndex(): Observable<WordIndex> {
    return this.data$.pipe(map(d => d.wordIndex));
  }
}
