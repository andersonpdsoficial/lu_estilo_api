#!/bin/bash

# Criar banco de dados de teste
docker-compose exec db psql -U postgres -c "CREATE DATABASE lu_estilo_test;"

# Aplicar migrações no banco de teste
docker-compose run --rm app alembic upgrade head 