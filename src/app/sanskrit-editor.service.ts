import { Injectable } from '@angular/core';
import { environment } from '../environments/environment';

export interface MantraEdit {
  samhita?: string;
  pada?: string;
  krama?: string;
  updatedAt?: string;
}

export interface AllEditsMap {
  [key: string]: MantraEdit; // key format: "${anuvakamId}_${mantraId}"
}

declare const process: any;

@Injectable({
  providedIn: 'root'
})
export class SanskritEditorService {
  private readonly STORAGE_KEY = 'namakam_sanskrit_edits';

  /**
   * Checks if the Sanskrit Editor is enabled via environment variable or runtime flag.
   */
  isEditorEnabled(): boolean {
    // 1. Check environment variable from process.env (Node / build time / Angular CLI)
    try {
      if (typeof process !== 'undefined' && process?.env) {
        const envVal = process.env['ENABLE_EDITOR'] || 
                       process.env['ENABLE_SANSKRIT_EDITOR'] || 
                       process.env['NG_APP_ENABLE_EDITOR'];
        if (envVal === 'true' || envVal === '1') {
          return true;
        }
      }
    } catch (e) {
      // Ignore error if process is undefined
    }

    // 2. Check Angular environment config
    if (environment?.enableEditor) {
      return true;
    }

    // 3. Check window global object or localStorage (allows runtime toggle via browser)
    if (typeof window !== 'undefined') {
      const win = window as any;
      if (win.ENABLE_EDITOR === true || win.ENABLE_EDITOR === 'true' || win.env?.ENABLE_EDITOR === 'true') {
        return true;
      }
      if (localStorage.getItem('ENABLE_EDITOR') === 'true') {
        return true;
      }
    }

    return false;
  }

  /**
   * Enables or disables editor via localStorage for testing in browser console.
   */
  setEditorEnabledState(enabled: boolean): void {
    if (enabled) {
      localStorage.setItem('ENABLE_EDITOR', 'true');
    } else {
      localStorage.removeItem('ENABLE_EDITOR');
    }
  }

  /**
   * Retrieves all saved edits from LocalStorage.
   */
  getAllEdits(): AllEditsMap {
    try {
      const raw = localStorage.getItem(this.STORAGE_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (e) {
      console.error('Failed to parse saved Sanskrit edits from localStorage:', e);
      return {};
    }
  }

  /**
   * Gets specific mantra edit override if present.
   */
  getMantraEdit(anuvakamId: number, mantraId: number): MantraEdit | null {
    const edits = this.getAllEdits();
    const key = `${anuvakamId}_${mantraId}`;
    return edits[key] || null;
  }

  /**
   * Saves custom Sanskrit text and intonations for a specific mantra.
   */
  saveMantraEdit(anuvakamId: number, mantraId: number, edit: { samhita: string; pada: string; krama: string }): void {
    const edits = this.getAllEdits();
    const key = `${anuvakamId}_${mantraId}`;
    edits[key] = {
      samhita: edit.samhita.trim(),
      pada: edit.pada.trim(),
      krama: edit.krama.trim(),
      updatedAt: new Date().toISOString()
    };
    localStorage.setItem(this.STORAGE_KEY, JSON.stringify(edits));
  }

  /**
   * Resets edits for a specific mantra back to original defaults.
   */
  resetMantraEdit(anuvakamId: number, mantraId: number): void {
    const edits = this.getAllEdits();
    const key = `${anuvakamId}_${mantraId}`;
    if (edits[key]) {
      delete edits[key];
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(edits));
    }
  }

  /**
   * Clears all saved edits.
   */
  clearAllEdits(): void {
    localStorage.removeItem(this.STORAGE_KEY);
  }

  /**
   * Exports all custom edits as a JSON file download.
   */
  exportEditsAsJson(): void {
    const edits = this.getAllEdits();
    const jsonStr = JSON.stringify(edits, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `sanskrit_intonation_corrections_${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }

  /**
   * Imports edits from a JSON string.
   */
  importEditsFromJson(jsonString: string): boolean {
    try {
      const parsed = JSON.parse(jsonString);
      if (typeof parsed === 'object' && parsed !== null) {
        const current = this.getAllEdits();
        const merged = { ...current, ...parsed };
        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(merged));
        return true;
      }
    } catch (e) {
      console.error('Invalid JSON for Sanskrit edits:', e);
    }
    return false;
  }

  /**
   * Utility method to strip Vedic swara / intonation accents from text.
   */
  cleanIntonations(text: string): string {
    if (!text) return '';
    // Strip Devanagari stress signs (Anudatta U+0952, Svarita U+0951, Vedic extensions U+1CD0-U+1CFF)
    return text.replace(/[\u0951\u0952\u1CD0-\u1CFF]/g, '');
  }
}
