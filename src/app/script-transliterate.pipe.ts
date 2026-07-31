import { Pipe, PipeTransform } from '@angular/core';
import { ScriptTransliterationService } from './script-transliteration.service';

@Pipe({
  name: 'transliterate',
  standalone: true,
  pure: false
})
export class ScriptTransliteratePipe implements PipeTransform {
  constructor(private transliterationService: ScriptTransliterationService) {}

  transform(value: string | undefined | null, targetLang?: string): string {
    if (!value) return '';
    return this.transliterationService.transliterate(value, targetLang);
  }
}
