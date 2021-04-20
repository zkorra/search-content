import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class EngineService {
  constructor(private http: HttpClient) {}

  getEngines(): any {
    return this.http.get<any>(`${environment.backendUrl}/engine`);
  }

  createEngine(payload: any): any {
    return this.http.post<any>(
      `${environment.backendUrl}/engine`,
      payload
    );
  }

  updateEngine(id: string, payload: any): any {
    return this.http.put<any>(
      `${environment.backendUrl}/engine?id=${id}`,
      payload
    );
  }

  deleteEngine(id: string): any {
    return this.http.delete<any>(
      `${environment.backendUrl}/engine?id=${id}`
    );
  }
}
