import { TestBed } from '@angular/core/testing';

import { Cotizaciones } from './cotizaciones';

describe('Cotizaciones', () => {
  let service: Cotizaciones;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Cotizaciones);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
