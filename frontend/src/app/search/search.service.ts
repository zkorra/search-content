import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class SearchService {
  constructor(private http: HttpClient) {}

  fetchCustomSearch(searchParams: any): any {
    let params = new HttpParams();
    params = searchParams;

    return this.http.get<any>(`${environment.backendUrl}/fetch_custom_search`, {
      params,
    });
  }

  fetchHistory(): any {
    return this.http.get<any>(`${environment.backendUrl}/history`);
  }

  loadContentFile(filename: string): any {
    return this.http.get<any>(
      `${environment.backendUrl}/history?file=${filename}`
    );
  }

  deleteHistory(id: string): any {
    return this.http.delete<any>(`${environment.backendUrl}/history?id=${id}`);
  }

  checkHistory(searchParams: any): any {
    let params = new HttpParams();
    params = searchParams;

    return this.http.get<any>(`${environment.backendUrl}/history`, {
      params,
    });
  }

  saveSelectedContent(payload: any): any {
    return this.http.post<any>(`${environment.backendUrl}/history`, payload);
  }
}
