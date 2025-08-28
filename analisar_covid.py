import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# Conexão com MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="martinssxg",
    password="Biel*2302",
    database="meus_dados"
)

# Carregar dados para um DataFrame
query = "SELECT city, date, new_deaths, new_confirmed FROM casos_covid"
df = pd.read_sql(query, conn)

conn.close()

# Garantir que a coluna date seja tratada como data
df["date"] = pd.to_datetime(df["date"])

# Agrupar mortes e casos por cidade
deaths_by_city = df.groupby("city")["new_deaths"].sum().sort_values(ascending=False)
cases_by_city = df.groupby("city")["new_confirmed"].sum().sort_values(ascending=False)

# ---- Gráfico 1: Mortes totais por cidade ----
plt.figure(figsize=(12,6))
deaths_by_city.head(10).plot(kind="bar", color="red")
plt.title("Top 10 cidades com mais mortes por COVID-19")
plt.xlabel("Cidade")
plt.ylabel("Total de Novas Mortes")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("relatorio_mortes.png")
plt.show()

# ---- Gráfico 2: Casos confirmados totais por cidade ----
plt.figure(figsize=(12,6))
cases_by_city.head(10).plot(kind="bar", color="blue")
plt.title("Top 10 cidades com mais casos confirmados de COVID-19")
plt.xlabel("Cidade")
plt.ylabel("Total de Novos Casos Confirmados")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("relatorio_casos.png")
plt.show()

print("✅ Análises geradas com sucesso! Arquivos salvos: relatorio_mortes.png, relatorio_casos.png")
