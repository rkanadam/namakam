import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { AnuvakamComponent } from './anuvakam/anuvakam.component';
import { MantraDetailComponent } from './mantra-detail/mantra-detail.component';
import { PrefaceComponent } from './preface/preface.component';
import { WordIndexComponent } from './word-index/word-index.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'introduction', component: PrefaceComponent, data: { type: 'introduction' } },
  { path: 'conclusion', component: PrefaceComponent, data: { type: 'conclusion' } },
  { path: 'word-index', component: WordIndexComponent },
  { path: 'anuvakam/:id', component: AnuvakamComponent },
  { path: 'anuvakam/:anuvakamId/mantra/:mantraId', component: MantraDetailComponent },
];
