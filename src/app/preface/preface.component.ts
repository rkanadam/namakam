import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { NamakamService, Preface } from '../namakam.service';

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

  constructor(
    private route: ActivatedRoute,
    private namakamService: NamakamService
  ) {}

  ngOnInit(): void {
    this.type = this.route.snapshot.data['type'] || 'introduction';
    const source$ = this.type === 'introduction'
      ? this.namakamService.getIntroduction()
      : this.namakamService.getConclusion();
    source$.subscribe(d => this.data = d);
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
