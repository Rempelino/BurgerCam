import { Component } from '@angular/core';
import { VideoStreamComponent } from '../video-streamer/video-streamer.component';
import { MatCard, MatCardContent, MatCardTitle } from '@angular/material/card';
import { CommonModule } from '@angular/common';
import { ApiServiceService } from '../api.service';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-live-view',
  standalone: true,
  imports: [VideoStreamComponent,
    MatCard,
    MatCardContent,
    MatCardTitle,
    CommonModule,
    MatProgressSpinnerModule
  ],
  templateUrl: './live-view.component.html',
  styleUrl: './live-view.component.scss'
})
export class LiveViewComponent {
  constructor(public API: ApiServiceService) { API.getSettings();}
}
