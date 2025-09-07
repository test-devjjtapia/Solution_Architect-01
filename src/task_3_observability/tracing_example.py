# -*- coding: utf-8 -*-
"""
Ejemplo de Trazado Distribuido (Distributed Tracing) con OpenTelemetry.

Este script muestra cómo instrumentar una aplicación Python para generar trazas (traces).
Las trazas permiten visualizar el flujo de una petición a través de múltiples microservicios,
siendo una herramienta fundamental para la observabilidad.

El ejemplo configura un "Tracer" que exporta las trazas a la consola, pero en un
entorno real, se configuraría para exportar a un colector como Jaeger u OpenTelemetry Collector.
"""

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,       # Exporta a la consola
    SimpleSpanProcessor
)
from opentelemetry.sdk.resources import Resource

# --- Configuración de OpenTelemetry ---

# 1. Define un recurso para identificar el servicio que genera las trazas.
resource = Resource(attributes={
    "service.name": "my-billing-microservice"
})

# 2. Configura el proveedor de trazas.
provider = TracerProvider(resource=resource)

# 3. Configura un procesador para enviar las trazas a un exportador.
#    SimpleSpanProcessor es bueno para debugging, en producción se usaría BatchSpanProcessor.
processor = SimpleSpanProcessor(ConsoleSpanExporter()) # Imprime en consola
provider.add_span_processor(processor)

# 4. Establece el proveedor de trazas global.
trace.set_tracer_provider(provider)

# 5. Obtiene un "tracer" para este módulo específico.
#    El nombre del tracer es una convención para saber de dónde vienen las trazas.
tracer = trace.get_tracer("billing.service.api.v1")

def process_payment(payment_data):
    """
    Procesa un pago, creando "spans" para cada operación importante.
    Un "span" representa una unidad de trabajo (ej. una función, una llamada de red).
    """
    # Inicia un "span" padre que engloba toda la operación de procesamiento.
    with tracer.start_as_current_span("process_payment") as parent_span:
        # Se pueden añadir atributos a los spans para darles contexto.
        parent_span.set_attribute("payment.id", payment_data.get("id"))
        parent_span.set_attribute("payment.amount", payment_data.get("amount"))
        print(f"Iniciando procesamiento para el pago {payment_data.get('id')}.")

        # Crea un span hijo para la validación de datos.
        with tracer.start_as_current_span("validate_payment_data") as validation_span:
            print("Validando datos del pago...")
            # ... Lógica de validación ...
            validation_span.set_attribute("validation.status", "success")

        # Otro span hijo para la llamada a la pasarela de pago.
        with tracer.start_as_current_span("call_payment_gateway") as gateway_span:
            print("Contactando a la pasarela de pago...")
            # ... Lógica de la llamada a la API externa ...
            gateway_span.set_attribute("gateway.name", "Stripe")
            gateway_span.set_attribute("http.status_code", 200)

        # Se pueden añadir "eventos" a un span para marcar puntos en el tiempo.
        parent_span.add_event("Pago procesado y registrado en la base de datos.")
        print("Pago procesado exitosamente.")

if __name__ == "__main__":
    print("Iniciando simulación de procesamiento de pago con tracing.")
    payment = {
        "id": "pay-xyz-12345",
        "amount": 150.75,
        "currency": "EUR"
    }
    process_payment(payment)
    print("\nRevisa la consola para ver la traza generada por OpenTelemetry.")
