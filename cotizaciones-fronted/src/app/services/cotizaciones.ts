import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Cotizacion {
  id: number;
  cliente: number;
  cliente_nombre?: string;
  nombre_proyecto: string;
  fecha: string;
  total: string;
}

@Injectable({
  providedIn: 'root'
})
export class CotizacionesService {

  private apiUrl = 'http://localhost:8000/cotizaciones/api/cotizaciones/';

  constructor(private http: HttpClient) {}

  list(): Observable<any> {return this.http.get<any>(this.apiUrl);
  }

}