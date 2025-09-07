# Propuesta de Solución: Arquitectura de Integración

> **Nota:** Este documento es la resolución de un ejercicio técnico para una evaluación de Arquitecto de Soluciones, realizado en **Marzo de 2023** para una consultora en Portugal, Europa. El contenido es público y se ofrece para fines educativos y de aprendizaje.

## 1. Contexto del Problema

Se requiere diseñar una arquitectura de integración para una nueva solución SaaS que se conectará a un panorama de sistemas existente. Este panorama incluye un stack heredado (SOAP, OracleDB, SAP) y una nueva arquitectura de microservicios (REST APIs, Kafka).

La solución debe cumplir con altos estándares de **Gestión del Ciclo de Vida de la Aplicación (ALM)**, **Observabilidad**, **Requisitos No Funcionales (NFRs)** y **Cobertura de Pruebas**.

## 2. Diseño de la Arquitectura de Integración

A continuación, se detalla la estrategia para abordar cada uno de los requisitos clave. Los ejemplos de código para cada tarea se encuentran en la carpeta `src`, organizados por tarea.

### Tarea 1: Requisitos No Funcionales (NFRs)

Para garantizar la **disponibilidad, rendimiento y seguridad**, la estrategia se centra en la implementación de un **API Gateway** y una arquitectura de microservicios resiliente.

Un pilar fundamental para la disponibilidad es el **Patrón Circuit Breaker**, que aísla los fallos de sistemas externos (como el stack legacy) para que no afecten a toda la arquitectura.

> 📄 **Código de Ejemplo:** El código para este patrón se encuentra en:
> **`src/task_1_nfrs/circuit_breaker_example.py`**

### Tarea 2: Estrategia de ALM

Se implementará una estrategia de **GitOps** para automatizar y controlar el ciclo de vida de la aplicación. La integración y el despliegue continuo (CI/CD) son el motor de esta estrategia.

Un pipeline de CI/CD automatiza las pruebas, la construcción de artefactos (imágenes de contenedor) y su publicación en un registro, asegurando un proceso de entrega rápido y fiable.

> 📄 **Código de Ejemplo:** La definición de un pipeline de CI/CD para un microservicio se encuentra en:
> **`src/task_2_alm/ci_cd_pipeline.yml`**

### Tarea 3: Observabilidad

Para entender el estado interno del sistema, se implementará una estrategia de observabilidad basada en tres pilares: logging, métricas y **trazado distribuido (tracing)**.

El trazado distribuido es crucial en una arquitectura de microservicios, ya que permite seguir el flujo de una petición a través de los diferentes servicios que participan en ella, facilitando la identificación de cuellos de botella y la causa raíz de los errores.

> 📄 **Código de Ejemplo:** Una demostración de cómo instrumentar una aplicación con OpenTelemetry para generar trazas se encuentra en:
> **`src/task_3_observability/tracing_example.py`**

### Tarea 4: Cobertura de Pruebas

Se aplicará una estrategia de pirámide de pruebas. En un entorno de microservicios, las **Pruebas de Contrato (Contract Testing)** son especialmente importantes para garantizar que los servicios puedan evolucionar de forma independiente sin romper la comunicación entre ellos.

Estas pruebas aseguran que el "contrato" (el formato de los datos y la estructura de la API) entre un servicio consumidor y un proveedor se mantenga.

> 📄 **Código de Ejemplo:** Una prueba de contrato del lado del consumidor usando la herramienta Pact se encuentra en:
> **`src/task_4_testing/contract_test_consumer.py`**

### Tarea 5: Descomisionamiento y Mantenibilidad

La transición de los sistemas heredados se gestionará de forma gradual y controlada utilizando el **Patrón Strangler Fig (Fachada Estranguladora)**.

Se implementa un proxy o fachada que se antepone a los sistemas legacy y nuevos. Este proxy enruta el tráfico a la implementación nueva o a la antigua en función de la funcionalidad, permitiendo migrar el sistema pieza por pieza.

> 📄 **Código de Ejemplo:** Una implementación simple de este proxy con Flask se encuentra en:
> **`src/task_5_strangler/strangler_proxy.py`**

---

## 3. Licencia

Este proyecto se distribuye bajo la **Licencia MIT**.

```text
MIT License

Copyright (c) 2023

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
