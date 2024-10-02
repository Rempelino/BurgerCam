import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';
import { MatCardModule } from '@angular/material/card';
import { MatSlider, MatSliderModule } from '@angular/material/slider';
import { MatSelectModule } from '@angular/material/select';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { RouterModule , RouterLink, RouterLinkActive} from '@angular/router';
import { CommonModule } from '@angular/common';
import { SettingsStructure } from './app.interface';
import { firstValueFrom } from 'rxjs/internal/firstValueFrom';
import { ApiServiceService } from './api.service';
import { Subscription, interval } from 'rxjs';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule,
            RouterOutlet, 
            RouterLink, 
            RouterLinkActive,
            MatSidenavModule,
            MatListModule,
            MatIconModule,
            MatSlider,
          ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {

  constructor(private apiService: ApiServiceService) { }

  private reconnectSubscription: Subscription | null = null;

  failedToConnect: Boolean = true;
  title = 'frontend_new';
  settings!: SettingsStructure

  ngOnInit(){
    this.startPolling();
  }

  async getStatus() {
    const settings = await firstValueFrom(this.apiService.getSettings());
    if (settings) {
      this.settings = settings;
      console.log("updated settings", settings)
    }
  }

  private startPolling() {
    if (!this.reconnectSubscription) {
      this.reconnectSubscription = interval(5000).subscribe(() => {
        if (this.failedToConnect) {
          this.getStatus();
        }
      });
    }
  }

 
}
