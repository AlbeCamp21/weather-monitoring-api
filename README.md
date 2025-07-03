# Weather Monitoring API

Sistema de monitoreo de clima con API pública contenerizado con Docker.

## Estructura del proyecto

```
weather-monitoring-api/
├── docker-compose.yml
├── requirements.txt
├── README.md
└── src/
    ├── app/
    │   ├── Dockerfile
    │   └── main.py
    └── db/
        ├── Dockerfile
        └── init.sql
```

## Uso

1. Ejecutar el proyecto:
```bash
docker-compose up --build
```

2. Acceder a la API:
- API: http://localhost:8000
- Base de datos: localhost:5432