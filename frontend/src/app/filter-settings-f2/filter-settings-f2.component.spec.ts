import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FilterSettingsF2Component } from './filter-settings-f2.component';

describe('FilterSettingsF2Component', () => {
  let component: FilterSettingsF2Component;
  let fixture: ComponentFixture<FilterSettingsF2Component>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FilterSettingsF2Component]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FilterSettingsF2Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
