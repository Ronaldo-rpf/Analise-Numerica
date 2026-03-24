
import numpy as np
import sys
import time

def decomposicao_LU(matriz):
    n = matriz.shape[0]
    L = np.identity(n)
    U = matriz.astype(float).copy()
    for k in range(n):
        if U[k, k] == 0:
            raise ValueError("Elemento pivô igual a zero.")
        for i in range(k + 1, n):
            fator = U[i, k] / U[k, k]
            L[i, k] = fator
            U[i, :] -= fator * U[k, :]
    return L, U

def resolver_LU(L, U, vetor_b):
    n = len(vetor_b)
    y = np.zeros(n)
    for i in range(n):
        y[i] = vetor_b[i] - np.dot(L[i, :i], y[:i])
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        soma = np.dot(U[i, i+1:], x[i+1:]) if i < n - 1 else 0
        x[i] = (y[i] - soma) / U[i, i]
    return x

def inverter_matriz(matriz):
    L, U = decomposicao_LU(matriz)
    n = matriz.shape[0]
    inversa = np.zeros((n, n))
    for j in range(n):
        e = np.zeros(n)
        e[j] = 1
        inversa[:, j] = resolver_LU(L, U, e)
    return inversa

def numero_de_condicao(matriz, matriz_inversa):
    norma_A = np.linalg.norm(matriz, 2)
    norma_A_inv = np.linalg.norm(matriz_inversa, 2)
    return norma_A * norma_A_inv

def carregar_matriz(nome_arquivo):
    try:
        with open(nome_arquivo, "r", encoding="utf-8", errors="ignore") as arq:
            linhas = arq.readlines()
            matriz = []
            for linha in linhas:
                if linha.strip():
                    valores = [float(x.strip().replace("Â", "")) for x in linha.split()]
                    matriz.append(valores)
        matriz = np.array(matriz)
        if matriz.shape[0] != matriz.shape[1]:
            raise ValueError(f"A matriz não é quadrada: {matriz.shape[0]}x{matriz.shape[1]}")
        return matriz
    except Exception as erro:
        print(f"Falha na leitura do arquivo: {erro}")
        sys.exit(1)

def escrever_saida(cond, inversa):
    with open("saida.txt", "w") as arq:
        arq.write(f"Condicionamento da matriz: {cond:.6f}\n")
        arq.write("\nMatriz inversa:\n")
        for linha in inversa:
            arq.write(" ".join(f"{val:.6f}" for val in linha) + "\n")

def principal(entrada):
    matriz = carregar_matriz(entrada)
    inicio = time.time()
    inversa = inverter_matriz(matriz)
    cond = numero_de_condicao(matriz, inversa)
    fim = time.time() - inicio
    print(f"Condicionamento calculado: {cond:.6f}")
    print(f"Tempo gasto: {fim:.6f} s")
    escrever_saida(cond, inversa)

if __name__ == "__main__":
    arquivo = "entrada.txt"
    principal(arquivo)
