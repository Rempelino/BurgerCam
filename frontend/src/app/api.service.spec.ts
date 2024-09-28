import { TestBed } from '@angular/core/testing';
import { ApiServiceService } from './api.service';

describe('ApiService', () => {
  let service: ApiServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ApiServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
