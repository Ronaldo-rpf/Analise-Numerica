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


def eliminacao_gauss(A_in: np.ndarray, b_in: np.ndarray) -> np.ndarray:
    A = A_in.astype(float).copy()
    b = b_in.astype(float).copy()

    n = A.shape[0]
    if A.shape != (n, n) or b.shape != (n,):
        raise ValueError("Dimensões inconsistentes entre A e b.")

    for k in range(n):
        if A[k, k] == 0.0:
            raise ZeroDivisionError(f"Divisão por zero durante eliminação no pivô A[{k},{k}].")

        for i in range(k + 1, n):
            m = A[i, k] / A[k, k]
            A[i, k:] = A[i, k:] - m * A[k, k:]
            b[i] = b[i] - m * b[k]

    x = np.zeros(n, dtype=float)
    for i in range(n - 1, -1, -1):
        denom = A[i, i]
        if denom == 0.0:
            raise ZeroDivisionError(f"Divisão por zero na retro-substituição na linha {i}.")
        s = np.dot(A[i, i + 1 :], x[i + 1 :]) if i + 1 < n else 0.0
        x[i] = (b[i] - s) / denom

    return x


def main(caminho_entrada: str = "../entrada.txt"):
    A, b = ler_entrada(caminho_entrada)

    t0 = time.time()
    try:
        x = eliminacao_gauss(A, b)
    except Exception as exc:
        print(f"Erro durante eliminação de Gauss: {exc}")
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
