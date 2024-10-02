import { Component } from '@angular/core';
import { VideoStreamComponent } from '../video-streamer/video-streamer.component';
import { DoubleSliderComponent } from '../double-slider/double-slider.component';
import { SettingsStructure } from '../app.interface';
import { firstValueFrom, interval, Subscription } from 'rxjs';
import { ApiServiceService } from '../api.service';
import { MatCard, MatCardTitle } from '@angular/material/card';
import { CommonModule } from '@angular/common';
import { MatCheckbox } from '@angular/material/checkbox';
import { FormsModule } from '@angular/forms';
import { MatIcon } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-cam-settings',
  standalone: true,
  imports: [CommonModule,
    FormsModule,
    VideoStreamComponent,
    DoubleSliderComponent,
    MatCard,
    MatCardTitle,
    MatCheckbox,
    MatIcon,
    MatProgressSpinnerModule  
  ],
  templateUrl: './cam-settings.component.html',
  styleUrl: './cam-settings.component.css'
})
export class CamSettingsComponent {
  settings!: SettingsStructure
  failedToConnect: boolean = true;
  private reconnectSubscription: Subscription | null = null;

  constructor(private apiService: ApiServiceService) { }

  ngOnInit(){
    this.connectToBackend();
  }

  ngOnDestroy() {
    this.stopReconnection();
  }

  async connectToBackend() {
    const settings = await firstValueFrom(this.apiService.getSettings());
    if (settings) {
      this.settings = settings;
      this.stopReconnection();
    } else {
      this.startReconnection();
    }
  }

  private startReconnection() {
    this.failedToConnect = true;
    if (!this.reconnectSubscription) {
      this.reconnectSubscription = interval(5000).subscribe(() => {
        if (this.failedToConnect) {
          this.connectToBackend();
        }
      });
    }
  }

  private stopReconnection() {
    this.failedToConnect = false;
    if (this.reconnectSubscription) {
      this.reconnectSubscription.unsubscribe();
      this.reconnectSubscription = null;
    }
  }

  onExpoTimeChange(value: number) {
    if (this.settings) {
      this.settings.cam_settings.ExposureTime = value;
      this.sendDataToBackend();
    }
  }

  onCutOutMinChanged(value: number) {
    if (this.settings) {
      this.settings.frame_cutout.min = value;
      this.sendDataToBackend();
    }
  }

  onCutOutMaxChanged(value: number) {
    if (this.settings) {
      this.settings.frame_cutout.max = value;
      this.sendDataToBackend();
    }
  }

  sendDataToBackend() {
    this.apiService.setSettings(this.settings).subscribe({
      error: () => {
        this.startReconnection();
      }
    });
  }


}
