import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VideostreamerComponent } from './videostreamer.component';

describe('VideostreamerComponent', () => {
  let component: VideostreamerComponent;
  let fixture: ComponentFixture<VideostreamerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [VideostreamerComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(VideostreamerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
