import { Routes } from '@angular/router';
import { Cotizaciones } from './pages/cotizaciones/cotizaciones';

export const routes: Routes = [
  { path: '', redirectTo: 'cotizaciones', pathMatch: 'full' },
  { path: 'cotizaciones', component: Cotizaciones },
];