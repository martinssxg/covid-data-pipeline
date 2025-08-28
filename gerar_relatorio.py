import pandas as pd
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os

# ====== CARREGAR CSV ======
df = pd.read_csv("data/caso_full.csv")
df = df.fillna(0)

# ====== 1) Mortes por cidade ======
mortes_por_cidade = df.groupby("city")["new_deaths"].sum().reset_index()

# ====== 2) População estimada ======
populacao = df.groupby("city")[["estimated_population", "estimated_population_2019"]].max().reset_index()

# ====== 3) Maior/Menor cidade por casos ======
casos_por_cidade = df.groupby("city")["last_available_confirmed"].max().reset_index()
maior_cidade = casos_por_cidade.loc[casos_por_cidade["last_available_confirmed"].idxmax()]
menor_cidade = casos_por_cidade.loc[casos_por_cidade["last_available_confirmed"].idxmin()]

# ====== CRIAR PASTA PARA GRÁFICOS ======
os.makedirs("relatorio/prints", exist_ok=True)

# ====== GRÁFICO DAS 10 CIDADES COM MAIS MORTES ======
top10_mortes = mortes_por_cidade.sort_values("new_deaths", ascending=False).head(10)

# Criar posições numéricas para o eixo x
x_pos = range(len(top10_mortes))

plt.figure(figsize=(10,6))
plt.bar(x_pos, top10_mortes["new_deaths"], color="red")
plt.xticks(x_pos, top10_mortes["city"], rotation=45, ha="right")
plt.title("Top 10 cidades com mais mortes (new_deaths)")
plt.xlabel("Cidade")
plt.ylabel("Mortes")
plt.tight_layout()
grafico_path = "relatorio/prints/top10_mortes.png"
plt.savefig(grafico_path)
plt.close()

# ====== FUNÇÃO PARA FORMATAR TABELAS ======
def criar_tabela(df, colunas=None, max_linhas=15):
    """Cria uma tabela do ReportLab a partir de um DataFrame"""
    if colunas:
        df = df[colunas]
    if len(df) > max_linhas:
        df = df.head(max_linhas)

    dados = [df.columns.tolist()] + df.values.tolist()

    tabela = Table(dados, hAlign='CENTER')
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.grey),
        ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0,0), (-1,0), 6),
        ("BACKGROUND", (0,1), (-1,-1), colors.beige),
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
    ]))
    return tabela

# ====== GERAR PDF ======
doc = SimpleDocTemplate("relatorio/Relatorio_Covid.pdf")
styles = getSampleStyleSheet()
story = []

story.append(Paragraph("<b>Relatório de Análise COVID</b>", styles["Title"]))
story.append(Spacer(1, 20))

# 1. Mortes por cidade
story.append(Paragraph("<b>1. Mortes por cidade</b>", styles["Heading2"]))
story.append(criar_tabela(mortes_por_cidade.sort_values("new_deaths", ascending=False), ["city", "new_deaths"]))
story.append(Spacer(1, 20))

# 2. População estimada
story.append(Paragraph("<b>2. População estimada antes e depois</b>", styles["Heading2"]))
story.append(criar_tabela(populacao, ["city", "estimated_population_2019", "estimated_population"]))
story.append(Spacer(1, 20))

# 3. Maior/Menor cidade em casos confirmados
story.append(Paragraph("<b>3. Maior e menor cidade em casos confirmados</b>", styles["Heading2"]))
story.append(Paragraph(f"<b>Maior cidade:</b> {maior_cidade['city']} - {int(maior_cidade['last_available_confirmed'])} casos", styles["Normal"]))
story.append(Paragraph(f"<b>Menor cidade:</b> {menor_cidade['city']} - {int(menor_cidade['last_available_confirmed'])} casos", styles["Normal"]))
story.append(Spacer(1, 20))

# 4. Gráfico
story.append(Paragraph("<b>4. Gráfico - Top 10 cidades com mais mortes</b>", styles["Heading2"]))
story.append(Image(grafico_path, width=400, height=250))

doc.build(story)

print("✅ Relatório gerado em 'relatorio/Relatorio_Covid.pdf'")
