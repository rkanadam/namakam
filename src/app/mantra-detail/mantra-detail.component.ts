import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { forkJoin } from 'rxjs';
import {
  NamakamService,
  MantraWordAnalysis,
  Dictionary,
  DictionaryEntry,
  Token,
  CorrelatedMantra
} from '../namakam.service';

@Component({
  selector: 'app-mantra-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './mantra-detail.component.html',
  styleUrls: ['./mantra-detail.component.css']
})
export class MantraDetailComponent implements OnInit, OnDestroy {
  anuvakamId = 0;
  mantraId = 0;
  wordAnalysis: MantraWordAnalysis | null = null;
  correlatedMantra: CorrelatedMantra | undefined;
  dictionary: Dictionary = {};
  selectedWord: DictionaryEntry | null = null;
  activePathaTab: 'samhita' | 'pada' | 'krama' = 'samhita';
  activeCommentaryTab: 'sayana' | 'bhatta_bhaskara' | 'abhinava_shankara' = 'sayana';
  activeCommentaryLang: 'sanskrit' | 'english' = 'english';

  hoveredWord: DictionaryEntry | null = null;
  hoveredWordIds: Set<number> = new Set();
  tooltipX = 0;
  tooltipY = 0;
  tooltipPosition: 'above' | 'below' = 'above';
  tooltipVisible = false;
  private hideTimeout: any = null;

  constructor(
    private route: ActivatedRoute,
    private namakamService: NamakamService
  ) {}

  ngOnInit(): void {
    this.anuvakamId = Number(this.route.snapshot.paramMap.get('anuvakamId'));
    this.mantraId = Number(this.route.snapshot.paramMap.get('mantraId'));

    this.namakamService.getMantra(this.anuvakamId, this.mantraId)
      .subscribe(m => this.correlatedMantra = m);

    forkJoin({
      wordAnalysis: this.namakamService.getMantraWordAnalysis(this.anuvakamId, this.mantraId),
      dictionary: this.namakamService.getDictionary()
    }).subscribe(({ wordAnalysis, dictionary }) => {
      this.wordAnalysis = wordAnalysis;
      this.dictionary = dictionary;
    });
  }

  ngOnDestroy(): void {
    if (this.hideTimeout) clearTimeout(this.hideTimeout);
  }

  get currentTokens(): Token[] {
    if (!this.wordAnalysis) return [];
    switch (this.activePathaTab) {
      case 'samhita': return this.wordAnalysis.samhita_tokens;
      case 'pada': return this.wordAnalysis.pada_tokens;
      case 'krama': return this.wordAnalysis.krama_tokens;
    }
  }

  isClickable(token: Token): boolean {
    return token.word_ids && token.word_ids.length > 0;
  }

  onTokenClick(token: Token): void {
    if (!this.isClickable(token)) return;
    const firstId = token.word_ids[0];
    const entry = this.dictionary[String(firstId)];
    if (entry) {
      this.selectedWord = this.selectedWord?.id === entry.id ? null : entry;
    }
  }

  isTokenSelected(token: Token): boolean {
    if (!this.selectedWord || !token.word_ids?.length) return false;
    return token.word_ids.includes(this.selectedWord.id);
  }

  isSiblingHighlighted(token: Token): boolean {
    if (!this.hoveredWord || !token.word_ids?.length) return false;
    return token.word_ids.some(id => this.hoveredWordIds.has(id));
  }

  onTokenMouseEnter(event: MouseEvent, token: Token): void {
    if (!this.isClickable(token)) return;
    if (this.hideTimeout) {
      clearTimeout(this.hideTimeout);
      this.hideTimeout = null;
    }
    const entry = this.dictionary[String(token.word_ids[0])];
    if (entry) {
      this.hoveredWord = entry;
      this.hoveredWordIds = new Set(token.word_ids);
      const rect = (event.target as HTMLElement).getBoundingClientRect();
      this.tooltipX = rect.left + rect.width / 2;
      const spaceAbove = rect.top;
      const spaceBelow = window.innerHeight - rect.bottom;
      if (spaceAbove > 200 || spaceAbove > spaceBelow) {
        this.tooltipPosition = 'above';
        this.tooltipY = rect.top;
      } else {
        this.tooltipPosition = 'below';
        this.tooltipY = rect.bottom;
      }
      this.tooltipVisible = true;
    }
  }

  onTokenMouseLeave(): void {
    this.scheduleHide();
  }

  onTooltipMouseEnter(): void {
    if (this.hideTimeout) {
      clearTimeout(this.hideTimeout);
      this.hideTimeout = null;
    }
  }

  onTooltipMouseLeave(): void {
    this.scheduleHide();
  }

  private scheduleHide(): void {
    if (this.hideTimeout) clearTimeout(this.hideTimeout);
    this.hideTimeout = setTimeout(() => {
      this.tooltipVisible = false;
      this.hoveredWord = null;
      this.hoveredWordIds = new Set();
    }, 200);
  }

  closeWordPanel(): void {
    this.selectedWord = null;
  }

  get commentaryData() {
    return this.wordAnalysis?.commentaries;
  }

  get currentCommentary() {
    return this.commentaryData?.[this.activeCommentaryTab];
  }

  hasCommentaryContent(key: string): boolean {
    const c = this.commentaryData?.[key as keyof typeof this.commentaryData];
    return !!(c?.text || c?.sanskrit);
  }
}
