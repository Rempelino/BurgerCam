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
import versionInfo from '../version.json';


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
  version: string = versionInfo.version;
  constructor(public API: ApiServiceService) { }
  title = 'Burger Cam';
}
