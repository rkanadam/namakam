import { Injectable } from '@angular/core';
import anuvakam1 from '../anuvakam1.json';
import anuvakam2 from '../anuvakam2.json';
import anuvakam3 from '../anuvakam3.json';
import anuvakam4 from '../anuvakam4.json';
import anuvakam5 from '../anuvakam5.json';
import anuvakam6 from '../anuvakam6.json';
import anuvakam7 from '../anuvakam7.json';
import anuvakam8 from '../anuvakam8.json';
import anuvakam9 from '../anuvakam9.json';
import anuvakam10 from '../anuvakam10.json';
import anuvakam11 from '../anuvakam11.json';

export interface Mantra {
  id: number;
  samhita: string;
  pada: string;
  krama: string;
}

export interface Anuvakam {
  anuvakam: number;
  title: string;
  mantras: Mantra[];
}

@Injectable({
  providedIn: 'root'
})
export class NamakamService {
  private anuvakams: Anuvakam[] = [
    anuvakam1, anuvakam2, anuvakam3, anuvakam4, anuvakam5,
    anuvakam6, anuvakam7, anuvakam8, anuvakam9, anuvakam10, anuvakam11
  ] as Anuvakam[];

  getAnuvakams(): Anuvakam[] {
    return this.anuvakams;
  }
}
