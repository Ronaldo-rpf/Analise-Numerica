#!/usr/bin/env python3
import os
import pandas as pd
import matplotlib.pyplot as plt

# caminhos dos arquivos de saída
paths = {
    "Bissecção": "bisseccao/saida.txt",
    "Posição Falsa": "posicao_falsa/saida.txt",
    "Newton-Raphson": "newton_raphson/saida.txt",
    "Secante": "secante/saida.txt"
}

resultados = []

for metodo, caminho in paths.items():
    if not os.path.isfile(caminho):
        print(f"Aviso: {caminho} não existe, pulando {metodo}.")
        continue
    
    with open(caminho, "r") as f:
        linhas = [ln.strip() for ln in f.readlines() if ln.strip() != ""]
    
    if len(linhas) < 4:
        print(f"Aviso: {caminho} tem menos de 4 linhas válidas. Conteúdo: {linhas}")
        continue
    
    try:
        raiz = float(linhas[0])
        erro = float(linhas[1])
        iteracoes = int(float(linhas[2]))
        tempo = float(linhas[3])
    except Exception as e:
        print(f"Erro ao ler {caminho}: {e}")
        continue
    
    resultados.append({
        "Método": metodo,
        "Raiz": raiz,
        "Erro": erro,
        "Iterações": iteracoes,
        "Tempo (s)": tempo
    })

# transformar em DataFrame
df = pd.DataFrame(resultados).set_index("Método")
print("\n=== Resultados Comparativos ===")
print(df)

# salvar CSV para consulta
df.to_csv("resultados_comparacao.csv")
print("\nResultados salvos em resultados_comparacao.csv")

# ----- GRÁFICOS -----
# 1) Raiz aproximada
plt.figure(figsize=(6,4))
df["Raiz"].plot(kind="bar")
plt.ylabel("Raiz aproximada")
plt.title("Comparação de Raízes")
plt.tight_layout()
plt.savefig("comparacao_raiz.png")

# 2) Erro final (escala log)
plt.figure(figsize=(6,4))
ax = df["Erro"].plot(kind="bar")
ax.set_yscale("log")
plt.ylabel("Erro final (escala log)")
plt.title("Comparação de Erros")
plt.tight_layout()
plt.savefig("comparacao_erro.png")

# 3) Iterações
plt.figure(figsize=(6,4))
df["Iterações"].plot(kind="bar")
plt.ylabel("Número de iterações")
plt.title("Comparação de Iterações")
plt.tight_layout()
plt.savefig("comparacao_iteracoes.png")

# 4) Tempo de execução
plt.figure(figsize=(6,4))
df["Tempo (s)"].plot(kind="bar")
plt.ylabel("Tempo (s)")
plt.title("Comparação de Tempos de Execução")
plt.tight_layout()
plt.savefig("comparacao_tempo.png")

print("\nGráficos gerados: comparacao_raiz.png, comparacao_erro.png, comparacao_iteracoes.png, comparacao_tempo.png")
