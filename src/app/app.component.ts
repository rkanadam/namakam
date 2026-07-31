import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, RouterLink } from '@angular/router';
import { SanskritEditorService } from './sanskrit-editor.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'namakam';

  constructor(private editorService: SanskritEditorService) {}

  get isEditorEnabled(): boolean {
    return this.editorService.isEditorEnabled();
  }

  exportEdits(): void {
    this.editorService.exportEditsAsJson();
  }

  importEdits(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (!input.files?.length) return;
    const file = input.files[0];
    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target?.result as string;
      if (this.editorService.importEditsFromJson(content)) {
        alert('Sanskrit text & intonation corrections imported successfully!');
        window.location.reload();
      } else {
        alert('Failed to import JSON file. Please verify the file format.');
      }
    };
    reader.readAsText(file);
  }

  clearAllEdits(): void {
    if (confirm('Are you sure you want to clear all custom Sanskrit text corrections?')) {
      this.editorService.clearAllEdits();
      window.location.reload();
    }
  }
}
