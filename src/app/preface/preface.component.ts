import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { NamakamService, Preface, Anuvakam } from '../namakam.service';

@Component({
  selector: 'app-preface',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './preface.component.html',
  styleUrls: ['./preface.component.css']
})
export class PrefaceComponent implements OnInit {
  type: 'introduction' | 'conclusion' = 'introduction';
  data: Preface | null = null;
  activeSource: 'rudradhyaya' | 'rudrabhashya' = 'rudradhyaya';
  activeLanguage: 'sanskrit' | 'english' = 'english';

  anuvakams: Anuvakam[] = [];
  expandedAnuvakams: { [key: number]: boolean } = {};

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private namakamService: NamakamService
  ) {}

  ngOnInit(): void {
    this.anuvakams = this.namakamService.getAnuvakams();
    this.type = this.route.snapshot.data['type'] || 'introduction';
    const source$ = this.type === 'introduction'
      ? this.namakamService.getIntroduction()
      : this.namakamService.getConclusion();
    source$.subscribe(d => this.data = d);
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

  get title(): string {
    return this.type === 'introduction'
      ? 'प्रस्तावना — Introduction'
      : 'उपसंहारः — Conclusion';
  }

  get currentText(): string {
    if (!this.data) return '';
    return this.data[this.activeSource][this.activeLanguage];
  }
}
