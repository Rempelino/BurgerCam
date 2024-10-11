import { Component } from '@angular/core';
import { VideoStreamComponent } from '../video-streamer/video-streamer.component';
import { DoubleSliderComponent } from '../double-slider/double-slider.component';
import { ApiServiceService } from '../api.service';
import { MatCard, MatCardContent, MatCardTitle } from '@angular/material/card';
import { CommonModule } from '@angular/common';
import { MatCheckbox } from '@angular/material/checkbox';
import { FormsModule } from '@angular/forms';
import { MatIcon } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ToggleButtonComponent } from '../toggle-button/toggle-button.component';

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
    MatProgressSpinnerModule,
    MatCardContent,
    ToggleButtonComponent
  ],
  templateUrl: './cam-settings.component.html',
  styleUrl: './cam-settings.component.scss'
})
export class CamSettingsComponent {

  constructor(public API: ApiServiceService) { API.getSettings();}
}
