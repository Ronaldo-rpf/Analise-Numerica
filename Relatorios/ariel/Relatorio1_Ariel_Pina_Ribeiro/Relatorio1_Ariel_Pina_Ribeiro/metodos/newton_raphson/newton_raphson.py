from pathlib import Path
import time
from typing import Callable, Tuple

import numpy as np
from sympy import symbols, sympify, lambdify, diff


def newton_raphson(F: Callable[[float], float], F_prime: Callable[[float], float], a: float, b: float, tolerancia: float = 1e-6, max_iter: int = 1000) -> Tuple[float, float, int]:
    iteracoes = 0
    erro = 0.0

    x = (a + b) / 2.0

    while iteracoes < max_iter:
        try:
            Fx = float(F(x))
            Fpx = float(F_prime(x))
        except Exception as exc:
            raise RuntimeError(f"Erro avaliando f ou f' em x={x}: {exc}")

        if Fpx == 0.0:
            raise ZeroDivisionError("A derivada f'(x) é zero no ponto atual; método não pode continuar.")

        x_new = x - Fx / Fpx
        erro = abs(x_new - x)
        iteracoes += 1

        try:
            if erro < tolerancia or abs(float(F(x_new))) < tolerancia:
                return x_new, erro, iteracoes
        except Exception:
            if erro < tolerancia:
                return x_new, erro, iteracoes

        x = x_new

    return x, erro, iteracoes


def ler_arquivo_entrada(caminho: str) -> Tuple[Callable[[float], float], Callable[[float], float], float, float, float]:
    p = Path(caminho)
    if not p.exists():
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {caminho}")

    linhas = [ln.rstrip("\n") for ln in p.open("r", encoding="utf-8").readlines()]

    if len(linhas) < 3:
        raise ValueError("Arquivo de entrada deve conter pelo menos 3 linhas: função, a, b")

    expr_str = linhas[0].strip()

    try:
        a = float(linhas[1].strip())
        b = float(linhas[2].strip())
    except Exception as exc:
        raise ValueError(f"Erro convertendo a ou b para float: {exc}")

    tolerancia = 1e-8
    if len(linhas) >= 4:
        tol_s = linhas[3].strip()
        if tol_s:
            try:
                tolerancia = float(tol_s)
            except Exception as exc:
                raise ValueError(f"Tolerância inválida: {exc}")

    x = symbols("x")
    try:
        expr = sympify(expr_str)
    except Exception as exc:
        raise ValueError(f"Não foi possível parsear a expressão '{expr_str}': {exc}")

    expr_prime = diff(expr, x)
    F_num = lambdify(x, expr, modules=["numpy"])  
    Fp_num = lambdify(x, expr_prime, modules=["numpy"])  

    try:
        _ = float(F_num((a + b) / 2.0))
        _ = float(Fp_num((a + b) / 2.0))
    except Exception as exc:
        raise RuntimeError(f"Erro avaliando f ou f' no chute inicial: {exc}")

    return F_num, Fp_num, a, b, tolerancia


def main(caminho_entrada: str = "../entrada.txt"):
    F, F_prime, a, b, tolerancia = ler_arquivo_entrada(caminho_entrada)

    t0 = time.time()
    raiz, erro, iteracoes = newton_raphson(F, F_prime, a, b, tolerancia=tolerancia, max_iter=1000)
    tempo = time.time() - t0

    with open("saida.txt", "w", encoding="utf-8") as fo:
        fo.write(f"{raiz}\n")
        fo.write(f"{erro}\n")
        fo.write(f"{iteracoes}\n")
        fo.write(f"{tempo:.6f}\n")

    print("Arquivo de saída salvo em: 'saida.txt'!")


if __name__ == "__main__":
    entrada = "../entrada.txt"
    try:
        main(entrada)
    except Exception as e:
        print(f"Erro: {e}")
        raise
