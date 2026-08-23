#!/bin/sh
set -e

# Migrations are idempotent (alembic tracks the applied revision), so running
# them on every start keeps a fresh database and an existing one on the same
# footing. Set RUN_MIGRATIONS=0 to skip — e.g. when several API replicas start
# at once, or when migrating is a separate deploy step.
if [ "${RUN_MIGRATIONS:-1}" = "1" ]; then
    echo "[entrypoint] alembic upgrade head"
    alembic upgrade head
fi

exec "$@"
