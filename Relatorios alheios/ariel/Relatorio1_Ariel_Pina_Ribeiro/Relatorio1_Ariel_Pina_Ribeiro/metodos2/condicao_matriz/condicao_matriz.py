from pathlib import Path
import time
from typing import Tuple

import numpy as np


def ler_entrada(arquivo: str) -> np.ndarray:
    p = Path(arquivo)
    if not p.exists():
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {arquivo}")

    linhas = [ln.strip() for ln in p.open('r', encoding='utf-8').readlines() if ln.strip() != '']
    if len(linhas) == 0:
        raise ValueError("Arquivo de entrada vazio.")

    try:
        rows = [[float(v) for v in line.split()] for line in linhas]
    except Exception as exc:
        raise ValueError(f"Erro convertendo valores da matriz para float: {exc}")

    A = np.array(rows, dtype=float)
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("A deve ser uma matriz quadrada (n x n).")

    return A


def fatoracao_lu(A: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    A = A.astype(float).copy()
    n = A.shape[0]
    L = np.zeros((n, n), dtype=float)
    U = np.zeros((n, n), dtype=float)

    for i in range(n):
        L[i, i] = 1.0

    for i in range(n):
        for j in range(i, n):
            s = 0.0
            if i > 0:
                s = float(np.dot(L[i, :i], U[:i, j]))
            U[i, j] = A[i, j] - s

        if U[i, i] == 0.0:
            raise ZeroDivisionError(f"Pivô zero detectado em U[{i},{i}].")

        for j in range(i + 1, n):
            s = 0.0
            if i > 0:
                s = float(np.dot(L[j, :i], U[:i, i]))
            L[j, i] = (A[j, i] - s) / U[i, i]

    return L, U


def resolver_sistema_LU(L: np.ndarray, U: np.ndarray, b: np.ndarray) -> np.ndarray:
    n = b.size
    y = np.zeros(n, dtype=float)
    for i in range(n):
        s = float(np.dot(L[i, :i], y[:i])) if i > 0 else 0.0
        y[i] = b[i] - s

    x = np.zeros(n, dtype=float)
    for i in range(n - 1, -1, -1):
        denom = U[i, i]
        if denom == 0.0:
            raise ZeroDivisionError(f"Pivô zero na retro-substituição U[{i},{i}].")
        s = float(np.dot(U[i, i + 1 :], x[i + 1 :])) if i + 1 < n else 0.0
        x[i] = (y[i] - s) / denom

    return x


def calcular_inversa_por_LU(A: np.ndarray) -> np.ndarray:
    n = A.shape[0]
    L, U = fatoracao_lu(A)
    invA = np.zeros((n, n), dtype=float)

    for i in range(n):
        e = np.zeros(n, dtype=float)
        e[i] = 1.0
        invA[:, i] = resolver_sistema_LU(L, U, e)

    return invA


def calcular_numero_de_condicao(A: np.ndarray, invA: np.ndarray) -> float:
    norm_A = np.linalg.norm(A, ord=2)
    norm_invA = np.linalg.norm(invA, ord=2)
    return norm_A * norm_invA


def salvar_resultados(cond_number: float, inv_matrix: np.ndarray, tempo: float):
    with open('saida.txt', 'w', encoding='utf-8') as fo:
        fo.write(f"Número de condição (norma 2): {cond_number:.6e}\n")
        fo.write(f"Tempo de execução: {tempo:.6f} segundos\n\n")
        fo.write("Matriz inversa:\n")
        for row in inv_matrix:
            fo.write(f"[{', '.join(f'{val:.6e}' for val in row)}]\n")


def main(caminho_entrada: str = "entrada.txt"):
    A = ler_entrada(caminho_entrada)

    t0 = time.time()
    try:
        invA = calcular_inversa_por_LU(A)
        cond_number = calcular_numero_de_condicao(A, invA)
    except Exception as exc:
        print(f"Erro durante cálculo: {exc}")
        raise
    tempo = time.time() - t0

    salvar_resultados(cond_number, invA, tempo)

    print(f"Número de condição (norma 2): {cond_number:.6e}")
    print(f"Arquivo de saída salvo em: 'saida.txt' (tempo: {tempo:.6f}s)")


if __name__ == '__main__':
    entrada = "entrada.txt"
    try:
        main(entrada)
    except Exception as e:
        print(f"Erro: {e}")
        raise
