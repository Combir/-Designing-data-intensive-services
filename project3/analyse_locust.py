import os
import pandas as pd

csv_file = "../project2/locust_module3_stats.csv"

if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
    agg = df[df["Name"] == "Aggregated"]
    
    if not agg.empty:
        total_requests = int(agg.iloc[0]["Request Count"])
        failure_count = int(agg.iloc[0]["Failure Count"])
        fail_percent = (failure_count / total_requests * 100) if total_requests > 0 else 0
        rps = float(agg.iloc[0]["Requests/s"])
        p50 = float(agg.iloc[0]["50%"])
        p95 = float(agg.iloc[0]["95%"])
        
        print("Результаты нагрузочного тестирования (Locust):")
        print(f"  ✓ Обработано запросов : {total_requests}")
        print(f"  ✓ Процент ошибок      : {int(fail_percent)}%")
        print(f"  ✓ Пропускная способность: {rps:.2f} RPS")
        print(f"  ✓ Медиана отклика (p50): {int(p50)} ms")
        print(f"  ✓ 95% запросов (p95)   : {int(p95)} ms")
    else:
        print("Ошибка: В CSV-файле не найдена строка 'Aggregated'.")
else:
    print(f"Файл {csv_file} не найден. Проверьте путь к файлу.")