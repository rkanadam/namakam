import { Component } from '@angular/core';
import { AnuvakamDisplayComponent } from './anuvakam-display/anuvakam-display.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [AnuvakamDisplayComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'namakam';
}
