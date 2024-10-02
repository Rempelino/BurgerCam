import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { VideoStreamComponent } from '../video-streamer/video-streamer.component';
import { DoubleSliderComponent } from "../double-slider/double-slider.component";
import { MatCard, MatCardTitle } from '@angular/material/card';
import { SettingsStructure } from '../app.interface';
import { firstValueFrom } from 'rxjs';
import { ApiServiceService } from '../api.service';

@Component({
  selector: 'app-filter-settings-f2',
  standalone: true,
  imports: [VideoStreamComponent,
    CommonModule,
    DoubleSliderComponent,
    DoubleSliderComponent,
    MatCard,
    MatCardTitle
  ],
  templateUrl: './filter-settings-f2.component.html',
  styleUrl: './filter-settings-f2.component.css'
})


export class FilterSettingsF2Component {
  failedToConnect: boolean = false;
  settings!: SettingsStructure;
  
  constructor(private apiService: ApiServiceService) { }

  async ngOnInit() {
    const settings = await firstValueFrom(this.apiService.getSettings());
    if (settings) {
      this.settings = settings;
      this.failedToConnect = false;
    } else {
      this.failedToConnect = true;
      console.log("failed to retrieve data from backend!")
    }
  }

  onValueChange(value: number) {
    if (this.settings) {
      this.settings.filter_2 = value;
      this.sendDataToBackend();
    }
  }

  sendDataToBackend() {
    this.apiService.setSettings(this.settings).subscribe({
      next: (response) => {
        console.log('Settings updated successfully', response);
      },
      error: (error) => {
        console.error('Error updating settings', error);
      }
    });
  }
}
