import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-double-slider',
  templateUrl: './double-slider.component.html',
  styleUrls: ['./double-slider.component.css']
})
export class DoubleSliderComponent {
  @Input() value1: number = 0;
  @Input() value2: number = 0;
  @Input() label1: string = "";
  @Input() label2: string = "";
  @Input() isSingleSlider: boolean = false;
  @Input() maxValue: number = 255;

  @Output() value1Changed = new EventEmitter<number>();
  @Output() value2Changed = new EventEmitter<number>();

  onValue1Change(value: number) {
    if (this.isSingleSlider) {
      value = Math.max(Math.min(value, this.maxValue), 0);
    } else {
      value = Math.max(Math.min(value, this.value2), 0);
    }
    this.value1 = value;
    this.value1Changed.emit(this.value1);
  }

  onValue2Change(value: number) {
    value = Math.max(Math.min(value, this.maxValue), this.value1);
    this.value2 = value;
    this.value2Changed.emit(this.value2);
  }
}