import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { OnInit, ElementRef, Input, ViewChild } from '@angular/core';
import { SafeUrl, DomSanitizer } from '@angular/platform-browser';
import { environment } from '../../environments/environment';
import { MatCheckbox } from '@angular/material/checkbox';
import { MatFormField, MatLabel } from '@angular/material/form-field';
import { MatOption, MatSelect } from '@angular/material/select';
import { ToggleButtonComponent } from '../toggle-button/toggle-button.component';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

interface Filter {
  value: string;
  viewValue: string;
}

@Component({
  selector: 'app-video-streamer',
  standalone: true,
  imports: [FormsModule, CommonModule,
    MatCheckbox,
    MatFormField,
    MatLabel,
    MatSelect,
    MatOption,
    ToggleButtonComponent,
    MatProgressSpinnerModule
  ],
  templateUrl: './video-streamer.component.html',
  styleUrl: './video-streamer.component.scss'
})


export class VideoStreamComponent implements OnInit {
  @ViewChild('videoContainer') videoContainer?: ElementRef;
  @Input() checkBoxLabel: string = ''
  @Input() filter: string = 'none'
  @Input() with_rows: boolean = false
  @Input() with_level: boolean = false
  @Input() ID: string = ''
  @Input() optionsAvailable: boolean = true;

  videoUrl: SafeUrl = '';
  url = ''
  enableFrameUpdate = true;
  isLoading = true;

  filters: Filter[] = [
    {value: 'none', viewValue: 'None'},
    {value: 'mono', viewValue: 'Monochrom'},
    {value: 'filter_1', viewValue: 'Filter 1'},
    {value: 'filter_2', viewValue: 'Filter 2'},
    {value: 'pixel_counter', viewValue: 'Pixel Counter'},
  ];

  constructor(private sanitizer: DomSanitizer) { }

  ngOnInit() {
    this.videoUrl = this.sanitizer.bypassSecurityTrustUrl(environment.apiUrl + `/video_feed?ID=${this.ID}`);
    this.onSettingChange();
  }

  onSettingChange() {
    this.url = environment.apiUrl + `/setting_change?ID=${this.ID}&filter=${this.filter}&with_rows=${this.with_rows}&with_level=${this.with_level}`
    fetch(this.url)
  }

  onImageLoad() {
    this.isLoading = false;
  }

  // New method to handle image error event
  onImageError() {
    this.isLoading = false;
    // You might want to show an error message or placeholder image here
  }
}