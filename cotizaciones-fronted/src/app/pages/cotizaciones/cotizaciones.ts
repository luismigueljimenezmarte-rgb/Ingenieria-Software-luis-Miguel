import { Component, OnInit } from '@angular/core';
import { CotizacionesService, Cotizacion } from '../../services/cotizaciones';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-cotizaciones',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './cotizaciones.html',
})
export class Cotizaciones implements OnInit {

  items: Cotizacion[] = [];

  loading: boolean = true;

  error: string = '';   // ← ESTA LÍNEA ES LA SOLUCIÓN

  constructor(private api: CotizacionesService) {}

 ngOnInit(): void {
  this.api.list().subscribe({
    next: (data: any) => {

      console.log("DATA RECIBIDA:", data);

      // Maneja ambos casos: array directo o paginado
      if (Array.isArray(data)) {
        this.items = data;
      } else if (data.results) {
        this.items = data.results;
      } else {
        this.items = [];
      }

      console.log("ITEMS:", this.items);

      this.loading = false;
    },

    error: (err) => {
      console.error("ERROR API:", err);
      this.error = "Error cargando cotizaciones";
      this.loading = false;
    }
  });
}

}