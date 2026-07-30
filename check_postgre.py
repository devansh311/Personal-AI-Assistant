import psycopg

conn = psycopg.connect(
    "postgresql://admin:password@localhost:5433/aiassistant"
)

print("✅ PostgreSQL Connected Successfully!")

conn.close()