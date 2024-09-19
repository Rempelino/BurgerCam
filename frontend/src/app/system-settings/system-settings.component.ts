import { Component, OnInit } from '@angular/core';
import { SettingsStructure } from '../setings-interface';
import { firstValueFrom } from 'rxjs';
import { ApiServiceService } from '../api-service.service';
import { Router } from '@angular/router'

@Component({
  selector: 'app-system-settings',
  templateUrl: './system-settings.component.html',
  styleUrl: './system-settings.component.css'
})
export class SystemSettingsComponent implements OnInit{
  settings!: SettingsStructure;
  isLoading: boolean = true;
  failedToConnect: boolean = false;

  constructor(private apiService: ApiServiceService, private router: Router) { }

  async ngOnInit() {
    const settings = await firstValueFrom(this.apiService.getSettings());
    console.log('Raw settings received:', settings);
        if (settings) {
          this.settings = settings;
          console.log('Settings updated:', settings);
          this.isLoading = false;
          this.failedToConnect = false;
        } else {
          this.failedToConnect = true;
          this.isLoading = false;
        }
  }

  onMinCutoutChange(value: number) {
    if (this.settings) {
      this.settings.frame_cutout.min = value;
      this.sendDataToBackend();
    }
  }

  onMaxCutoutChange(value: number) {
    if (this.settings) {
      this.settings.frame_cutout.max = value;
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
