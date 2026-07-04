import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { NamakamService, CorrelatedAnuvakam } from '../namakam.service';

@Component({
  selector: 'app-anuvakam',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './anuvakam.component.html',
  styleUrls: ['./anuvakam.component.css']
})
export class AnuvakamComponent implements OnInit {
  anuvakam: CorrelatedAnuvakam | undefined;
  activeLanguage: 'sanskrit' | 'english' = 'sanskrit';

  constructor(
    private route: ActivatedRoute,
    private namakamService: NamakamService
  ) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.namakamService.getAnuvakam(id).subscribe(a => this.anuvakam = a);
  }

  getTranslation(mantra: any): string {
    const t = mantra.translations;
    if (!t) return '';
    return t.sayana || t.bhatta_bhaskara || t.abhinava_shankara || '';
  }
}
