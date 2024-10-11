import { Injectable, OnDestroy } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { SettingsStructure, State } from './app.interface';
import { environment } from '../environments/environment';
import { interval, Subscription } from 'rxjs';
import { switchMap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ApiServiceService implements OnDestroy {
  //private apiUrl = environment.apiUrl + '/api';
  private apiUrl = environment.apiUrl;
  public settings!: SettingsStructure;
  public state!: State;
  private pollSubscription!: Subscription;

  constructor(private http: HttpClient) {
    this.getSettings();
    this.getState();
    this.pollState();
  }

  ngOnDestroy() {
    if (this.pollSubscription) {
      this.pollSubscription.unsubscribe();
    }
  }

  private pollSettings() {
    this.pollSubscription = interval(5000)
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
      },
      error: (error) => {
        console.error('Error updating settings', error);
      }
    });
  }

  private pollState() {
    this.pollSubscription = interval(500)
      .pipe(
        switchMap(() => this.http.get<State>(`${this.apiUrl}/state`))
      )
      .subscribe({
        next: (state) => {
          if (state) {
            this.state = state;
            if (this.state.frontend_update_required){
              this.getSettings();
            }
          }
        },
        error: (error) => {
          console.error('Error fetching state:', error);
        }
      });
  }

  public getSettings(): void {
    this.http.get<SettingsStructure>(`${this.apiUrl}/settings`).subscribe(
      settings => this.settings = settings
    );
  }

  public getState(): void {
    this.http.get<State>(`${this.apiUrl}/state`).subscribe(
      state => this.state = state
    );
  }

}