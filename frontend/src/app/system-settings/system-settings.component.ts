import { Component } from '@angular/core';
import { ToggleButtonComponent } from "../toggle-button/toggle-button.component";

@Component({
  selector: 'app-system-settings',
  standalone: true,
  imports: [ToggleButtonComponent, ToggleButtonComponent],
  templateUrl: './system-settings.component.html',
  styleUrl: './system-settings.component.scss'
})
export class SystemSettingsComponent {
  label1: string = "JUHU";
  value1: boolean = true;

  onChange(){
    this.label1 = this.label1 + "!"
  }
}
