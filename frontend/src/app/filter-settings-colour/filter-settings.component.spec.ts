import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FilterSettingsColorComponent } from './filter-settings.component';

describe('FilterSettingsComponent', () => {
  let component: FilterSettingsColorComponent;
  let fixture: ComponentFixture<FilterSettingsColorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FilterSettingsColorComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FilterSettingsColorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
