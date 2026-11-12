import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ActivatedRoute, convertToParamMap, provideRouter } from '@angular/router';
import { BehaviorSubject } from 'rxjs';
import { MantraDetailComponent } from './mantra-detail.component';
import { DictionaryEntry } from '../namakam.service';
import { ScriptTransliterationService } from '../script-transliteration.service';

describe('Mantra detail study content', () => {
  let fixture: ComponentFixture<MantraDetailComponent>;
  let http: HttpTestingController;
  let params: BehaviorSubject<ReturnType<typeof convertToParamMap>>;
  const element = () => fixture.nativeElement as HTMLElement;
  const rudra: DictionaryEntry = {
    id: 3, clean_form: 'रुद्र', pada_form: 'रु॒द्र॒',
    meanings: { english: 'Rudra; remover of sorrow', nirukta: 'From the root rud, to cry.', vedantic: 'The presence that dispels suffering.' },
    grammatical_references: { case_ending: 'Vocative singular', panini: ['Vocative address'] },
    lexicographical_references: { nighantu: 'Rudra names', amara_kosha: 'Names of Shiva', abhidhana_ratnamala: '' }
  };
  const tableWord = (word: string) => Array.from(element().querySelectorAll<HTMLButtonElement>('.meaning-word button'))
    .find(button => button.textContent?.trim() === word);


  beforeEach(async () => {
    localStorage.clear();
    params = new BehaviorSubject(convertToParamMap({ anuvakamId: '1', mantraId: '1' }));
    await TestBed.configureTestingModule({
      imports: [MantraDetailComponent],
      providers: [
        provideHttpClient(), provideHttpClientTesting(), provideRouter([]),
        { provide: ActivatedRoute, useValue: { paramMap: params.asObservable() } }
      ]
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
    fixture = TestBed.createComponent(MantraDetailComponent);
    fixture.detectChanges();
    http.expectOne('assets/data.json').flush({
      correlated: { anuvakas: [] }, dictionary: { '3': rudra, '5': { ...rudra, id: 5, clean_form: 'उतोइति', meanings: { ...rudra.meanings, english: 'And also; moreover' }, grammatical_references: { case_ending: 'Particle', panini: 'Vedic particle' } } }, wordIndex: {}, mantras: {}
    });
    fixture.detectChanges();
  });

  afterEach(() => {
    http.verify();
    localStorage.clear();
  });

  it('shows a summary and correct word meanings even without legacy dictionary data', () => {
    const summary = element().querySelector('.summary-translation');
    expect(summary?.textContent).toContain('anger');
    const disclosure = element().querySelector<HTMLDetailsElement>('.word-meanings');
    expect(disclosure).not.toBeNull();
    expect(disclosure?.open).toBeFalse();
    const rows = Array.from(element().querySelectorAll('.word-meanings tbody tr'));
    const arrow = rows.find(row => row.querySelector('th')?.textContent?.trim() === 'इषवे');
    expect(arrow?.querySelector('td')?.textContent).toContain('arrow');
    expect(element().querySelectorAll('.word-meanings thead th').length).toBe(2);
  });

  it('replaces the summary and table and closes the disclosure on route changes', () => {
    const disclosure = element().querySelector<HTMLDetailsElement>('.word-meanings');
    expect(disclosure).not.toBeNull();
    if (!disclosure) return;
    disclosure.open = true;
    disclosure.dispatchEvent(new Event('toggle'));
    fixture.detectChanges();
    params.next(convertToParamMap({ anuvakamId: '8', mantraId: '8' }));
    fixture.detectChanges();
    expect(element().querySelector('.summary-translation')?.textContent).toContain('liberating');
    expect(element().querySelector('.word-meanings tbody')?.textContent).toContain('ताराय');
    expect(element().querySelector('.word-meanings tbody')?.textContent).not.toContain('इषवे');
    expect(element().querySelector<HTMLDetailsElement>('.word-meanings')?.open).toBeFalse();
  });

  it('transliterates the words while preserving English meanings', () => {
    TestBed.inject(ScriptTransliterationService).setLanguage('english');
    fixture.detectChanges();
    const words = element().querySelector('.word-meanings tbody')?.textContent || '';
    expect(words).toContain('iṣave');
    expect(words).toContain('To the arrow');
    expect(words).not.toContain('इषवे');
  });

  it('does not show stale study content for an unknown mantra', () => {
    params.next(convertToParamMap({ anuvakamId: '99', mantraId: '99' }));
    fixture.detectChanges();
    expect(element().querySelector('.summary-translation')).toBeNull();
    expect(element().querySelector('.word-meanings')).toBeNull();
  });
  it('shows the same full dictionary analysis when a table word is hovered or clicked', fakeAsync(() => {
    const button = tableWord('रुद्र');
    expect(button).toBeDefined();
    if (!button) return;
    button.dispatchEvent(new MouseEvent('mouseenter'));
    fixture.detectChanges();
    const tooltip = element().querySelector('.word-tooltip');
    expect(tooltip?.textContent).toContain('From the root rud');
    expect(tooltip?.textContent).toContain('Vocative singular');
    expect(tooltip?.textContent).toContain('Names of Shiva');
    button.dispatchEvent(new MouseEvent('mouseleave'));
    tick(201);
    fixture.detectChanges();
    expect(element().querySelector('.word-tooltip')).toBeNull();
    button.click();
    fixture.detectChanges();
    tick();
    expect(element().querySelector('.word-panel')?.textContent).toContain('The presence that dispels suffering');
    expect(element().querySelector('.word-panel')?.textContent).toContain('Names of Shiva');
    button.click();
    fixture.detectChanges();
    expect(element().querySelector('.word-panel')).toBeNull();
  }));

  it('resolves a pada spelling alias and renders legacy string grammar on keyboard focus', () => {
    const button = tableWord('उतो');
    expect(button).toBeDefined();
    if (!button) return;
    button.dispatchEvent(new FocusEvent('focus'));
    fixture.detectChanges();
    expect(element().querySelector('.word-tooltip')?.textContent).toContain('And also; moreover');
    expect(element().querySelector('.tooltip-ref')?.textContent).toContain('Vedic particle');
  });

  it('clears table word detail and hover state when the mantra changes', fakeAsync(() => {
    const button = tableWord('रुद्र');
    expect(button).toBeDefined();
    if (!button) return;
    button.dispatchEvent(new MouseEvent('mouseenter'));
    button.click();
    fixture.detectChanges();
    tick();
    params.next(convertToParamMap({ anuvakamId: '8', mantraId: '8' }));
    fixture.detectChanges();
    expect(element().querySelector('.word-tooltip')).toBeNull();
    expect(element().querySelector('.word-panel')).toBeNull();
  }));

  it('keeps a word usable when detailed dictionary data is missing', fakeAsync(() => {
    const button = tableWord('इषवे');
    expect(button).toBeDefined();
    if (!button) return;
    button.click();
    fixture.detectChanges();
    tick();
    expect(element().querySelector('.word-panel')?.textContent).toContain('To the arrow');
    expect(element().querySelector('.word-panel')?.textContent).toContain('Only the brief meaning');
  }));

  it('keeps a tall tooltip below the top edge of the viewport', () => {
    const button = tableWord('रुद्र')!;
    spyOn(button, 'getBoundingClientRect').and.returnValue({
      top: 201, bottom: 229, left: 12, right: 60, width: 48, height: 28, x: 12, y: 201,
      toJSON: () => ({})
    });
    button.dispatchEvent(new MouseEvent('mouseenter'));
    fixture.detectChanges();
    const tooltip = element().querySelector<HTMLElement>('.word-tooltip')!;
    expect(tooltip.getBoundingClientRect().top).toBeGreaterThanOrEqual(16);
  });

});
