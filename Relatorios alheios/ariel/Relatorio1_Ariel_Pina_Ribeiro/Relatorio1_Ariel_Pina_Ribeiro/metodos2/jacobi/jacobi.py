from pathlib import Path
import time
from typing import Tuple, Optional

import numpy as np


def ler_entrada(arquivo: str) -> Tuple[np.ndarray, np.ndarray, float, int]:
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

    tolerancia = 1e-6
    max_iter = 1000
    if len(linhas) >= 1 + n + 1:
        tol_s = linhas[1 + n].strip()
        if tol_s:
            try:
                tolerancia = float(tol_s)
            except Exception as exc:
                raise ValueError(f"Tolerância inválida: {exc}")
    if len(linhas) >= 1 + n + 2:
        max_iter_s = linhas[2 + n].strip()
        if max_iter_s:
            try:
                max_iter = int(max_iter_s)
            except Exception as exc:
                raise ValueError(f"max_iter inválido: {exc}")

    A = np.array(A_rows, dtype=float)
    b = np.array(b, dtype=float)
    return A, b, tolerancia, max_iter


def metodo_jacobi(A: np.ndarray, b: np.ndarray, tol: float = 1e-6, max_iter: int = 1000) -> Tuple[Optional[np.ndarray], int]:
    n = b.size
    if A.shape != (n, n):
        raise ValueError("Dimensões de A e b incompatíveis.")

    if np.any(np.isclose(np.diag(A), 0.0)):
        raise ZeroDivisionError("Zero (ou próximo de zero) detectado na diagonal de A; Jacobi inválido.")

    x = np.zeros(n, dtype=float)

    D = np.diag(np.diag(A))
    R = A - D

    for k in range(1, max_iter + 1):
        x_new = (b - R.dot(x)) / np.diag(D)

        if np.isinf(x_new).any() or np.isnan(x_new).any():
            return None, k

        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new, k

        x = x_new

    return x, max_iter


def main(caminho_entrada: str = "../entrada.txt"):
    A, b, tolerancia, max_iter = ler_entrada(caminho_entrada)

    t0 = time.time()
    try:
        x, iteracoes = metodo_jacobi(A, b, tol=tolerancia, max_iter=max_iter)
    except Exception as exc:
        print(f"Erro durante execução do método de Jacobi: {exc}")
        raise
    tempo = time.time() - t0

    with open("saida.txt", "w", encoding="utf-8") as fo:
        if x is None:
            fo.write("Solução não encontrada: o método divergiu.\n")
            fo.write(f"Iterações realizadas até a detecção: {iteracoes}\n")
            fo.write(f"Tempo de execução: {tempo:.6f} segundos\n")
            print("O método divergiu: não foi possível encontrar uma solução.")
        else:
            sol_arred = [round(float(xi), 6) for xi in x]
            fo.write(f"Solução encontrada: {sol_arred}\n")
            fo.write(f"Iterações realizadas: {iteracoes}\n")
            fo.write(f"Tempo de execução: {tempo:.6f} segundos\n")
            print(f"Solução encontrada: {sol_arred}")

    print("Arquivo de saída salvo em: 'saida.txt'!")


if __name__ == "__main__":
    entrada = "../entrada.txt"
    try:
        main(entrada)
    except Exception as e:
        print(f"Erro: {e}")
        raise
