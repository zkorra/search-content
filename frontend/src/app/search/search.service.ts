import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class SearchService {
  constructor(private http: HttpClient) {}

  allResults: any = [];

  fetchCustomSearch(userParams: any): any {
    let params = new HttpParams();
    params = userParams;

    return this.http.get<any>(`http://127.0.0.1:8000/fetch`, { params });
  }
}
