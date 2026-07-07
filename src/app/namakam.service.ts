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

@Injectable({
  providedIn: 'root'
})
export class NamakamService {
  private data$: Observable<CombinedData>;
  
  private anuvakams: Anuvakam[] = [
    anuvakam1, anuvakam2, anuvakam3, anuvakam4, anuvakam5,
    anuvakam6, anuvakam7, anuvakam8, anuvakam9, anuvakam10, anuvakam11
  ] as Anuvakam[];

  constructor(private http: HttpClient) {
    this.data$ = this.http.get<CombinedData>('assets/data.json').pipe(shareReplay(1));
  }

  // Original methods for other routed components
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

  // New methods for AnuvakamDisplayComponent
  getAnuvakams(): Anuvakam[] {
    return this.anuvakams;
  }

  getCorrelatedData(): Promise<any> {
    return firstValueFrom(this.http.get('assets/correlated_namakam.json'));
  }

  getGlobalDictionary(): Promise<any> {
    return firstValueFrom(this.http.get('assets/word_analysis/global_dictionary.json'));
  }

  getMantraDetails(anuvakamNum: number, mantraId: number): Promise<any> {
    return firstValueFrom(this.http.get(`assets/word_analysis/anuvakam${anuvakamNum}/mantra${mantraId}.json`));
  }
}
