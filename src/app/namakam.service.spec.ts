import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { NamakamService } from './namakam.service';
import { SanskritEditorService } from './sanskrit-editor.service';

describe('NamakamService Token Rebuilding', () => {
  let service: NamakamService;
  let editorService: SanskritEditorService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        NamakamService,
        SanskritEditorService
      ]
    });
    service = TestBed.inject(NamakamService);
    editorService = TestBed.inject(SanskritEditorService);
    localStorage.clear();
  });

  afterEach(() => {
    localStorage.clear();
  });

  it('should maintain correct word_ids for "te" (word 2) and "rudra" (word 3) when Padapatha is edited', () => {
    const originalPadaTokens = [
      { text: "नमः॑", word_ids: [1] },
      { text: " । ", word_ids: [] },
      { text: "ते॒", word_ids: [2] },
      { text: " । ", word_ids: [] },
      { text: "रु॒द्र॒", word_ids: [3] }
    ];

    const rebuilt = (service as any).rebuildTokens(originalPadaTokens, "नमः॑ । ते॒ । रु॒द्र॒");
    
    const teToken = rebuilt.find((t: any) => t.text.trim() === "ते॒");
    expect(teToken).toBeDefined();
    expect(teToken.word_ids).toEqual([2]); // Word ID 2 = "te"

    const rudraToken = rebuilt.find((t: any) => t.text.trim() === "रु॒द्र॒");
    expect(rudraToken).toBeDefined();
    expect(rudraToken.word_ids).toEqual([3]); // Word ID 3 = "rudra"
  });

  it('should correctly align Mantra 2 Padapatha compound words with iti and hyphens', () => {
    const originalMantra2PadaTokens = [
      { text: "या", word_ids: [44] },
      { text: " । ", word_ids: [] },
      { text: "ते॒", word_ids: [2] },
      { text: " । ", word_ids: [] },
      { text: "इषुः॑", word_ids: [66] },
      { text: " । ", word_ids: [] },
      { text: "शि॒व॒-तमा॑", word_ids: [67] },
      { text: " । ", word_ids: [] },
      { text: "शि॒वम्", word_ids: [68] },
      { text: " । ", word_ids: [] },
      { text: "ब॒भूव॑", word_ids: [47] },
      { text: " । ", word_ids: [] },
      { text: "ते॒", word_ids: [2] },
      { text: " । ", word_ids: [] },
      { text: "धनुः॑", word_ids: [26] }
    ];

    const newPadaText = "या । ते॒ । इषुः॑ । शि॒वत॒मेति॑ शि॒व = त॒मा॒ । शि॒वम । ब॒भूव॑ । ते॒ । धनुः॑";

    const rebuilt = (service as any).rebuildTokens(originalMantra2PadaTokens, newPadaText);

    // Verify "शि॒वत॒मेति॑" gets word_ids [67] (shivatama)
    const shivatameti = rebuilt.find((t: any) => t.text.includes("शि॒वत॒मेति"));
    expect(shivatameti).toBeDefined();
    expect(shivatameti.word_ids).toEqual([67]);

    // Verify "शि॒वम" gets word_ids [68] (shivam)
    const shivam = rebuilt.find((t: any) => t.text.trim() === "शि॒वम");
    expect(shivam).toBeDefined();
    expect(shivam.word_ids).toEqual([68]);

    // Verify "ते॒" gets word_ids [2] (te)
    const teTokens = rebuilt.filter((t: any) => t.text.trim() === "ते॒");
    expect(teTokens.length).toBeGreaterThan(0);
    expect(teTokens[0].word_ids).toEqual([2]);
  });
});
