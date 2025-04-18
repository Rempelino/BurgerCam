import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { VideoStreamComponent } from '../video-streamer/video-streamer.component';
import { DoubleSliderComponent } from "../double-slider/double-slider.component";
import { MatCard, MatCardContent, MatCardTitle } from '@angular/material/card';
import { SettingsStructure } from '../app.interface';
import { ApiServiceService } from '../api.service';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-filter-settings-f1',
  standalone: true,
  imports: [VideoStreamComponent,
    CommonModule,
    DoubleSliderComponent,
    DoubleSliderComponent,
    MatCard,
    MatCardTitle,
    MatCardContent,
    MatProgressSpinnerModule
  ],
  templateUrl: './filter-settings-f1.component.html',
  styleUrl: './filter-settings-f1.component.scss'
})

export class FilterSettingsF1Component {
  settings!: SettingsStructure
  failedToConnect: boolean = false;

  constructor(public API: ApiServiceService) { API.getSettings();}
}

