import { Injectable, OnDestroy } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { SettingsStructure, State } from './app.interface';
import { environment } from '../enviroments/enviroment';
import { interval, Subscription } from 'rxjs';
import { switchMap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ApiServiceService implements OnDestroy {
  private apiUrl = environment.apiUrl + '/api';
  public settings!: SettingsStructure;
  public state!: State;
  private pollSubscription!: Subscription;

  constructor(private http: HttpClient) {
    this.pollSettings();
    this.pollState();
  }

  ngOnDestroy() {
    if (this.pollSubscription) {
      this.pollSubscription.unsubscribe();
    }
  }

  private pollSettings() {
    this.pollSubscription = interval(5000) // Poll every 1000ms (1 second)
      .pipe(
        switchMap(() => this.http.get<SettingsStructure>(`${this.apiUrl}/settings`))
      )
      .subscribe({
        next: (settings) => {
          if (settings) {
            this.settings = settings;
          }
        },
        error: (error) => {
          console.error('Error fetching settings:', error);
        }
      });
  }

  public setSettings() {
    const url = `${this.apiUrl}/set_settings`;
    this.http.post<any>(url, this.settings).subscribe({
      next: (response) => {
        //console.log('Settings updated successfully', response);
      },
      error: (error) => {
        console.error('Error updating settings', error);
      }
    });
  }

  private pollState() {
    this.pollSubscription = interval(5000) // Poll every 1000ms (1 second)
      .pipe(
        switchMap(() => this.http.get<State>(`${this.apiUrl}/state`))
      )
      .subscribe({
        next: (state) => {
          if (state) {
            this.state = state;
          }
        },
        error: (error) => {
          console.error('Error fetching state:', error);
        }
      });
  }

}