import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { forkJoin } from 'rxjs';
import { NamakamService, Dictionary, DictionaryEntry, WordIndex, MantraRef } from '../namakam.service';

interface WordEntry {
  entry: DictionaryEntry;
  refs: MantraRef[];
}

@Component({
  selector: 'app-word-index',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './word-index.component.html',
  styleUrls: ['./word-index.component.css']
})
export class WordIndexComponent implements OnInit {
  allWords: WordEntry[] = [];
  filteredWords: WordEntry[] = [];
  searchTerm = '';
  totalRefs = 0;

  constructor(private namakamService: NamakamService) {}

  ngOnInit(): void {
    forkJoin({
      dictionary: this.namakamService.getDictionary(),
      wordIndex: this.namakamService.getWordIndex()
    }).subscribe(({ dictionary, wordIndex }) => {
      this.allWords = Object.keys(dictionary)
        .map(id => ({
          entry: dictionary[id],
          refs: (wordIndex[id] || []).sort((a, b) => a.anuvakam - b.anuvakam || a.mantra - b.mantra)
        }))
        .sort((a, b) => a.entry.clean_form.localeCompare(b.entry.clean_form, 'sa'));
      this.totalRefs = this.allWords.reduce((sum, w) => sum + w.refs.length, 0);
      this.filteredWords = this.allWords;
    });
  }

  onSearch(event: Event): void {
    this.searchTerm = (event.target as HTMLInputElement).value.trim().toLowerCase();
    if (!this.searchTerm) {
      this.filteredWords = this.allWords;
      return;
    }
    this.filteredWords = this.allWords.filter(w =>
      w.entry.clean_form.includes(this.searchTerm) ||
      w.entry.pada_form.includes(this.searchTerm) ||
      w.entry.meanings.english.toLowerCase().includes(this.searchTerm)
    );
  }
}
