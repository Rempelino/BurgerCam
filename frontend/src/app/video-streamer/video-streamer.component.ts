import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { OnInit, ElementRef, Input, ViewChild } from '@angular/core';
import { SafeUrl, DomSanitizer } from '@angular/platform-browser';
import { environment } from '../../enviroments/enviroment';


@Component({
  selector: 'app-video-streamer',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './video-streamer.component.html',
  styleUrl: './video-streamer.component.css'
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

  constructor(private sanitizer: DomSanitizer) { }

  ngOnInit() {
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
