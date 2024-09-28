import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CamSettingsComponent } from './cam-settings.component';

describe('CamSettingsComponent', () => {
  let component: CamSettingsComponent;
  let fixture: ComponentFixture<CamSettingsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CamSettingsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CamSettingsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
