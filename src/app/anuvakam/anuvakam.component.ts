import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { NamakamService, CorrelatedAnuvakam } from '../namakam.service';
import { SanskritEditorService } from '../sanskrit-editor.service';
import { SanskritEditorModalComponent } from '../sanskrit-editor-modal/sanskrit-editor-modal.component';

@Component({
  selector: 'app-anuvakam',
  standalone: true,
  imports: [CommonModule, RouterLink, SanskritEditorModalComponent],
  templateUrl: './anuvakam.component.html',
  styleUrls: ['./anuvakam.component.css']
})
export class AnuvakamComponent implements OnInit {
  anuvakam: CorrelatedAnuvakam | undefined;
  activeLanguage: 'sanskrit' | 'english' = 'sanskrit';

  editingMantra: any = null;
  anuvakamId: number = 0;

  constructor(
    private route: ActivatedRoute,
    private namakamService: NamakamService,
    private editorService: SanskritEditorService
  ) {}

  ngOnInit(): void {
    this.anuvakamId = Number(this.route.snapshot.paramMap.get('id'));
    this.loadAnuvakam();
  }

  loadAnuvakam(): void {
    this.namakamService.getAnuvakam(this.anuvakamId).subscribe(a => this.anuvakam = a);
  }

  get isEditorEnabled(): boolean {
    return this.editorService.isEditorEnabled();
  }

  openEditor(mantra: any, event: MouseEvent): void {
    event.stopPropagation();
    event.preventDefault();
    this.editingMantra = mantra;
  }

  closeEditor(): void {
    this.editingMantra = null;
  }

  onEditorSaved(): void {
    this.editingMantra = null;
    this.loadAnuvakam();
  }

  getTranslation(mantra: any): string {
    const t = mantra.translations;
    if (!t) return '';
    return t.sayana || t.bhatta_bhaskara || t.abhinava_shankara || '';
  }
}
