import pandas as pd
import urllib.parse
from sqlalchemy import create_engine

# =====================================================
# 1️⃣ CONEXIÓN A SQL SERVER
# =====================================================

params = urllib.parse.quote_plus(
    "Driver={SQL Server};"
    "Server=localhost\\SQLEXPRESS;"
    "Database=calls;"
    "Trusted_Connection=yes;"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# =====================================================
# 2️⃣ CARGAR TABLAS
# =====================================================

df_calls = pd.read_sql("SELECT * FROM calls", engine)
df_sales = pd.read_sql("SELECT * FROM group_sales", engine)

engine.dispose()

# =====================================================
# 3️⃣ CONVERTIR FECHAS
# =====================================================

df_calls["call_date"] = pd.to_datetime(df_calls["call_date"])
df_sales["booking_date"] = pd.to_datetime(df_sales["booking_date"])

# =====================================================
# 4️⃣ DATA QUALITY CHECKS – CALLS
# =====================================================

print("----- DATA QUALITY CHECKS (CALLS) -----")

print("Null values per column:\n", df_calls.isnull().sum())
print("Duplicated call_id:", df_calls["call_id"].duplicated().sum())
print("Negative wait_time_seconds:",
      (df_calls["wait_time_seconds"] < 0).sum())
print("Invalid handled values:",
      df_calls[~df_calls["handled"].isin([0, 1])].shape[0])

# =====================================================
# 5️⃣ KPI CONTACT CENTER
# =====================================================

# Crear columnas year y month
df_calls["year"] = df_calls["call_date"]
df_calls["month"] = df_calls["call_date"]

df_calls_summary = df_calls.groupby(
    ["country", "year", "month"]
).agg(
    total_calls=("call_id", "count"),
    total_handled=("handled", "sum")
)

df_calls_summary["handled_rate"] = (
    df_calls_summary["total_handled"] /
    df_calls_summary["total_calls"]
)

print("\n----- CONTACT CENTER KPI -----")
print(df_calls_summary)

# =====================================================
# 6️⃣ KPI MICE
# =====================================================

df_mice = df_sales[df_sales["segment"] == "MICE"].copy()

df_mice["year"] = df_mice["booking_date"]
df_mice["month"] = df_mice["booking_date"]

df_mice_summary = df_mice.groupby(
    ["country", "year", "month"]
).agg(
    total_mice_revenue=("revenue", "sum"),
    total_bookings=("booking_id", "count")
)

df_mice_summary["avg_revenue_per_booking"] = (
    df_mice_summary["total_mice_revenue"] /
    df_mice_summary["total_bookings"]
)

print("\n----- MICE KPI -----")
print(df_mice_summary)

# =====================================================
# 7️⃣ UNIÓN FINAL
# =====================================================

df_dashboard = df_calls_summary.merge(
    df_mice_summary,
    on=["country", "year", "month"],
    how="left"
)

print("\n----- FINAL DASHBOARD DATASET -----")
print(df_dashboard)
