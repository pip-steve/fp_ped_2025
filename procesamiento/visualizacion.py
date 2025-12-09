import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from sqlalchemy import create_engine
import urllib.parse
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

"""
Autor: Maviel Cedillo
Funcion del script:
Genera visualizaciones estadísticas a partir de la tabla 'coneval_limpio' en SQL Server.
Se generan los siguientes graficos:
- Top 10 pobreza en 3D
- Comparación de cambios más grandes (mejoraron/empeoraron) en 3D
- Relación Pobreza vs Pobreza extrema
- Evolución de indicadores con heatmap
- Cambio anual porcentual
"""

# Conexión SQL
server = "localhost\\SQLEXPRESS"
database = "datamex_coneval"
username = "sa"
password = "Maviel26"
driver = "ODBC Driver 18 for SQL Server"

params = urllib.parse.quote_plus(
    f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=no;"
)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# Cargar datos
df = pd.read_sql("SELECT * FROM coneval_limpio", engine)
ultimo_anio = df["year"].max()
primer_anio = df["year"].min()

# Estilo general
sns.set_style("whitegrid")
plt.rcParams.update({'figure.facecolor':'#f0f0f0', 'axes.facecolor':'#f9f9f9'})

# ---------- Top 10 pobreza 3D ----------
base_poverty = df[df["indicador"] == "poverty"]
top10 = base_poverty[base_poverty["year"] == ultimo_anio].sort_values("valor", ascending=False).head(10)
x_pos = range(len(top10))
colors = cm.viridis(top10["valor"]/top10["valor"].max())

fig = plt.figure(figsize=(10,6))
ax = fig.add_subplot(111, projection='3d')
ax.bar(x_pos, top10["valor"], zs=0, zdir='y', color=colors, edgecolor='black')
ax.set_xticks(x_pos)
ax.set_xticklabels(top10["state"], rotation=45, ha='right')
ax.set_ylabel('Estado')
ax.set_zlabel('Porcentaje')
ax.set_title(f"Top 10 pobreza 3D ({ultimo_anio})")
plt.show()

# ---------- Cambios más grandes 3D ----------
comp = base_poverty[base_poverty["year"].isin([primer_anio, ultimo_anio])].pivot(index="state", columns="year", values="valor").dropna()
comp["cambio"] = comp[ultimo_anio] - comp[primer_anio]

mayor = comp.sort_values("cambio", ascending=False).head(5)
mejor = comp.sort_values("cambio").head(5)

# Empeoraron 3D
fig = plt.figure(figsize=(8,5))
ax = fig.add_subplot(111, projection='3d')
x_pos = range(len(mayor))
colors = cm.plasma((mayor["cambio"] - mayor["cambio"].min()) / (mayor["cambio"].max() - mayor["cambio"].min()))
ax.bar(x_pos, mayor["cambio"], zs=0, zdir='y', color=colors, edgecolor='black')
ax.set_xticks(x_pos)
ax.set_xticklabels(mayor.index)
ax.set_title("Más empeoraron 3D")
plt.show()

# Mejoraron 3D
fig = plt.figure(figsize=(8,5))
ax = fig.add_subplot(111, projection='3d')
x_pos = range(len(mejor))
colors = cm.viridis((mejor["cambio"] - mejor["cambio"].min()) / (mejor["cambio"].max() - mejor["cambio"].min()))
ax.bar(x_pos, mejor["cambio"], zs=0, zdir='y', color=colors, edgecolor='black')
ax.set_xticks(x_pos)
ax.set_xticklabels(mejor.index)
ax.set_title("Más mejoraron 3D")
plt.show()

# ---------- Pobreza vs Extrema ----------
base_extreme = df[df["indicador"].isin(["poverty","extreme_poverty"])]
comp2 = base_extreme[base_extreme["year"] == ultimo_anio].pivot(index="state", columns="indicador", values="valor")
plt.figure(figsize=(8,6))
plt.scatter(comp2["poverty"], comp2["extreme_poverty"], s=120, c=comp2["extreme_poverty"], cmap='coolwarm', edgecolor='black')
plt.colorbar(label="Pobreza extrema")
plt.title("Pobreza vs Extrema")
plt.xlabel("Pobreza")
plt.ylabel("Extrema")
plt.show()

# ---------- Evolución heatmap ----------
tabla = df.groupby(["year","indicador"])["valor"].mean().unstack()
plt.figure(figsize=(10,6))
sns.heatmap(tabla, annot=True, fmt=".1f", cmap="YlGnBu", linewidths=0.5)
plt.title("Evolución")
plt.show()

# ---------- Cambio anual ----------
nacional = base_poverty.groupby("year")["valor"].mean().pct_change() * 100
plt.figure(figsize=(8,5))
plt.plot(nacional.index, nacional.values, marker="o", color='teal', linewidth=2)
plt.fill_between(nacional.index, nacional.values, color='teal', alpha=0.1)
plt.title("Cambio anual (%)")
plt.show()






