import pandas as pd
import mysql.connector
import math
import os

# Configurações
csv_file = "data/caso_full.csv"
chunksize = 10000

# Conexão com o banco
conn = mysql.connector.connect(
    host="localhost",
    user="martinssxg",       # altere se o usuário for diferente
    password="Biel*2302",     # coloque sua senha
    database="meus_dados"
)
cursor = conn.cursor()

# Criação da tabela (caso não exista)
cursor.execute("""
CREATE TABLE IF NOT EXISTS casos_covid (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(255),
    date DATE,
    new_deaths INT,
    new_confirmed INT,
    last_available_deaths INT,
    last_available_confirmed INT,
    estimated_population INT
);
""")

# Função para limpar valores antes de inserir no MySQL
def clean_value(val):
    if val is None:
        return None
    if isinstance(val, float) and math.isnan(val):
        return None
    return val

# Colunas do CSV que serão inseridas
cols = [
    "city", "date", "new_deaths", "new_confirmed",
    "last_available_deaths", "last_available_confirmed",
    "estimated_population"
]

# SQL para inserção em lote
sql = f"""
INSERT INTO casos_covid ({', '.join(cols)})
VALUES ({', '.join(['%s'] * len(cols))})
"""

# Processa o CSV em chunks
for chunk in pd.read_csv(csv_file, chunksize=chunksize):
    # Substitui NaN por None
    chunk = chunk.where(pd.notnull(chunk), None)

    # Prepara dados para inserção
    data = [
        tuple(clean_value(row[col]) for col in cols)
        for _, row in chunk.iterrows()
    ]

    # Insere no banco em lote
    cursor.executemany(sql, data)
    conn.commit()
    print(f"{len(data)} linhas inseridas...")

# Fecha conexão
cursor.close()
conn.close()

print("✅ Dados importados com sucesso!")
