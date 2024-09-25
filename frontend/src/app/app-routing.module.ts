import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LiveViewComponent } from './live-view/live-view.component';
import { FilterSettingsColorComponent } from './filter-settings-colour/filter-settings.component';
import { FilterSettingsF1Component } from './filter-settings-f1/filter-settings.component';
import { FilterSettingsF2Component } from './filter-settings-f2/filter-settings.component';
import { SystemSettingsComponent } from './system-settings/system-settings.component';
import { CamSettingsComponent } from './cam-settings/cam-settings.component';

const routes: Routes = [
  { path: '', component: LiveViewComponent },
  { path: 'live-view', component: LiveViewComponent },
  { path: 'filter-settings-colour', component: FilterSettingsColorComponent },
  { path: 'filter-settings-f1', component: FilterSettingsF1Component },
  { path: 'filter-settings-f2', component: FilterSettingsF2Component },
  { path: 'cam-settings', component: CamSettingsComponent },
  { path: 'system-settings', component: SystemSettingsComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
