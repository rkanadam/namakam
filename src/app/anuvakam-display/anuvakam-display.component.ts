import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NamakamService, Anuvakam } from '../namakam.service';

@Component({
  selector: 'app-anuvakam-display',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './anuvakam-display.component.html',
  styleUrls: ['./anuvakam-display.component.css']
})
export class AnuvakamDisplayComponent implements OnInit {
  anuvakams: Anuvakam[] = [];
  activeTab: { [key: number]: string } = {};

  constructor(private namakamService: NamakamService) {}

  ngOnInit(): void {
    this.anuvakams = this.namakamService.getAnuvakams();
    this.anuvakams.forEach(a => {
      this.activeTab[a.anuvakam] = 'samhita';
    });
  }

  setActiveTab(anuvakamNum: number, tab: string): void {
    this.activeTab[anuvakamNum] = tab;
  }

  scrollToAnuvakam(anuvakamNum: number): void {
    const element = document.getElementById(`anuvakam-${anuvakamNum}`);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  }
}
