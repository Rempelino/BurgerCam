import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FilterSettingsF1Component } from './filter-settings.component';

describe('FilterSettingsComponent', () => {
  let component: FilterSettingsF1Component;
  let fixture: ComponentFixture<FilterSettingsF1Component>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FilterSettingsF1Component]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FilterSettingsF1Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
