#!/bin/bash

case "$1" in
    start)
        echo "Starting services..."
        docker-compose up -d
        echo "Servicio iniciado en http://localhost:8000/docs"
        ;;
    stop)
        echo "Stopping services..."
        docker-compose down
        echo "Servicio detenido"
        ;;
    status)
        docker-compose ps
        ;;
    logs)
        docker-compose logs -f
        ;;
    *)
        echo "Usage: $0 {start|stop|status|logs}"
        exit 1
        ;;
esac
