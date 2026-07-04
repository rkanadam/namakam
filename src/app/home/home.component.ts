import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { NamakamService, CorrelatedAnuvakam } from '../namakam.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  anuvakas: CorrelatedAnuvakam[] = [];

  constructor(private namakamService: NamakamService) {}

  ngOnInit(): void {
    this.namakamService.getAnuvakas().subscribe(a => this.anuvakas = a);
  }
}
