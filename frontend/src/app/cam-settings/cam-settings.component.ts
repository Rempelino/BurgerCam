import { Component } from '@angular/core';
import { VideoStreamComponent } from '../video-streamer/video-streamer.component';
import { DoubleSliderComponent } from '../double-slider/double-slider.component';
import { SettingsStructure } from '../setings-interface';
import { firstValueFrom } from 'rxjs';
import { ApiServiceService } from '../api.service';
import { MatCard, MatCardTitle } from '@angular/material/card';
import { CommonModule } from '@angular/common';
import { MatCheckbox } from '@angular/material/checkbox';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-cam-settings',
  standalone: true,
  imports: [CommonModule,
    FormsModule,
    VideoStreamComponent,
    DoubleSliderComponent,
    MatCard,
    MatCardTitle,
    MatCheckbox
  ],
  templateUrl: './cam-settings.component.html',
  styleUrl: './cam-settings.component.css'
})
export class CamSettingsComponent {
  settings!: SettingsStructure
  failedToConnect: boolean = false;

  constructor(private apiService: ApiServiceService) { }

  async ngOnInit() {
    const settings = await firstValueFrom(this.apiService.getSettings());
    console.log(this.settings)
    console.log('Raw settings received:', settings);
    if (settings) {
      this.settings = settings;
      console.log('Settings updated:', settings);
      this.failedToConnect = false;
    } else {
      this.failedToConnect = true;
    }
  }

  onExpoTimeChange(value: number) {
    if (this.settings) {
      this.settings.cam_settings.ExposureTime = value;
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
