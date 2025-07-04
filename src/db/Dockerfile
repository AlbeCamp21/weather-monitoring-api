# Stage 1: Setup stage
FROM postgres:15 as setup

# Copiar script de inicialización a una ruta más legible
COPY init.sql /scripts/init.sql

# Stage 2: Production stage
FROM postgres:15 as production

# Copiar scripts desde el stage anterior
COPY --from=setup /scripts/init.sql /docker-entrypoint-initdb.d/init.sql

# Exponer puerto
EXPOSE 5432