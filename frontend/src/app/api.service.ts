import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject, of } from 'rxjs';
import { SettingsStructure } from './setings-interface';
import { catchError, tap, switchMap } from 'rxjs/operators';
import { environment } from '../enviroments/enviroment';

@Injectable({
  providedIn: 'root'
})
export class ApiServiceService {
  private apiUrl = environment.apiUrl + '/api';
  private settingsSubject = new BehaviorSubject<SettingsStructure | null>(null);

  constructor(private http: HttpClient) {}

  public getSettings(): Observable<SettingsStructure | null> {
    return this.fetchSettingsFromBackend();
  }

  private fetchSettingsFromBackend(): Observable<SettingsStructure | null> {
    return this.http.get<SettingsStructure>(`${this.apiUrl}/settings`).pipe(
      tap(data => {
        this.settingsSubject.next(data);
      }),
      catchError(error => {
        this.settingsSubject.next(null);
        return of(null);
      })
    );
  }

  public setSettings(settings: SettingsStructure): Observable<any> {
    const url = `${this.apiUrl}/set_settings`;
    
    return this.http.post<any>(url, settings);
  }
}