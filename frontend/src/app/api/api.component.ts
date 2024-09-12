import { Component } from '@angular/core';
import { ColourFilter } from './settings-interface';

@Component({
  selector: 'app-api',
  standalone: true,
  imports: [],
  templateUrl: './api.component.html',
  styleUrl: './api.component.css'
})
export class APIComponent {
  public setColourFilter(newFilterDate: ColourFilter){
    url = `http://localhost:5000/setting_change?ID=${this.ID}&filter=${this.filter}&with_rows=${this.with_rows}&with_level=${this.with_level}`
  }
}
