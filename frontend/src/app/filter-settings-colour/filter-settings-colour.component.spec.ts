import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FilterSettingsColourComponent } from './filter-settings-colour.component';

describe('FilterSettingsColourComponent', () => {
  let component: FilterSettingsColourComponent;
  let fixture: ComponentFixture<FilterSettingsColourComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FilterSettingsColourComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FilterSettingsColourComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
