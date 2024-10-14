// src/app/version.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

interface VersionFile {
  version: string;
}

@Injectable({
  providedIn: 'root'
})
export class VersionService {
  constructor(private http: HttpClient) {}

  getVersion(): Observable<string> {
    return this.http.get<VersionFile>('assets/version.json').pipe(
      map(data => data.version)
    );
  }
}