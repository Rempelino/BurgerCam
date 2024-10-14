import { Component, DoCheck } from '@angular/core';
import { VideoStreamComponent } from '../video-streamer/video-streamer.component';
import { MatCard, MatCardContent, MatCardTitle } from '@angular/material/card';
import { CommonModule } from '@angular/common';
import { ApiServiceService } from '../api.service';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatFormField, MatLabel } from '@angular/material/form-field';
import { MatOption, MatSelect } from '@angular/material/select';
import { MatButton } from '@angular/material/button';
import versionInfo from '../../version.json';

@Component({
  selector: 'app-live-view',
  standalone: true,
  imports: [VideoStreamComponent,
    MatCard,
    MatCardContent,
    MatCardTitle,
    CommonModule,
    MatProgressSpinnerModule,
    MatProgressBarModule,
    MatFormField,
    MatLabel,
    MatSelect,
    MatOption,
    MatButton
  ],
  templateUrl: './live-view.component.html',
  styleUrl: './live-view.component.scss'
})
export class LiveViewComponent implements DoCheck {
  version: string = versionInfo.version;
  chosen_log: string = ''
  private previousSaveActive: boolean = false

  constructor(public API: ApiServiceService) {
    API.getSettings();
    API.getAvailableLogs();
  }

  ngDoCheck() {
    if (!this.API.dataOK()){
      return;
    }
    if (this.API.state.saving_active !== this.previousSaveActive) {
      if (this.previousSaveActive === true && this.API.state.saving_active === false) {
        this.API.getAvailableLogs()

      }
      this.previousSaveActive = this.API.state.saving_active;
    }
  }
  startLogging() {
    this.API.startLog();
  }

  toggleReplay() {
    if (!this.API.state.replay_active) {
      if (this.chosen_log != '') {
        this.API.startReplay(this.chosen_log);
      }
    } else {
      this.API.stopReplay();
    }
  }
}
