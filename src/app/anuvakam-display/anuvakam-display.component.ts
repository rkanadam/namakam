import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NamakamService, Anuvakam, Mantra } from '../namakam.service';

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
  imports: [CommonModule],
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

  // Dictionary Hover State
  globalDictionary: { [key: string]: WordDetails } = {};
  hoveredWords: WordDetails[] = [];
  dictionaryLoaded: boolean = false;

  constructor(private namakamService: NamakamService) {}

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
    this.selectedMantra = null;
    this.selectedMantraDetails = null;
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
