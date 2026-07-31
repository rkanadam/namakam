import { Component, Input, Output, EventEmitter, OnInit, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SanskritEditorService } from '../sanskrit-editor.service';
import { ItransService } from '../itrans.service';

interface SwaraSymbol {
  symbol: string;
  name: string;
  char: string;
  shortcut: string;
}

@Component({
  selector: 'app-sanskrit-editor-modal',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './sanskrit-editor-modal.component.html',
  styleUrls: ['./sanskrit-editor-modal.component.css']
})
export class SanskritEditorModalComponent implements OnInit {
  @Input() anuvakamId!: number;
  @Input() mantraId!: number;
  @Input() initialSamhita: string = '';
  @Input() initialPada: string = '';
  @Input() initialKrama: string = '';

  @Output() saved = new EventEmitter<void>();
  @Output() cancelled = new EventEmitter<void>();

  @ViewChild('editorTextarea') editorTextarea!: ElementRef<HTMLTextAreaElement>;

  samhita: string = '';
  pada: string = '';
  krama: string = '';

  activeTab: 'samhita' | 'pada' | 'krama' = 'samhita';
  hasCustomEdits: boolean = false;

  swaraSymbols: SwaraSymbol[] = [
    { symbol: ' ॒ ', name: 'अनुदात्तः (Anudatta - Stress Below)', char: '\u0952', shortcut: 'Alt+1' },
    { symbol: ' ॑ ', name: 'स्वरितः (Svarita - Stress Above)', char: '\u0951', shortcut: 'Alt+2' },
    { symbol: ' ᳚ ', name: 'दीर्घस्वरितः (Dirgha Svarita - Double Stress)', char: '\u1CDA', shortcut: 'Alt+3' },
    { symbol: 'ऽ', name: 'अवग्रहः (Avagraha)', char: '\u093D', shortcut: 'Alt+4' },
    { symbol: 'ं', name: 'अनुस्वारः (Anusvara)', char: '\u0902', shortcut: 'Alt+5' },
    { symbol: 'ः', name: 'विसर्गः (Visarga)', char: '\u0903', shortcut: 'Alt+6' },
    { symbol: '।', name: 'दण्डः (Single Danda)', char: ' ।', shortcut: 'Alt+7' },
    { symbol: '॥', name: 'द्विदण्डः (Double Danda)', char: ' ॥', shortcut: 'Alt+8' },
    { symbol: 'ᳵ', name: 'जिह्वामूलीयः (Jihvamuliya)', char: '\u1CF5', shortcut: 'Alt+9' },
    { symbol: 'ᳶ', name: 'उपध्मानीयः (Upadhmaniya)', char: '\u1CF6', shortcut: 'Alt+0' },
    { symbol: ' ् ', name: 'विरामः / हलन्तः (Virama - Consonant Suppressor)', char: '\u094D', shortcut: 'Halant' }
  ];

  constructor(
    private editorService: SanskritEditorService,
    private itransService: ItransService
  ) {}

  ngOnInit(): void {
    const edit = this.editorService.getMantraEdit(this.anuvakamId, this.mantraId);
    if (edit) {
      this.samhita = edit.samhita !== undefined ? edit.samhita : this.initialSamhita;
      this.pada = edit.pada !== undefined ? edit.pada : this.initialPada;
      this.krama = edit.krama !== undefined ? edit.krama : this.initialKrama;
      this.hasCustomEdits = true;
    } else {
      this.samhita = this.initialSamhita;
      this.pada = this.initialPada;
      this.krama = this.initialKrama;
      this.hasCustomEdits = false;
    }
  }

  get activeText(): string {
    if (this.activeTab === 'pada') return this.pada;
    if (this.activeTab === 'krama') return this.krama;
    return this.samhita;
  }

  set activeText(val: string) {
    if (this.activeTab === 'pada') this.pada = val;
    else if (this.activeTab === 'krama') this.krama = val;
    else this.samhita = val;
  }

  convertPhoneticToDevanagari(): void {
    this.activeText = this.itransService.toDevanagari(this.activeText);
  }

  onTextareaKeydown(e: KeyboardEvent): void {
    if (e.altKey || e.ctrlKey) {
      let charToInsert: string | null = null;
      switch (e.key) {
        case '1': charToInsert = '\u0952'; break; // Anudatta
        case '2': charToInsert = '\u0951'; break; // Svarita
        case '3': charToInsert = '\u1CDA'; break; // Dirgha Svarita
        case '4': charToInsert = '\u093D'; break; // Avagraha
        case '5': charToInsert = '\u0902'; break; // Anusvara
        case '6': charToInsert = '\u0903'; break; // Visarga
        case '7': charToInsert = ' ।'; break;     // Single Danda
        case '8': charToInsert = ' ॥'; break;     // Double Danda
        case '9': charToInsert = '\u1CF5'; break; // Jihvamuliya
        case '0': charToInsert = '\u1CF6'; break; // Upadhmaniya
      }

      if (charToInsert) {
        e.preventDefault();
        e.stopPropagation();
        this.insertSymbol(charToInsert);
      }
    }
  }

  insertSymbol(char: string): void {
    const textarea = this.editorTextarea?.nativeElement;
    if (!textarea) {
      this.activeText += char;
      return;
    }

    const startPos = textarea.selectionStart;
    const endPos = textarea.selectionEnd;
    const currentValue = this.activeText;

    const newValue = currentValue.substring(0, startPos) + char + currentValue.substring(endPos);
    this.activeText = newValue;

    // Restore focus & cursor position after inserted character
    setTimeout(() => {
      textarea.focus();
      textarea.setSelectionRange(startPos + char.length, startPos + char.length);
    }, 0);
  }

  stripAccents(): void {
    this.activeText = this.editorService.cleanIntonations(this.activeText);
  }

  save(): void {
    this.editorService.saveMantraEdit(this.anuvakamId, this.mantraId, {
      samhita: this.samhita,
      pada: this.pada,
      krama: this.krama
    });
    this.saved.emit();
  }

  resetToDefault(): void {
    if (confirm('Are you sure you want to reset this mantra to its original Sanskrit text and intonations?')) {
      this.editorService.resetMantraEdit(this.anuvakamId, this.mantraId);
      this.samhita = this.initialSamhita;
      this.pada = this.initialPada;
      this.krama = this.initialKrama;
      this.hasCustomEdits = false;
      this.saved.emit();
    }
  }

  close(): void {
    this.cancelled.emit();
  }
}
