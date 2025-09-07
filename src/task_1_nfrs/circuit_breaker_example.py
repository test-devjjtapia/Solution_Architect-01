# -*- coding: utf-8 -*-
"""
Ejemplo de Implementación del Patrón Circuit Breaker.

Este script demuestra cómo proteger una llamada de red a un sistema externo (legacy)
utilizando un Circuit Breaker. Si el sistema externo falla repetidamente, el "circuito" se abre,
evitando nuevas llamadas y permitiendo que el sistema se recupere.
"""

import pybreaker
import requests
import time

# --- Configuración del Circuit Breaker ---
# Se abre después de 5 fallos consecutivos.
# El circuito permanecerá abierto (en estado de "fallback") durante 60 segundos.
breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60)

def legacy_api_call(data):
    """
    Simula una llamada a una API de un sistema legacy (SOAP, SAP, etc.).
    Esta función está diseñada para fallar y demostrar el Circuit Breaker.

    Args:
        data (dict): Datos para enviar en la petición.

    Returns:
        dict: La respuesta JSON de la API.

    Raises:
        requests.exceptions.RequestException: Si la llamada de red falla.
    """
    print("Intentando conectar con http://legacy-system.local/api...")
    # Esta URL no existe, por lo que la llamada siempre fallará.
    response = requests.post("http://legacy-system.local/api", json=data, timeout=2)
    response.raise_for_status()  # Lanza una excepción para errores HTTP (4xx o 5xx)
    return response.json()

@breaker
def protected_legacy_call(order_data):
    """
    Función wrapper que está protegida por el Circuit Breaker.
    Cualquier excepción levantada por `legacy_api_call` será contada como un fallo por el breaker.

    Args:
        order_data (dict): Datos de la orden a procesar.

    Returns:
        dict: Resultado de la llamada a la API.

    Raises:
        pybreaker.CircuitBreakerError: Si el circuito está abierto.
        requests.exceptions.RequestException: Si la llamada de red falla.
    """
    try:
        return legacy_api_call(order_data)
    except requests.exceptions.RequestException as e:
        # Se relanza la excepción para que pybreaker la capture como un fallo.
        raise e

if __name__ == "__main__":
    print("Iniciando simulación de llamadas a sistema legacy protegido por Circuit Breaker.")
    order_payload = {"customer_id": 123, "amount": 99.99}
    
    # Realizar 10 llamadas para ver el comportamiento del breaker
    for i in range(10):
        print(f"\n--- Intento de llamada #{i + 1} ---")
        try:
            result = protected_legacy_call(order_payload)
            print(f"Resultado: {result}")
        except requests.exceptions.RequestException as e:
            print(f"Error capturado: La llamada a la API falló. {e}")
        except pybreaker.CircuitBreakerError as e:
            print(f"Error capturado: ¡El circuito está abierto! Las llamadas están bloqueadas. {e}")
            if i == breaker.fail_max:
                print("El circuito se abrirá por 60 segundos. Las siguientes llamadas fallarán inmediatamente.")
        
        time.sleep(2)
