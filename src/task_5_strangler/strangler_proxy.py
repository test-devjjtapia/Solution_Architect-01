# -*- coding: utf-8 -*-
"""
Ejemplo del Patrón Strangler Fig usando un Proxy con Flask.

Este script implementa un "Facade" o "Proxy" que se coloca frente a los sistemas
nuevo y legacy. Actúa como el único punto de entrada para los clientes, ocultando
la complejidad de la migración.

El proxy enruta las peticiones de la siguiente manera:
- Las peticiones a funcionalidades ya migradas (ej. /api/invoices) se dirigen
  al nuevo microservicio.
- Las peticiones a funcionalidades aún no migradas (ej. /api/orders) se dirigen
  al sistema legacy.

Con el tiempo, más rutas se modificarán para que apunten al nuevo sistema, "estrangulando"
gradualmente al sistema legacy hasta que pueda ser desmantelado.
"""

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# --- URLs de los sistemas de backend ---
# En un entorno real, estas URLs se gestionarían a través de variables de entorno.
LEGACY_SYSTEM_URL = "http://sap-legacy-system.local/api"
NEW_BILLING_SERVICE_URL = "http://new-billing-microservice.local/api"

@app.route('/api/v1/invoices/<invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    """
    Ruta para facturas. Esta funcionalidad ya ha sido migrada.
    La petición se redirige al nuevo microservicio de facturación.
    """
    print(f"[PROXY] Petición para factura {invoice_id}. Enrutando al NUEVO servicio.")
    try:
        # Se hace una petición al nuevo microservicio, pasando la misma ruta.
        res = requests.get(f"{NEW_BILLING_SERVICE_URL}/invoices/{invoice_id}")
        res.raise_for_status() # Captura errores HTTP
        return jsonify(res.json()), res.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Error al contactar el servicio de facturación", "details": str(e)}), 503

@app.route('/api/v1/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    """
    Ruta para órdenes. Esta funcionalidad aún reside en el sistema legacy.
    La petición se redirige al backend de SAP.
    """
    print(f"[PROXY] Petición para orden {order_id}. Enrutando al sistema LEGACY.")
    try:
        # Se hace una petición al sistema legacy.
        res = requests.get(f"{LEGACY_SYSTEM_URL}/orders/{order_id}")
        res.raise_for_status()
        return jsonify(res.json()), res.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Error al contactar el sistema legacy", "details": str(e)}), 503

if __name__ == '__main__':
    # Este proxy se ejecutaría en un puerto expuesto a los clientes, como el 80 o 443.
    print("Iniciando el proxy Strangler Fig en el puerto 5000.")
    app.run(port=5000, debug=True)
