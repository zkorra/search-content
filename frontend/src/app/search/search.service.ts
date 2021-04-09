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

    return this.http.get<any>(`${environment.backendUrl}/fetch`, { params });
  }
}
