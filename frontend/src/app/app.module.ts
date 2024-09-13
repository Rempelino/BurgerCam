import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { LayoutModule } from '@angular/cdk/layout';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';
import { MatCardModule } from '@angular/material/card';
import { MatSliderModule } from '@angular/material/slider';
import { MatSelectModule } from '@angular/material/select';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { FormsModule } from '@angular/forms';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ScrollingModule } from '@angular/cdk/scrolling';
import { MatDialogModule } from '@angular/material/dialog';
import { AppRoutingModule } from './app-routing.module';
import { VideoStreamComponent } from './videostreamer/videostreamer.component';
import { LiveViewComponent } from './live-view/live-view.component';
import { SystemSettingsComponent } from './system-settings/system-settings.component';
import { FilterSettingsColorComponent } from './filter-settings-colour/filter-settings.component';
import { FilterSettingsF1Component } from './filter-settings-f1/filter-settings.component';
import { FilterSettingsF2Component } from './filter-settings-f2/filter-settings.component';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { DoubleSliderComponent } from './double-slider/double-slider.component';
import { ApiServiceService } from './api-service.service';

@NgModule({
  declarations: [
    AppComponent,
    LiveViewComponent,
    SystemSettingsComponent,
    FilterSettingsColorComponent,
    FilterSettingsF1Component,
    FilterSettingsF2Component,
    DoubleSliderComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    LayoutModule,
    MatToolbarModule,
    MatButtonModule,
    MatSidenavModule,
    MatIconModule,
    MatListModule,
    MatCardModule,
    MatSliderModule,
    MatSelectModule,
    MatCheckboxModule,
    MatInputModule,
    FormsModule,
    MatProgressSpinnerModule,
    ScrollingModule,
    MatDialogModule,
    AppRoutingModule,
    VideoStreamComponent,
    HttpClientModule
  ],
  providers: [
    provideAnimationsAsync(),
    ApiServiceService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }