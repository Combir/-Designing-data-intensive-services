import subprocess

def run_psql(sql: str) -> str:
    try:
        result = subprocess.run(
            ["docker", "exec", "-i", "postgres_db", "psql", "-U", "postgres", "-d", "app_db", "-t", "-A", "-c", sql],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

print("-" * 60)
print("ИТОГОВАЯ СВОДКА ПО МОДУЛЮ ИЗ КОНТЕЙНЕРА")
print("-" * 60)
print()

db_size = run_psql("SELECT pg_size_pretty(pg_database_size('app_db'));")
print(f" Размер базы данных в PostgreSQL: {db_size}")

print("\n Количество строк в таблицах:")
for table in ["users", "products", "orders", "order_items"]:
    count = run_psql(f"SELECT COUNT(*) FROM {table};")
    print(f"  • {table}: {count}")

print("-" * 60)