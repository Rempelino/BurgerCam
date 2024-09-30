import { Component } from '@angular/core';
import { VideoStreamComponent } from '../video-streamer/video-streamer.component';
import { CommonModule } from '@angular/common';
import { ApiServiceService } from '../api.service';
import { firstValueFrom } from 'rxjs';
import { SettingsStructure } from '../setings-interface';
import { MatCard, MatCardTitle } from '@angular/material/card';
import { DoubleSliderComponent } from "../double-slider/double-slider.component";


@Component({
  selector: 'app-filter-settings-colour',
  standalone: true,
  imports: [VideoStreamComponent,
    CommonModule,
    MatCard,
    MatCardTitle,
    DoubleSliderComponent
  ],
  templateUrl: './filter-settings-colour.component.html',
  styleUrl: './filter-settings-colour.component.css'
})
export class FilterSettingsColourComponent {
  settings!: SettingsStructure
  failedToConnect: boolean = false;

  constructor(private apiService: ApiServiceService) { }

  async ngOnInit() {
    this.failedToConnect = true;
    const settings = await firstValueFrom(this.apiService.getSettings());
    if (settings) {
      console.log("received settings", settings);
      this.settings = settings;
      this.failedToConnect = false;
    } else {
      this.failedToConnect = true;
      console.log("failed to retrieve data from backend!")
    }
  }

  onHueMinChanged(value: number) {
    if (this.settings) {
      this.settings.colourFilter.hue.min = value;
      this.sendDataToBackend();
    }
  }

  onHueMaxChanged(value: number) {
    if (this.settings) {
      this.settings.colourFilter.hue.max = value;
      this.sendDataToBackend();
    }
  }

  onSatMinChanged(value: number) {
    if (this.settings) {
      this.settings.colourFilter.saturation.min = value;
      this.sendDataToBackend();
    }
  }

  onSatMaxChanged(value: number) {
    if (this.settings) {
      this.settings.colourFilter.saturation.max = value;
      this.sendDataToBackend();
    }
  }

  onValueMinChanged(value: number) {
    if (this.settings) {
      this.settings.colourFilter.value.min = value;
      this.sendDataToBackend();
    }
  }

  onValueMaxChanged(value: number) {
    if (this.settings) {
      this.settings.colourFilter.value.max = value;
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
