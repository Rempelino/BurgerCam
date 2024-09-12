import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DoubleSliderComponent } from './double-slider.component';

describe('DoubleSliderComponent', () => {
  let component: DoubleSliderComponent;
  let fixture: ComponentFixture<DoubleSliderComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DoubleSliderComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DoubleSliderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
