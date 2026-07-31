import { TestBed } from '@angular/core/testing';
import { ItransService } from './itrans.service';

describe('ItransService', () => {
  let service: ItransService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ItransService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should convert QWERTY ITRANS text to Devanagari', () => {
    expect(service.toDevanagari('namaste')).toEqual('नमस्ते');
    expect(service.toDevanagari('rudra')).toEqual('रुद्र');
    expect(service.toDevanagari('manyave')).toEqual('मन्यवे');
    expect(service.toDevanagari('namaH')).toEqual('नमः');
  });

  it('should preserve Vedic swara accents during transliteration', () => {
    const input = "namas\u0951te ru\u0952dra";
    const dev = service.toDevanagari(input);
    expect(dev).toContain('\u0951');
    expect(dev).toContain('\u0952');
  });
});
