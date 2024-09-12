import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LiveViewComponent } from './live-view/live-view.component';
import { FilterSettingsComponent } from './filter-settings/filter-settings.component';
import { SystemSettingsComponent } from './system-settings/system-settings.component';

const routes: Routes = [
  { path: '', redirectTo: '/manual', pathMatch: 'full' },
  { path: 'live-view', component: LiveViewComponent },
  { path: 'filter-settings', component: FilterSettingsComponent },
  { path: 'system-settings', component: SystemSettingsComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
