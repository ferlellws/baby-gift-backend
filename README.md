# BabyGift Backend
Esta es la base para el backend del aplicativo de marketplace.

## Arquitectura

El aplicativo está implementado con arquitectura serverless con el uso de la nube de AWS y programado en el lenguaje Python 3.9.

![Arquitectura BabyGift](BabyGift-Arquitectura.jpeg)

El backend está construido por microservicios con el uso de funciones Lambd (Python 3.9), API Gateway, Cognito (Gestor de usuarios y permisos) y DynamoDB.

## Pipeline
El pipeline revisa los cambios ocurridos en la rama main y realiza el despliegue en el ambiente de develop. Para desplegar en el ambiente de staging y production se realiza a través de una aprobación manual.