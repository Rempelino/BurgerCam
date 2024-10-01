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
  private fetchingSettings = false;

  constructor(private http: HttpClient) { 
    this.initialize();
  }

  private initialize(): void {
    this.fetchSettingsFromBackend().subscribe();
  }

  public getSettings(): Observable<SettingsStructure | null> {
    if (this.settingsSubject.getValue() === null && !this.fetchingSettings) {
      return this.fetchSettingsFromBackend();
    }
    return this.settingsSubject.asObservable();
  }

  private fetchSettingsFromBackend(): Observable<SettingsStructure | null> {
    if (this.fetchingSettings) {
      return this.settingsSubject.asObservable();
    }
    
    this.fetchingSettings = true;
    return this.http.get<SettingsStructure>(`${this.apiUrl}/settings`).pipe(
      tap(data => {
        this.settingsSubject.next(data);
        this.fetchingSettings = false;
      }),
      catchError(error => {
        console.error('Error fetching settings:', error);
        this.settingsSubject.next(null);
        this.fetchingSettings = false;
        return of(null);
      })
    );
  }

  public setSettings(settings: SettingsStructure): Observable<any> {
    const url = `${this.apiUrl}/set_settings`;
    
    return this.http.post<any>(url, settings).pipe(
      tap(response => console.log('Settings updated successfully:', response)),
      catchError(this.handleError)
    );
  }

  private handleError(error: any) {
    console.error('An error occurred:', error);
    return new Observable((observer) => {
      observer.error('Something went wrong; please try again later.');
    });
  }
}