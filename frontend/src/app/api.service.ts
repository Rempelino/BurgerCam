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
  public availableLogs: string[] = [];
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


  public dataOK() {
    return !!this.settings && !!this.state
  }

  private pollState() {
    this.pollSubscription = interval(500)
      .pipe(
        switchMap(() => this.http.get<State>(`${this.apiUrl}/get_state`))
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
    this.http.get<SettingsStructure>(`${this.apiUrl}/get_settings`).subscribe(
      settings => this.settings = settings
    );
  }

  public getState(): void {
    this.http.get<State>(`${this.apiUrl}/get_state`).subscribe(
      state => {this.state = state}
    );
  }

  public getAvailableLogs(): void {
    this.http.get<string[]>(`${this.apiUrl}/get_available_logs`).subscribe(
      logs => {
        this.availableLogs = logs;
      }
    );
  }

  public startLog(): void {
    this.http.get<any>(`${this.apiUrl}/start_log`).subscribe({
      next: (response) => {
        console.log('Logging started successfully', response);
        // You can handle the response here if needed
      },
      error: (error) => {
        console.error('Error starting log', error);
        // Handle error (e.g., show an error message to the user)
      }
    });
  }

  public startReplay(replay: string) {
    const url = `${this.apiUrl}/start_replay`;
    this.http.post<string>(url, {replay: replay}).subscribe({
      next: (response) => {
      },
      error: (error) => {
        console.error('Error sending replay command', error);
      }
    });
  }

  public stopReplay(): void {
    this.http.get<string[]>(`${this.apiUrl}/stop_replay`).subscribe(
      response => { }
    );
  }
}