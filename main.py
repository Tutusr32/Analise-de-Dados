# %% Organização de Dados

import pandas as pd

df = pd.read_csv("SampleSuperstore.csv", sep=",")

# %%

df.head()

# %% Renomeando colunas

df = df.rename(columns={
    'Ship Mode': 'Modo de Envio',
    'Segment': 'Segmento',
    'Country': 'País',
    'City': 'Cidade',
    'State': 'Estado',
    'Postal Code': 'Código Postal',
    'Region': 'Região',
    'Category': 'Categoria',
    'Sub-Category': 'Sub-Categoria',
    'Sales': 'Vendas',
    'Quantity': 'Quantidade',
    'Discount': 'Desconto',
    'Profit': 'Lucro'
})

df["Vendas"] = df['Vendas'].fillna(0)

df

# %% Soma do Sales

soma_sales = df["Vendas"].sum()
soma_sales

# %% Soma do Profit

soma_profit = df["Lucro"].sum()
soma_profit

# %% É Lucrativo?

#Sim, profit positivo indica lucro positivo também.

# %% Margem de lucros em %

margem = soma_profit / soma_sales * 100
print(f'{margem:.2f}%')

# %% Qual região fatura mais?

df_fatura_regiao = df.groupby(by="Região", as_index=False)["Vendas"].sum().sort_values(by="Vendas", ascending=False)

df_fatura_regiao.head(1)

# %% Qual região lucra mais?

df_lucro_regiao = df.groupby(by="Região", as_index=False)["Lucro"].sum().sort_values(by="Lucro", ascending=False)

df_lucro_regiao.head(1)

# %% Existe região que vende muito mas dá prejuízo?

df_lucro_regiao

# Não existe região que dá prejuízo.

# %% Top 5 estados por faturamento

df_fatura_estado = df.groupby(by="Estado", as_index=False)["Vendas"].sum().sort_values(by="Vendas", ascending=False)

df_fatura_estado.head()

# %% Top 5 estados por lucro

df_lucro_estado = df.groupby(by="Estado", as_index=False)["Lucro"].sum().sort_values(by="Lucro", ascending=False)

df_lucro_estado.head()

# %% Top 5 estados por prejuízo

df_preju_estado = df.groupby(by="Estado", as_index=False)["Lucro"].sum().sort_values(by="Lucro", ascending=True)

df_preju_estado.head()

# %% Qual categoria vende mais?

df_categoria_sales = df.groupby(by="Categoria", as_index=False)["Vendas"].sum().sort_values(by="Vendas", ascending=False)

df_categoria_sales.head(1)

# %% Qual categoria lucra mais?

df_categoria_lucro = df.groupby(by="Categoria", as_index=False)["Lucro"].sum().sort_values(by="Lucro", ascending=False)

df_categoria_lucro.head(1)

# %% Existe categoria com lucro negativo?

df_categoria_lucro_neg = df.groupby(by="Categoria", as_index=False)["Lucro"].sum().sort_values(by="Lucro", ascending=True)

df_categoria_lucro_neg.head()

# Não existe, as 3 categorias trazem lucro positivo

# %% Quais subcategorias dão prejuízo?
 
subcategoria_preju = df.groupby(by="Sub-Categoria", as_index=False)["Lucro"].sum().sort_values(by="Lucro", ascending=True)

subcategoria_preju.loc[subcategoria_preju["Lucro"] < 0, "Sub-Categoria"]

# Tables, Bookcases, Supplies

# %% Quais subcategorias salvam o caixa?

preju_subcat = subcategoria_preju.loc[subcategoria_preju["Lucro"] < 0, "Lucro"].sum()

preju_total = abs(preju_subcat)

lucro_subcat = subcategoria_preju.loc[subcategoria_preju["Lucro"] > 0, ["Sub-Categoria", "Lucro"]]

lucro_subcat["Cobertura_Prejuizo"] = lucro_subcat["Lucro"] - preju_total

lucro_subcat[lucro_subcat["Lucro"] >= preju_total].sort_values(by="Cobertura_Prejuizo", ascending=False)

# %% Qual o desconto médio aplicado?

desc_mean = pd.to_numeric(df["Desconto"], errors="coerce").mean()

print(f"{desc_mean * 100:.2f}%")

# %% Quanto maior o desconto, menor o lucro?

# Em proporção sim, por exemplo:
#   50% de desconto em um possível R$1000 de lucro, se torna R$500.
# Mas, por exemplo, 20% em R$10, se torna R$8.
# 500 é maior que 8, mas 8 foi um lucro maior do que 500 na proporção.

# %% Existe um “ponto de ruptura” onde desconto mata o lucro?

df_desconto = df.groupby("Desconto", as_index=False)["Lucro"].mean().sort_values("Desconto")

ponto_ruptura = df_desconto[df_desconto["Lucro"] <= 0].head(1)

ponto_ruptura

#A partir de 30% de desconto, o lucro médio observado no dataset fica negativo. Indica risco, possível ponto de ruptura.

# %% Subcategorias mais afetadas por desconto

desconto_subcat = df.groupby("Sub-Categoria", as_index=False)["Desconto"].sum().sort_values("Desconto", ascending=False)

desconto_subcat.head()

# A análise apresentada segue a lógica adotada ao longo do projeto (Soluções desenvolvidas por mim). Abordagens que fugiriam dessa estrutura não foram aplicadas.

# %% Ticket médio por venda

qntd_vendas = len(df)

ticket = soma_sales / qntd_vendas

ticket

# %% Lucro médio por vendas

lucro_vendas = soma_profit / qntd_vendas

lucro_vendas

# %% Lucro por item vendido

lucro_itens = soma_sales / df["Quantidade"].sum()

lucro_itens

# %% Produtos vendidos em grande quantidade, mas com baixo lucro

mescla = df.groupby(by="Sub-Categoria", as_index=False).agg({
    "Vendas": "sum",
    "Lucro": "sum"
}).sort_values(by="Vendas", ascending=False)

mescla

# %% Qual segmento é mais lucrativo?

seg_lucrativo = df.groupby(by="Segmento", as_index=False)["Lucro"].sum().sort_values(by="Lucro", ascending=False)

seg_lucrativo.head(1)

# %% Segmento que mais gera prejuízo

seg_lucrativo = df.groupby(by="Segmento", as_index=False)["Lucro"].sum().sort_values(by="Lucro", ascending=False)

seg_lucrativo.tail(1)

# Não dá prejuízo, mas é o menos lucrativo

# %% Ship Mode mais usado

ship_mode = df.groupby(by="Modo de Envio", as_index=False)["Quantidade"].sum().sort_values(by="Quantidade", ascending=False)

ship_mode.head(1)

# %% Ship Mode mais lucrativo

ship_mode_lucro = df.groupby(by="Modo de Envio", as_index=False)["Lucro"].sum().sort_values(by="Lucro", ascending=False)

ship_mode_lucro.head()

# %% Existe Ship Mode caro demais pro lucro que gera?

mescla_ship = ship_mode.merge(ship_mode_lucro, on="Modo de Envio", how="inner")

mescla_ship

# Same Day apresenta menor retorno em relação ao volume,
# indicando possível ineficiência quando comparado aos demais modos.

# %% Existem vendas com lucro negativo? Quantas?

qtd_vendas_neg = (df["Lucro"] < 0).sum()

qtd_vendas_neg

# %% Existem vendas com desconto alto e lucro positivo?

vendas_desc_final = len(df[(df["Desconto"] > 0.5) & (df["Lucro"] > 0)])

vendas_desc_final

# %% Outliers extremos de prejuízo

# com prejuízos extremos. Eles podem ser identificados com métodos estatísticos, como o uso de quartis (IQR).

#Essa análise não foi feita em código neste projeto porque ainda foge do meu nível atual de estudo, ficando como um próximo passo de aprendizado.

# %% Vendas com Sales alto e Profit negativo

media = df["Vendas"].mean()

final = df.loc[
    (df["Vendas"] > media) & (df["Lucro"] < 0),
    ["Vendas", "Lucro"]
].sort_values(by="Vendas", ascending=False)

final
