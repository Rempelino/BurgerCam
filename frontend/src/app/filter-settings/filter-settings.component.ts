import { Component, EventEmitter } from '@angular/core';


@Component({
  selector: 'app-filter-settings',
  templateUrl: './filter-settings.component.html',
  styleUrl: './filter-settings.component.css'
})
export class FilterSettingsComponent {
  value_1: number = 50;
  value_2: number = 70;
  onValue1Changed(value: number) {
    this.value_1 = value;
    console.log("updated value 1 to: ")
    console.log(value)
  }

  onValue2Changed(value: number) {
    this.value_2 = value;
    // Do something with the updated value_2
  }
}
