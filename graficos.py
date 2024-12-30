import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

df = pd.read_csv('ecommerce_estatistica.csv')
df = df.drop(['Review2', 'Review1', 'Review3', 'Temporada'], axis=1)

print(df.head().to_string())

# Histograma - Distribuição de Descontos
plt.figure(figsize=(8, 6))
plt.hist(df['Desconto'], bins=50, color='green', alpha=0.8)
plt.title('Histograma - Distribuição de Descontos')
plt.xlabel('Desconto')
plt.xticks(ticks=range(0, int(df['Desconto'].max())+10, 10))
plt.ylabel('Frequência')
plt.grid(True)
plt.show()

# Preparação para Vendas por Marca
vendas_por_marca = df.groupby('Marca')['Qtd_Vendidos_Cod'].sum().reset_index()

# Renomear as colunas para uma melhor apresentação
vendas_por_marca.columns = ['Marca', 'Qtd_Total_Vendas']

top_marcas = vendas_por_marca.nlargest(5, 'Qtd_Total_Vendas')
top_marcas_list = top_marcas['Marca'].tolist()

# Adicionar uma entrada "Outros" para as marcas que não estão no top 5
vendas_por_marca['Marca'] = vendas_por_marca['Marca'].apply(lambda x: x if x in top_marcas_list else 'Outros')
vendas_agrupadas = vendas_por_marca.groupby('Marca')['Qtd_Total_Vendas'].sum().reset_index()

# Ordenar por quantidade de vendas
vendas_agrupadas = vendas_agrupadas.sort_values(by='Qtd_Total_Vendas', ascending=False)

# Gráfico de dispersão - Vendas por Marca
plt.figure(figsize=(10, 6))
sns.scatterplot(data=vendas_agrupadas, x='Qtd_Total_Vendas', y='Marca', s=100, color='blue')
plt.title('Top 5 Marcas com Mais Vendas e Outros', fontsize=16)
plt.xlabel('Quantidade Total de Vendas', fontsize=14)
plt.ylabel('Marca', fontsize=14)
plt.grid(True)


# Mapa de Calor - Correlação Material e Vendas, não há uma correlação relevante
df_renomeado = df.rename(columns={'Material_Cod': 'Material.', 'Qtd_Vendidos_Cod': 'Vendas.'})

plt.figure(figsize=(5, 5))
corr = df_renomeado[['Material.', 'Vendas.']].corr()
#plt.subplot(2, 2, 3)  # 1 Linha, 2 Colunas, 3° Gráfico
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title('Correlação Material e Vendas')

# Preparação do Gráfico de Barras
faixas = [0, 50, 100, 200, float('inf')]  # 'inf' para capturar valores acima de 200
labels = ['0-50', '50-100', '100-200', '200+']

# Criar a nova coluna "Faixa" com base nas faixas de preço
df['Faixa'] = pd.cut(df['Preço'], bins=faixas, labels=labels, right=False)

# Contagem de produtos por faixa
contagem_por_faixa = df['Faixa'].value_counts().sort_index()

# Gráfico de barras - Qtd. de Produtos por Faixa
plt.figure(figsize=(8, 6))
contagem_por_faixa.plot(kind='bar', color='skyblue')

plt.title('Quantidade de Produtos por Faixa de Preço', fontsize=14)
plt.xlabel('Faixa de Preço', fontsize=12)
plt.ylabel('Quantidade de Produtos', fontsize=12)
plt.xticks(rotation=0)
plt.tight_layout()  # Ajustar espaçamentos
plt.show()

# Gráfico de pizza - % de Produtos por Faixa
x = df['Faixa'].value_counts().index
y = df['Faixa'].value_counts().values

plt.figure(figsize=(4, 4)) #Cria o gráfico de pizza
plt.pie(y, labels=x, autopct='%.1f%%', startangle=90)
plt.title('% de Produtos por Faixa de Preço')
plt.show()

# Gráfico de Densidade - Preços
plt.figure(figsize=(10, 6))
sns.kdeplot(df['Preço'], fill=True, color='#863e9c')
plt.title('Densidade de Preços')
plt.xlabel('Preço')
plt.show()

# Gráfico de Regressão - Num. Vendas por Num. Avaliações
sns.regplot(x='Qtd_Vendidos_Cod', y='N_Avaliações', data=df, color='#278f65', scatter_kws={'alpha': 0.5, 'color': '#34c289'})
plt.title('Regressão de Num. Vendas por Num. Avaliações')
plt.xlabel('Vendas')
plt.ylabel('Avaliações')
plt.show()
