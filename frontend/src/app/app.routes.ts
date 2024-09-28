import { Routes } from '@angular/router';
import { LiveViewComponent } from './live-view/live-view.component';
import { FilterSettingsColourComponent } from './filter-settings-colour/filter-settings-colour.component';
import { FilterSettingsF1Component } from './filter-settings-f1/filter-settings-f1.component';
import { FilterSettingsF2Component } from './filter-settings-f2/filter-settings-f2.component';
import { CamSettingsComponent } from './cam-settings/cam-settings.component';
import { SystemSettingsComponent } from './system-settings/system-settings.component';

export const routes: Routes = [
  { path: 'live-view', component: LiveViewComponent },
  { path: 'filter-settings-colour', component: FilterSettingsColourComponent },
  { path: 'filter-settings-f1', component: FilterSettingsF1Component },
  { path: 'filter-settings-f2', component: FilterSettingsF2Component },
  { path: 'cam-settings', component: CamSettingsComponent },
  { path: 'system-settings', component: SystemSettingsComponent },
  { path: '', redirectTo: '/live-view', pathMatch: 'full' },
  { path: '**', redirectTo: '/live-view' }
];