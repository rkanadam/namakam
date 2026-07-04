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

@Injectable({
  providedIn: 'root'
})
export class NamakamService {
  private correlatedData$: Observable<CorrelatedData> | null = null;
  private dictionary$: Observable<Dictionary> | null = null;
  private wordIndex$: Observable<WordIndex> | null = null;

  constructor(private http: HttpClient) {}

  private getCorrelatedData(): Observable<CorrelatedData> {
    if (!this.correlatedData$) {
      this.correlatedData$ = this.http.get<CorrelatedData>(
        'assets/correlated_namakam.json'
      ).pipe(shareReplay(1));
    }
    return this.correlatedData$;
  }

  getAnuvakas(): Observable<CorrelatedAnuvakam[]> {
    return this.getCorrelatedData().pipe(map(d => d.anuvakas));
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
    return this.getCorrelatedData().pipe(map(d => d.introduction));
  }

  getConclusion(): Observable<Preface> {
    return this.getCorrelatedData().pipe(map(d => d.conclusion));
  }

  getMantraWordAnalysis(anuvakamId: number, mantraId: number): Observable<MantraWordAnalysis> {
    return this.http.get<MantraWordAnalysis>(
      `assets/word_analysis/anuvakam${anuvakamId}/mantra${mantraId}.json`
    );
  }

  getDictionary(): Observable<Dictionary> {
    if (!this.dictionary$) {
      this.dictionary$ = this.http.get<Dictionary>(
        'assets/word_analysis/global_dictionary.json'
      ).pipe(shareReplay(1));
    }
    return this.dictionary$;
  }

  getWordIndex(): Observable<WordIndex> {
    if (!this.wordIndex$) {
      this.wordIndex$ = this.http.get<WordIndex>(
        'assets/word_analysis/word_index.json'
      ).pipe(shareReplay(1));
    }
    return this.wordIndex$;
  }
}
