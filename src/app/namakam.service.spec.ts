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

    const shivatameti = rebuilt.find((t: any) => t.text.includes("शि॒वत॒मेति"));
    expect(shivatameti).toBeDefined();
    expect(shivatameti.word_ids).toEqual([67]);

    const shivam = rebuilt.find((t: any) => t.text.trim() === "शि॒वम");
    expect(shivam).toBeDefined();
    expect(shivam.word_ids).toEqual([68]);

    const teTokens = rebuilt.filter((t: any) => t.text.trim() === "ते॒");
    expect(teTokens.length).toBeGreaterThan(0);
    expect(teTokens[0].word_ids).toEqual([2]);
  });

  it('should correctly align Mantra 3 Padapatha iti expansions like "apapakashini", "tanuva", "girishanta"', () => {
    const originalMantra3PadaTokens = [
      { text: "या", word_ids: [44] },
      { text: " । ", word_ids: [] },
      { text: "ते॒", word_ids: [2] },
      { text: " । ", word_ids: [] },
      { text: "रु॒द्र॒", word_ids: [3] },
      { text: " । ", word_ids: [] },
      { text: "शि॒वा", word_ids: [69] },
      { text: " । ", word_ids: [] },
      { text: "त॒नूः", word_ids: [72] },
      { text: " । ", word_ids: [] },
      { text: "अ॒घो॒रा", word_ids: [73] },
      { text: " । ", word_ids: [] },
      { text: "अ॒पा॑प-काशिनी", word_ids: [74] },
      { text: " । ", word_ids: [] },
      { text: "तया॑", word_ids: [48] },
      { text: " । ", word_ids: [] },
      { text: "नः॒", word_ids: [33] },
      { text: " । ", word_ids: [] },
      { text: "त॒नुवा॑", word_ids: [75] },
      { text: " । ", word_ids: [] },
      { text: "शन्तः॑-मया", word_ids: [76] },
      { text: " । ", word_ids: [] },
      { text: "गिरि॑-शन्त", word_ids: [77] },
      { text: " । ", word_ids: [] },
      { text: "अ॒भि", word_ids: [78] },
      { text: " । ", word_ids: [] },
      { text: "चा॒क॒शी॒हि॒", word_ids: [79] }
    ];

    const newPadaText = "या । ते॒ । रु॒द्र॒ । शि॒वा । त॒नूः । अघो॑रा । अपा॑पकाशि॒ नीत्य पा॑प = का॒शि॒नी॒ । तया᳚ । नः॒ । त॒नुवा॑॑ । शन्त॑म॒येति॒ शम त॒म॒या॒ । गिरि॑श॒न्तेति॒ गिरि॑ = श॒न्त॒ । अ॒भिति॑ (अ॒भि) । चा॒क॒शी॒हि॒";

    const rebuilt = (service as any).rebuildTokens(originalMantra3PadaTokens, newPadaText);

    // Verify "taya" gets word_ids [48]
    const tayaToken = rebuilt.find((t: any) => t.text.trim() === "तया᳚");
    expect(tayaToken).toBeDefined();
    expect(tayaToken.word_ids).toEqual([48]);

    // Verify "nah" gets word_ids [33]
    const nahToken = rebuilt.find((t: any) => t.text.trim() === "नः॒");
    expect(nahToken).toBeDefined();
    expect(nahToken.word_ids).toEqual([33]);

    // Verify "tanuva" gets word_ids [75]
    const tanuvaToken = rebuilt.find((t: any) => t.text.trim().startsWith("त॒नुवा"));
    expect(tanuvaToken).toBeDefined();
    expect(tanuvaToken.word_ids).toEqual([75]);

    // Verify "chakashihi" gets word_ids [79]
    const chakashihiToken = rebuilt.find((t: any) => t.text.trim() === "चा॒क॒शी॒हि॒");
    expect(chakashihiToken).toBeDefined();
    expect(chakashihiToken.word_ids).toEqual([79]);
  });
});
