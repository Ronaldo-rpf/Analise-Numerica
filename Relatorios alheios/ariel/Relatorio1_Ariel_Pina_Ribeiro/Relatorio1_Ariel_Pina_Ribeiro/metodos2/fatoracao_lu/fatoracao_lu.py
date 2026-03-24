from pathlib import Path
import time
from typing import Tuple

import numpy as np


def ler_entrada(arquivo: str) -> Tuple[np.ndarray, np.ndarray]:
    p = Path(arquivo)
    if not p.exists():
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {arquivo}")

    linhas = [ln.strip() for ln in p.open("r", encoding="utf-8").readlines() if ln.strip() != ""]

    if len(linhas) < 1:
        raise ValueError("Arquivo de entrada vazio ou formato inválido.")

    try:
        n = int(linhas[0])
    except Exception as exc:
        raise ValueError(f"Primeira linha deve conter inteiro n (dimensão): {exc}")

    if len(linhas) < 1 + n:
        raise ValueError(f"Arquivo deve conter n={n} linhas com os coeficientes após a primeira linha.")

    A_rows = []
    b = []
    for i in range(n):
        parts = linhas[1 + i].split()
        if len(parts) < n + 1:
            raise ValueError(f"Linha {i+2} deve conter n+1={n+1} valores (coeficientes e termo independente).")
        try:
            nums = [float(x) for x in parts[: n + 1]]
        except Exception as exc:
            raise ValueError(f"Erro convertendo números na linha {i+2}: {exc}")
        A_rows.append(nums[:n])
        b.append(nums[n])

    A = np.array(A_rows, dtype=float)
    b = np.array(b, dtype=float)
    return A, b


def fatoracao_LU(A_in: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    A = A_in.astype(float).copy()
    n = A.shape[0]
    if A.shape != (n, n):
        raise ValueError("A deve ser uma matriz quadrada n x n.")

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
            raise ZeroDivisionError(f"Pivô U[{i},{i}] é zero (sem pivotamento); fatoração impossível.")

        for j in range(i + 1, n):
            s = 0.0
            if i > 0:
                s = float(np.dot(L[j, :i], U[:i, i]))
            L[j, i] = (A[j, i] - s) / U[i, i]

    return L, U


def resolver_sistema_LU(L: np.ndarray, U: np.ndarray, b: np.ndarray) -> np.ndarray:
    n = b.size
    if L.shape != (n, n) or U.shape != (n, n):
        raise ValueError("Dimensões de L, U e b incompatíveis.")

    y = np.zeros(n, dtype=float)
    for i in range(n):
        s = 0.0
        if i > 0:
            s = float(np.dot(L[i, :i], y[:i]))
        y[i] = b[i] - s

    x = np.zeros(n, dtype=float)
    for i in range(n - 1, -1, -1):
        if U[i, i] == 0.0:
            raise ZeroDivisionError(f"Pivô zero na retro-substituição em U[{i},{i}].")
        s = 0.0
        if i + 1 < n:
            s = float(np.dot(U[i, i + 1 :], x[i + 1 :]))
        x[i] = (y[i] - s) / U[i, i]

    return x


def main(caminho_entrada: str = "../entrada.txt"):
    A, b = ler_entrada(caminho_entrada)

    t0 = time.time()
    try:
        L, U = fatoracao_LU(A)
        x = resolver_sistema_LU(L, U, b)
    except Exception as exc:
        print(f"Erro durante fatoração/solução: {exc}")
        raise
    tempo = time.time() - t0

    sol_arred = [round(float(xi), 6) for xi in x]

    with open("saida.txt", "w", encoding="utf-8") as fo:
        fo.write(f"Solução encontrada: {sol_arred}\n")
        fo.write(f"Tempo de execução: {tempo:.6f} segundos\n")

    print("Arquivo de saída salvo em: 'saida.txt'!")


if __name__ == "__main__":
    entrada = "../entrada.txt"
    try:
        main(entrada)
    except Exception as e:
        print(f"Erro: {e}")
        raise
