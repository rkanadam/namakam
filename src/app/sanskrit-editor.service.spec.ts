import { TestBed } from '@angular/core/testing';
import { SanskritEditorService } from './sanskrit-editor.service';

describe('SanskritEditorService', () => {
  let service: SanskritEditorService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SanskritEditorService);
    localStorage.clear();
  });

  afterEach(() => {
    localStorage.clear();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should detect editor state from localStorage or process.env or window', () => {
    expect(service.isEditorEnabled()).toBeFalse();
    service.setEditorEnabledState(true);
    expect(service.isEditorEnabled()).toBeTrue();
    service.setEditorEnabledState(false);
    expect(service.isEditorEnabled()).toBeFalse();
  });

  it('should save, retrieve and reset mantra edits', () => {
    expect(service.getMantraEdit(1, 1)).toBeNull();

    service.saveMantraEdit(1, 1, {
      samhita: 'नम॑स्ते रु॒द्र',
      pada: 'नमः॑ । ते॒ । रु॒द्र॒',
      krama: 'नम॑स्ते । ते रु॑द्र'
    });

    const saved = service.getMantraEdit(1, 1);
    expect(saved).not.toBeNull();
    expect(saved?.samhita).toEqual('नम॑स्ते रु॒द्र');
    expect(saved?.pada).toEqual('नमः॑ । ते॒ । रु॒द्र॒');

    service.resetMantraEdit(1, 1);
    expect(service.getMantraEdit(1, 1)).toBeNull();
  });

  it('should strip Vedic swara accents cleanly', () => {
    const textWithSwaras = 'नम॑स्ते रुद्र म॒न्यव॑';
    const cleanText = service.cleanIntonations(textWithSwaras);
    expect(cleanText).toEqual('नमस्ते रुद्र मन्यव');
  });

  it('should export and import edits JSON', () => {
    const editsToImport = JSON.stringify({
      "1_1": {
        samhita: "नम॑स्ते रु॒द्र",
        pada: "नमः॑ । ते॒",
        krama: "नम॑स्ते"
      }
    });

    const success = service.importEditsFromJson(editsToImport);
    expect(success).toBeTrue();

    const retrieved = service.getMantraEdit(1, 1);
    expect(retrieved?.samhita).toEqual('नम॑स्ते रु॒द्र');
  });
});
