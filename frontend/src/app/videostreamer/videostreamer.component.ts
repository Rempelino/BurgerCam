import { Component, OnInit, OnDestroy, ElementRef, ViewChild, AfterViewInit, Input } from '@angular/core';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-video-stream',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './videostreamer.component.html'
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
    console.log(this.checkBoxLabel);
    console.log(this.filter);
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
    this.url = `http://localhost:5000/setting_change?ID=${this.ID}&filter=${this.filter}&with_rows=${this.with_rows}&with_level=${this.with_level}`
    fetch(this.url)
  }

  private startStream() {
    this.url = `http://localhost:5000/video_feed?ID=${this.ID}`
    this.updateUrl();
  }

  private stopStream() {
    this.url = "";
    this.updateUrl();
  }

  onEnableChange(value: boolean) {
    if (value) {
      this.url = `http://localhost:5000/enableFrameUpdate`
    } else {
      this.url = `http://localhost:5000/disableFrameUpdate`
    }
    fetch(this.url)
  }

  private updateUrl() {
    this.videoUrl = this.sanitizer.bypassSecurityTrustUrl(this.url);
    console.log(`updated url to ${this.url}`)
  }
}