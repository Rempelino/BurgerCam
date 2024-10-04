import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { OnInit, ElementRef, Input, ViewChild } from '@angular/core';
import { SafeUrl, DomSanitizer } from '@angular/platform-browser';
import { environment } from '../../enviroments/enviroment';
import { MatCheckbox } from '@angular/material/checkbox';
import { MatFormField, MatLabel } from '@angular/material/form-field';
import { MatOption, MatSelect } from '@angular/material/select';

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
    MatOption
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
  isStreamEnabled = true;
  url = ''
  enableFrameUpdate = true;
  disable_component = false;

  filters: Filter[] = [
    {value: 'none', viewValue: 'None'},
    {value: 'mono', viewValue: 'Monochrom'},
    {value: 'filter_1', viewValue: 'Filter 1'},
    {value: 'filter_2', viewValue: 'Filter 2'},
    {value: 'pixel_counter', viewValue: 'Pixel Counter'},
  ];

  constructor(private sanitizer: DomSanitizer) { }

  ngOnInit() {
    if (this.disable_component){
      return;
    }
    this.onCheckboxChange();
    this.onSettingChange();
  }

  onCheckboxChange() {
    if (this.isStreamEnabled) {
      this.startStream();
    } else {
      this.stopStream();
    }
  }

  onSettingChange() {
    this.url = environment.apiUrl + `/setting_change?ID=${this.ID}&filter=${this.filter}&with_rows=${this.with_rows}&with_level=${this.with_level}`
    fetch(this.url)
  }

  private startStream() {
    this.url = environment.apiUrl + `/video_feed?ID=${this.ID}`
    this.updateUrl();
  }

  private stopStream() {
    this.url = "";
    this.updateUrl();
  }

  onEnableChange(value: boolean) {
    if (value) {
      this.url = environment.apiUrl + `/enableFrameUpdate`
    } else {
      this.url = environment.apiUrl + `/disableFrameUpdate`
    }
    fetch(this.url)
  }

  private updateUrl() {
    this.videoUrl = this.sanitizer.bypassSecurityTrustUrl(this.url);
  }
}