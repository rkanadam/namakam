import { Component, OnInit, OnDestroy, HostListener } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { forkJoin } from 'rxjs';
import {
  NamakamService,
  MantraWordAnalysis,
  Dictionary,
  DictionaryEntry,
  Token,
  CorrelatedMantra,
  Anuvakam,
  Mantra
} from '../namakam.service';

import { SanskritEditorModalComponent } from '../sanskrit-editor-modal/sanskrit-editor-modal.component';
import { SanskritEditorService } from '../sanskrit-editor.service';

@Component({
  selector: 'app-mantra-detail',
  standalone: true,
  imports: [CommonModule, RouterLink, SanskritEditorModalComponent],
  templateUrl: './mantra-detail.component.html',
  styleUrls: ['./mantra-detail.component.css']
})
export class MantraDetailComponent implements OnInit, OnDestroy {
  anuvakamId = 0;
  mantraId = 0;
  anuvakams: Anuvakam[] = [];
  expandedAnuvakams: { [key: number]: boolean } = {};

  wordAnalysis: MantraWordAnalysis | null = null;
  correlatedMantra: CorrelatedMantra | undefined;
  dictionary: Dictionary = {};
  selectedWord: DictionaryEntry | null = null;
  activePathaTab: 'samhita' | 'pada' | 'krama' = 'samhita';
  activeCommentaryTab: 'sayana' | 'bhatta_bhaskara' | 'abhinava_shankara' = 'sayana';
  activeCommentaryLang: 'sanskrit' | 'english' = 'english';

  showEditorModal = false;

  hoveredWord: DictionaryEntry | null = null;
  hoveredWordIds: Set<number> = new Set();
  tooltipX = 0;
  tooltipY = 0;
  tooltipPosition: 'above' | 'below' = 'above';
  tooltipVisible = false;
  private hideTimeout: any = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private namakamService: NamakamService,
    private editorService: SanskritEditorService
  ) {}

  ngOnInit(): void {
    this.anuvakams = this.namakamService.getAnuvakams();
    this.route.paramMap.subscribe(params => {
      this.anuvakamId = Number(params.get('anuvakamId'));
      this.mantraId = Number(params.get('mantraId'));
      this.expandedAnuvakams[this.anuvakamId] = true;
      this.loadData();
    });
  }

  isAnuvakamExpanded(id: number): boolean {
    if (this.expandedAnuvakams[id] === undefined) {
      return this.anuvakamId === id;
    }
    return !!this.expandedAnuvakams[id];
  }

  toggleAnuvakamExpand(id: number, event?: Event): void {
    if (event) event.stopPropagation();
    this.expandedAnuvakams[id] = !this.isAnuvakamExpanded(id);
  }

  getPrevMantraInfo(): { anuvakamId: number; mantraId: number } | null {
    if (!this.anuvakams.length) return null;
    const currentAnv = this.anuvakams.find(a => a.anuvakam === this.anuvakamId);
    if (!currentAnv) return null;
    const currentMantraIdx = currentAnv.mantras.findIndex(m => m.id === this.mantraId);
    if (currentMantraIdx > 0) {
      return {
        anuvakamId: this.anuvakamId,
        mantraId: currentAnv.mantras[currentMantraIdx - 1].id
      };
    }
    const currentAnvIdx = this.anuvakams.findIndex(a => a.anuvakam === this.anuvakamId);
    if (currentAnvIdx > 0) {
      const prevAnv = this.anuvakams[currentAnvIdx - 1];
      if (prevAnv.mantras && prevAnv.mantras.length > 0) {
        return {
          anuvakamId: prevAnv.anuvakam,
          mantraId: prevAnv.mantras[prevAnv.mantras.length - 1].id
        };
      }
    }
    return null;
  }

  getNextMantraInfo(): { anuvakamId: number; mantraId: number } | null {
    if (!this.anuvakams.length) return null;
    const currentAnv = this.anuvakams.find(a => a.anuvakam === this.anuvakamId);
    if (!currentAnv) return null;
    const currentMantraIdx = currentAnv.mantras.findIndex(m => m.id === this.mantraId);
    if (currentMantraIdx >= 0 && currentMantraIdx < currentAnv.mantras.length - 1) {
      return {
        anuvakamId: this.anuvakamId,
        mantraId: currentAnv.mantras[currentMantraIdx + 1].id
      };
    }
    const currentAnvIdx = this.anuvakams.findIndex(a => a.anuvakam === this.anuvakamId);
    if (currentAnvIdx >= 0 && currentAnvIdx < this.anuvakams.length - 1) {
      const nextAnv = this.anuvakams[currentAnvIdx + 1];
      if (nextAnv.mantras && nextAnv.mantras.length > 0) {
        return {
          anuvakamId: nextAnv.anuvakam,
          mantraId: nextAnv.mantras[0].id
        };
      }
    }
    return null;
  }

  goToPreviousMantra(): void {
    const prev = this.getPrevMantraInfo();
    if (prev) {
      this.router.navigate(['/anuvakam', prev.anuvakamId, 'mantra', prev.mantraId]);
    }
  }

  goToNextMantra(): void {
    const next = this.getNextMantraInfo();
    if (next) {
      this.router.navigate(['/anuvakam', next.anuvakamId, 'mantra', next.mantraId]);
    }
  }

  selectIntro(): void {
    this.router.navigate(['/introduction']);
  }

  selectConclusion(): void {
    this.router.navigate(['/conclusion']);
  }

  selectWordIndex(): void {
    this.router.navigate(['/word-index']);
  }

  selectAnuvakam(anuvakamId: number): void {
    this.router.navigate(['/anuvakam', anuvakamId]);
  }

  selectMantraFromSidebar(anuvakamId: number, mantraId: number): void {
    this.router.navigate(['/anuvakam', anuvakamId, 'mantra', mantraId]);
  }

  @HostListener('window:keydown', ['$event'])
  handleKeyboardEvent(event: KeyboardEvent): void {
    if (this.showEditorModal) return;
    const activeEl = document.activeElement;
    if (activeEl && (activeEl.tagName === 'INPUT' || activeEl.tagName === 'TEXTAREA' || activeEl.getAttribute('contenteditable') === 'true')) {
      return;
    }
    if (event.key === 'ArrowLeft' && this.getPrevMantraInfo()) {
      event.preventDefault();
      this.goToPreviousMantra();
    } else if (event.key === 'ArrowRight' && this.getNextMantraInfo()) {
      event.preventDefault();
      this.goToNextMantra();
    }
  }

  loadData(): void {
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

  get isEditorEnabled(): boolean {
    return this.editorService.isEditorEnabled();
  }

  openEditor(): void {
    this.showEditorModal = true;
  }

  closeEditor(): void {
    this.showEditorModal = false;
  }

  onEditorSaved(): void {
    this.showEditorModal = false;
    this.loadData();
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
