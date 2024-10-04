import { CommonModule } from '@angular/common';
import { Component, Input, Output, EventEmitter } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatCheckbox } from '@angular/material/checkbox';

@Component({
  selector: 'toggle-button',
  standalone: true,
  imports: [MatCheckbox, CommonModule, FormsModule],
  templateUrl: './toggle-button.component.html',
  styleUrl: './toggle-button.component.scss'
})
export class ToggleButtonComponent {
  @Input() text: string = '';
  @Input() isTicked: boolean = false;
  @Output() isTickedChange = new EventEmitter<boolean>();

  public toggle() {
    this.isTicked = !this.isTicked;
    this.isTickedChange.emit(this.isTicked);
  }
}