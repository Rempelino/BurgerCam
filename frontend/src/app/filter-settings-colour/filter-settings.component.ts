import { Component, OnInit } from '@angular/core';
import { SettingsStructure, ColourFilter } from '../setings-interface';
import { ApiServiceService } from '../api-service.service';
import { Router } from '@angular/router'

@Component({
  selector: 'app-filter-settings-color',
  templateUrl: './filter-settings.component.html',
  styleUrl: './filter-settings.component.css'
})
export class FilterSettingsColorComponent implements OnInit {
  settings!: SettingsStructure;
  filterSettings!: ColourFilter;
  isLoading: boolean = true;
  failedToConnect: boolean = false;

  constructor(private apiService: ApiServiceService, private router: Router) { }

  ngOnInit(): void {
    this.apiService.getSettings().subscribe({
      next: (settings) => {
        console.log('Raw settings received:', settings);
        if (settings) {
          this.settings = settings
          if (this.settings != null && this.settings.colourFilter) {
            this.filterSettings = this.settings.colourFilter;
            console.log("updated filter settings", this.filterSettings)
          }
          console.log('Settings updated:', settings);
          this.isLoading = false;
          this.failedToConnect = false;
        } else {
          this.failedToConnect = true;
          this.isLoading = false;
          this.reloadRoute();
        }
      },
      error: (error) => {
        console.error('Error fetching settings:', error);
        this.isLoading = false;
      }
    });
  }

  reloadRoute(): void {
    this.router.navigateByUrl('/', { skipLocationChange: true }).then(() => {
      this.router.navigate([this.router.url]);
    });
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