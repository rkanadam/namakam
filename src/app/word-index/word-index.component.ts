import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { forkJoin } from 'rxjs';
import { NamakamService, Dictionary, DictionaryEntry, WordIndex, MantraRef, Anuvakam } from '../namakam.service';
import { ScriptTransliteratePipe } from '../script-transliterate.pipe';

interface WordEntry {
  entry: DictionaryEntry;
  refs: MantraRef[];
}

@Component({
  selector: 'app-word-index',
  standalone: true,
  imports: [CommonModule, RouterLink, ScriptTransliteratePipe],
  templateUrl: './word-index.component.html',
  styleUrls: ['./word-index.component.css']
})
export class WordIndexComponent implements OnInit {
  allWords: WordEntry[] = [];
  filteredWords: WordEntry[] = [];
  searchTerm = '';
  totalRefs = 0;

  anuvakams: Anuvakam[] = [];
  expandedAnuvakams: { [key: number]: boolean } = {};

  constructor(
    private namakamService: NamakamService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.anuvakams = this.namakamService.getAnuvakams();
    forkJoin({
      dictionary: this.namakamService.getDictionary(),
      wordIndex: this.namakamService.getWordIndex()
    }).subscribe(({ dictionary, wordIndex }) => {
      this.allWords = Object.keys(dictionary)
        .map(id => ({
          entry: dictionary[id],
          refs: (wordIndex[id] || []).sort((a, b) => a.anuvakam - b.anuvakam || a.mantra - b.mantra)
        }))
        .sort((a, b) => a.entry.clean_form.localeCompare(b.entry.clean_form, 'sa'));
      this.totalRefs = this.allWords.reduce((sum, w) => sum + w.refs.length, 0);
      this.filteredWords = this.allWords;
    });
  }

  isAnuvakamExpanded(id: number): boolean {
    return !!this.expandedAnuvakams[id];
  }

  toggleAnuvakamExpand(id: number, event?: Event): void {
    if (event) event.stopPropagation();
    this.expandedAnuvakams[id] = !this.isAnuvakamExpanded(id);
  }

  isSidebarCollapsed(): boolean {
    return this.namakamService.isSidebarCollapsed();
  }

  toggleSidebar(): void {
    this.namakamService.toggleSidebarCollapsed();
  }

  getMantraPrefix(text: string): string {
    return this.namakamService.getMantraPrefix(text);
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

  onSearch(event: Event): void {
    this.searchTerm = (event.target as HTMLInputElement).value.trim().toLowerCase();
    if (!this.searchTerm) {
      this.filteredWords = this.allWords;
      return;
    }
    this.filteredWords = this.allWords.filter(w =>
      w.entry.clean_form.includes(this.searchTerm) ||
      w.entry.pada_form.includes(this.searchTerm) ||
      w.entry.meanings.english.toLowerCase().includes(this.searchTerm)
    );
  }
}
