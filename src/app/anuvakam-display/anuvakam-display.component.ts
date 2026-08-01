import { Component, OnInit, HostListener } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { NamakamService, Anuvakam, Mantra } from '../namakam.service';
import { SanskritEditorService } from '../sanskrit-editor.service';
import { SanskritEditorModalComponent } from '../sanskrit-editor-modal/sanskrit-editor-modal.component';
import { ScriptTransliteratePipe } from '../script-transliterate.pipe';
import { ScriptTransliterationService } from '../script-transliteration.service';

interface WordDetails {
  id: number;
  pada_form: string;
  clean_form: string;
  meanings?: { english?: string; nirukta?: string; vedantic?: string };
  grammatical_references?: { panini?: string[] | string; case_ending?: string };
  lexicographical_references?: { nighantu?: string; amara_kosha?: string; abhidhana_ratnamala?: string };
}

@Component({
  selector: 'app-anuvakam-display',
  standalone: true,
  imports: [CommonModule, SanskritEditorModalComponent, ScriptTransliteratePipe, RouterLink],
  templateUrl: './anuvakam-display.component.html',
  styleUrls: ['./anuvakam-display.component.css']
})
export class AnuvakamDisplayComponent implements OnInit {
  // Navigation states
  anuvakams: Anuvakam[] = [];
  selectedAnuvakam: Anuvakam | null = null;
  activeView: 'intro' | 'anuvakam' | 'conclusion' = 'intro';
  
  // Prefix/Postfix Commentaries
  correlatedData: any = null;
  activeIntroTab: 'rudradhyaya' | 'rudrabhashya' = 'rudradhyaya';
  activeConclusionTab: 'rudradhyaya' | 'rudrabhashya' = 'rudradhyaya';
  introLang: 'sanskrit' | 'english' = 'english';
  conclusionLang: 'sanskrit' | 'english' = 'english';

  // Mantra Details
  selectedMantra: any = null;
  selectedMantraDetails: any = null;
  activeMantraTab: 'samhita' | 'pada' | 'krama' = 'samhita';
  activeCommentator: 'sayana' | 'bhatta_bhaskara' | 'abhinava_shankara' = 'sayana';
  commentaryLang: 'sanskrit' | 'english' = 'english';
  loadingMantra: boolean = false;

  // Editor Modal State
  showEditorModal: boolean = false;

  // Dictionary Hover State
  globalDictionary: { [key: string]: WordDetails } = {};
  hoveredWords: WordDetails[] = [];
  dictionaryLoaded: boolean = false;

  constructor(
    private namakamService: NamakamService,
    private editorService: SanskritEditorService,
    private transliterationService: ScriptTransliterationService
  ) {}

  get selectedLanguage(): string {
    return this.transliterationService.currentLanguage;
  }

  onLanguageChange(event: Event): void {
    const select = event.target as HTMLSelectElement;
    this.transliterationService.setLanguage(select.value);
  }

  async ngOnInit(): Promise<void> {
    // Load basic list
    this.anuvakams = this.namakamService.getAnuvakams();
    
    // Load prefix/postfix commentaries
    try {
      this.correlatedData = await this.namakamService.getCorrelatedData();
    } catch (e) {
      console.error("Error loading commentaries:", e);
    }

    // Load global dictionary in background
    try {
      this.globalDictionary = await this.namakamService.getGlobalDictionary();
      this.dictionaryLoaded = true;
    } catch (e) {
      console.error("Error loading global dictionary:", e);
    }
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
    this.anuvakams = this.namakamService.getAnuvakams();
    if (this.selectedMantra) {
      this.selectMantra(this.selectedMantra);
    }
  }

  // Sidebar Collapse State
  isSidebarCollapsed(): boolean {
    return this.namakamService.isSidebarCollapsed();
  }

  toggleSidebar(): void {
    this.namakamService.toggleSidebarCollapsed();
  }

  getMantraPrefix(text: string): string {
    return this.namakamService.getMantraPrefix(text);
  }

  // Sidebar Mantra Expansion State
  expandedAnuvakams: { [key: number]: boolean } = {};

  isAnuvakamExpanded(anuvakamId: number): boolean {
    if (this.expandedAnuvakams[anuvakamId] === undefined) {
      return this.selectedAnuvakam?.anuvakam === anuvakamId;
    }
    return !!this.expandedAnuvakams[anuvakamId];
  }

  toggleAnuvakamExpand(anuvakamId: number, event?: Event): void {
    if (event) event.stopPropagation();
    this.expandedAnuvakams[anuvakamId] = !this.isAnuvakamExpanded(anuvakamId);
  }

  selectIntro(): void {
    this.activeView = 'intro';
    this.selectedAnuvakam = null;
    this.selectedMantra = null;
    this.selectedMantraDetails = null;
  }

  selectConclusion(): void {
    this.activeView = 'conclusion';
    this.selectedAnuvakam = null;
    this.selectedMantra = null;
    this.selectedMantraDetails = null;
  }

  selectAnuvakam(anuvakam: Anuvakam): void {
    this.activeView = 'anuvakam';
    this.selectedAnuvakam = anuvakam;
    this.expandedAnuvakams[anuvakam.anuvakam] = true;
    this.selectedMantra = null;
    this.selectedMantraDetails = null;
  }

  selectMantraFromSidebar(anuvakam: Anuvakam, mantra: Mantra): void {
    this.activeView = 'anuvakam';
    this.selectedAnuvakam = anuvakam;
    this.expandedAnuvakams[anuvakam.anuvakam] = true;
    this.selectMantra(mantra);
  }

  getPrevMantraInfo(): { anuvakam: Anuvakam; mantra: Mantra } | null {
    if (!this.selectedAnuvakam || !this.selectedMantra) return null;
    const currentMantraIdx = this.selectedAnuvakam.mantras.findIndex(m => m.id === this.selectedMantra.id);
    if (currentMantraIdx > 0) {
      return {
        anuvakam: this.selectedAnuvakam,
        mantra: this.selectedAnuvakam.mantras[currentMantraIdx - 1]
      };
    }
    const currentAnvIdx = this.anuvakams.findIndex(a => a.anuvakam === this.selectedAnuvakam?.anuvakam);
    if (currentAnvIdx > 0) {
      const prevAnv = this.anuvakams[currentAnvIdx - 1];
      if (prevAnv.mantras && prevAnv.mantras.length > 0) {
        return {
          anuvakam: prevAnv,
          mantra: prevAnv.mantras[prevAnv.mantras.length - 1]
        };
      }
    }
    return null;
  }

  getNextMantraInfo(): { anuvakam: Anuvakam; mantra: Mantra } | null {
    if (!this.selectedAnuvakam || !this.selectedMantra) return null;
    const currentMantraIdx = this.selectedAnuvakam.mantras.findIndex(m => m.id === this.selectedMantra.id);
    if (currentMantraIdx >= 0 && currentMantraIdx < this.selectedAnuvakam.mantras.length - 1) {
      return {
        anuvakam: this.selectedAnuvakam,
        mantra: this.selectedAnuvakam.mantras[currentMantraIdx + 1]
      };
    }
    const currentAnvIdx = this.anuvakams.findIndex(a => a.anuvakam === this.selectedAnuvakam?.anuvakam);
    if (currentAnvIdx >= 0 && currentAnvIdx < this.anuvakams.length - 1) {
      const nextAnv = this.anuvakams[currentAnvIdx + 1];
      if (nextAnv.mantras && nextAnv.mantras.length > 0) {
        return {
          anuvakam: nextAnv,
          mantra: nextAnv.mantras[0]
        };
      }
    }
    return null;
  }

  goToPreviousMantra(): void {
    const prev = this.getPrevMantraInfo();
    if (prev) {
      this.activeView = 'anuvakam';
      this.selectedAnuvakam = prev.anuvakam;
      this.expandedAnuvakams[prev.anuvakam.anuvakam] = true;
      this.selectMantra(prev.mantra);
    }
  }

  goToNextMantra(): void {
    const next = this.getNextMantraInfo();
    if (next) {
      this.activeView = 'anuvakam';
      this.selectedAnuvakam = next.anuvakam;
      this.expandedAnuvakams[next.anuvakam.anuvakam] = true;
      this.selectMantra(next.mantra);
    }
  }

  @HostListener('window:keydown', ['$event'])
  handleKeyboardEvent(event: KeyboardEvent): void {
    if (this.showEditorModal) return;
    const activeEl = document.activeElement;
    if (activeEl && (activeEl.tagName === 'INPUT' || activeEl.tagName === 'TEXTAREA' || activeEl.getAttribute('contenteditable') === 'true')) {
      return;
    }
    if (this.activeView === 'anuvakam' && this.selectedMantra) {
      if (event.key === 'ArrowLeft') {
        if (this.getPrevMantraInfo()) {
          event.preventDefault();
          this.goToPreviousMantra();
        }
      } else if (event.key === 'ArrowRight') {
        if (this.getNextMantraInfo()) {
          event.preventDefault();
          this.goToNextMantra();
        }
      }
    }
  }

  async selectMantra(mantra: Mantra): Promise<void> {
    if (!this.selectedAnuvakam) return;
    this.selectedMantra = mantra;
    this.selectedMantraDetails = null;
    this.loadingMantra = true;

    try {
      this.selectedMantraDetails = await this.namakamService.getMantraDetails(
        this.selectedAnuvakam.anuvakam,
        mantra.id
      );
      this.activeMantraTab = 'samhita';
      // Default to sayana if available, otherwise abhinava_shankara
      if (this.selectedMantraDetails.commentaries?.sayana?.english) {
        this.activeCommentator = 'sayana';
      } else {
        this.activeCommentator = 'abhinava_shankara';
      }
      this.commentaryLang = 'english';
    } catch (e) {
      console.error("Error loading mantra details:", e);
    } finally {
      this.loadingMantra = false;
    }
  }

  // Get active tokens based on current tab selection
  get activeTokens(): any[] {
    if (!this.selectedMantraDetails) return [];
    if (this.activeMantraTab === 'pada') return this.selectedMantraDetails.pada_tokens || [];
    if (this.activeMantraTab === 'krama') return this.selectedMantraDetails.krama_tokens || [];
    return this.selectedMantraDetails.samhita_tokens || [];
  }

  // Token Hover Actions
  onTokenHover(wordIds: number[]): void {
    if (!wordIds || wordIds.length === 0 || !this.dictionaryLoaded) {
      this.hoveredWords = [];
      return;
    }
    
    this.hoveredWords = wordIds
      .map(id => this.globalDictionary[id.toString()])
      .filter(w => w !== undefined);
  }

  onTokenLeave(): void {
    this.hoveredWords = [];
  }

  // Helper for Panini rules array rendering
  getPaniniRules(rules: any): string[] {
    if (!rules) return [];
    if (Array.isArray(rules)) return rules;
    if (typeof rules === 'string') return [rules];
    return [];
  }
}
