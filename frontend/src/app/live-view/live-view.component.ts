import { Component } from '@angular/core';
import { VideoStreamComponent } from '../video-streamer/video-streamer.component';

@Component({
  selector: 'app-live-view',
  standalone: true,
  imports: [VideoStreamComponent],
  templateUrl: './live-view.component.html',
  styleUrl: './live-view.component.css'
})
export class LiveViewComponent {

}
