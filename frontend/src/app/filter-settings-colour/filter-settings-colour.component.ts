import { Component } from '@angular/core';
import { VideoStreamComponent } from '../video-streamer/video-streamer.component';
import { CommonModule } from '@angular/common';
import { ApiServiceService } from '../api.service';
import { SettingsStructure } from '../app.interface';
import { MatCard, MatCardContent, MatCardTitle } from '@angular/material/card';
import { DoubleSliderComponent } from "../double-slider/double-slider.component";
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';


@Component({
  selector: 'app-filter-settings-colour',
  standalone: true,
  imports: [VideoStreamComponent,
    CommonModule,
    MatCard,
    MatCardTitle,
    DoubleSliderComponent,
    MatCardContent,
    MatProgressSpinnerModule
  ],
  templateUrl: './filter-settings-colour.component.html',
  styleUrl: './filter-settings-colour.component.scss'
})
export class FilterSettingsColourComponent {
  settings!: SettingsStructure
  failedToConnect: boolean = false;

  constructor(public API: ApiServiceService) { API.getSettings();}
}
