import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { SettingsStructure } from './setings-interface';
import { catchError, tap } from 'rxjs/operators';
import { environment } from '../enviroments/enviroment';

@Injectable({
  providedIn: 'root'
})
export class ApiServiceService {
  private apiUrl = environment.apiUrl + '/api';
  private settingsSubject = new BehaviorSubject<SettingsStructure | null>(null);

  constructor(private http: HttpClient) { 
    this.initialize();
  }

  private initialize(): void {
    this.fetchSettingsFromBackend();
  }

  public getSettings(): Observable<SettingsStructure | null> {
    this.fetchSettingsFromBackend();
    return this.settingsSubject.asObservable();
  }

  private fetchSettingsFromBackend(): void {
    this.http.get<SettingsStructure>(`${this.apiUrl}/settings`).subscribe({
      next: (data) => {
        this.settingsSubject.next(data);
      },
      error: (error) => {
        this.settingsSubject.next(null);
        console.error('Error fetching settings:', error);
      }
    });
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