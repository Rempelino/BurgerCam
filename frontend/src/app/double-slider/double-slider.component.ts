import { CommonModule } from '@angular/common';
import { Component, Input, Output, EventEmitter, forwardRef } from '@angular/core';
import { FormsModule, NG_VALUE_ACCESSOR, ControlValueAccessor } from '@angular/forms';
import { MatCard, MatCardContent } from '@angular/material/card';
import { MatFormField, MatLabel } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSlider, MatSliderModule } from '@angular/material/slider';

@Component({
  selector: 'app-double-slider',
  standalone: true,
  imports: [CommonModule,
    FormsModule,
    MatCard,
    MatCardContent,
    MatLabel,
    MatFormField,
    MatSliderModule,
    MatInputModule
  ],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => DoubleSliderComponent),
      multi: true
    }
  ],
  templateUrl: './double-slider.component.html',
  styleUrl: './double-slider.component.css'
})
export class DoubleSliderComponent {
  @Input() value1: number = 0;
  @Input() value2: number = 0;
  @Input() label1: string = "";
  @Input() label2: string = "";
  @Input() isSingleSlider: boolean = false;
  @Input() minValue: number = 0;
  @Input() maxValue: number = 255;

  @Output() value1Changed = new EventEmitter<number>();
  @Output() value2Changed = new EventEmitter<number>();

  onValue1Change(value: number) {
    if (this.isSingleSlider) {
      value = Math.max(Math.min(value, this.maxValue), this.minValue);
    } else {
      value = Math.max(Math.min(value, this.value2), this.minValue);
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
