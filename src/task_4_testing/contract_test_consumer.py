# -*- coding: utf-8 -*-
"""
Ejemplo de Prueba de Contrato del Lado del Consumidor con Pact.

Este script define una prueba para un "Consumidor" (ej. un microservicio de Ordenes)
que depende de un "Proveedor" (ej. un microservicio de Productos).

La prueba hace lo siguiente:
1. Define la interacción esperada: El Consumidor hará una petición GET a /products/10
   y espera una respuesta 200 OK con un JSON específico.
2. Inicia un servidor mock de Pact que simulará ser el Proveedor.
3. Ejecuta el código real del Consumidor que hace la llamada HTTP.
4. El mock de Pact verifica que la petición del Consumidor coincide con lo esperado.
5. Si todo coincide, Pact genera un fichero de contrato (un JSON).

Este fichero de contrato se compartirá con el equipo del Proveedor, quienes lo usarán
para verificar que cualquier cambio que hagan en su API no rompa las expectativas
del Consumidor.
"""

import pytest
from pact import Consumer, Provider, Like
import requests

# --- Definición del Contrato ---

# Define el nombre del Consumidor (este servicio) y el Proveedor (el servicio del que depende).
pact = Consumer('OrderService').has_pact_with(Provider('ProductService'), port=1234)

@pytest.fixture(scope="session")
def pact_session():
    """Fixture de Pytest para iniciar y detener el servicio mock de Pact."""
    pact.start_service()
    yield
    pact.stop_service()

# --- Código del Consumidor ---

class ProductClient:
    """Cliente HTTP simple para obtener datos de ProductService."""
    def __init__(self, base_uri):
        self.base_uri = base_uri

    def get_product(self, product_id):
        """Obtiene los datos de un producto por su ID."""
        uri = f"{self.base_uri}/products/{product_id}"
        response = requests.get(uri)
        response.raise_for_status()
        return response.json()

# --- Prueba de Contrato ---

def test_get_product_when_it_exists(pact_session):
    """
    Prueba el caso en que un producto existe y se devuelve correctamente.
    """
    # 1. Define el estado previo requerido en el Proveedor.
    #    Esto le dice al Proveedor qué datos debe configurar para que esta prueba pase.
    # 2. Define la petición que el Consumidor hará.
    # 3. Define la respuesta que el Proveedor debe devolver.
    (pact
     .given('un producto con id 10 existe y está disponible')
     .upon_receiving('una petición para obtener los datos del producto 10')
     .with_request('GET', '/products/10')
     .will_respond_with(200, body={
         'id': 10,
         'name': Like('Laptop Gamer'), # `Like` asegura que el tipo de dato es string
         'price': Like(1500.00)       # y proporciona un valor de ejemplo.
     }))

    # 4. Ejecuta la prueba usando el mock de Pact.
    with pact:
        client = ProductClient(pact.uri)
        product = client.get_product(10)
        
        # 5. Verifica que el cliente procesa la respuesta correctamente.
        assert product['id'] == 10
        assert isinstance(product['name'], str)

    # Si la prueba es exitosa, Pact genera el fichero de contrato en el directorio `pacts`.
