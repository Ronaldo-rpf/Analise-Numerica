from pathlib import Path
import time
from typing import Callable, Tuple

import numpy as np
from sympy import symbols, sympify, lambdify


def secante(F: Callable[[float], float], x0: float, x1: float, tolerancia: float = 1e-6, max_iter: int = 1000) -> Tuple[float, float, int]:
    iteracoes = 0
    erro = 0.0
    x_prev = x0
    x_curr = x1
    x_new = x_curr

    try:
        fx_prev = float(F(x_prev))
        fx_curr = float(F(x_curr))
    except Exception as exc:
        raise RuntimeError(f"Erro avaliando F nos chutes iniciais: {exc}")

    if abs(fx_prev) == 0.0:
        return x_prev, 0.0, 0
    if abs(fx_curr) == 0.0:
        return x_curr, 0.0, 0

    while iteracoes < max_iter:
        try:
            fx_prev = float(F(x_prev))
            fx_curr = float(F(x_curr))
        except Exception as exc:
            raise RuntimeError(f"Erro avaliando F durante iteração em x_prev={x_prev} ou x_curr={x_curr}: {exc}")

        denom = (fx_curr - fx_prev)
        if denom == 0.0:
            raise ZeroDivisionError("Denominador zero detectado na fórmula da secante (fx1 - fx0 == 0).")

        x_new = x_curr - fx_curr * (x_curr - x_prev) / denom
        erro = abs(x_new - x_curr)

        iteracoes += 1

        if erro < tolerancia:
            return x_new, erro, iteracoes

        x_prev, x_curr = x_curr, x_new

    return x_new, erro, iteracoes


def ler_arquivo_entrada(caminho: str) -> Tuple[Callable[[float], float], float, float, float]:  
    p = Path(caminho)
    if not p.exists():
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {caminho}")

    linhas = [ln.rstrip("\n") for ln in p.open("r", encoding="utf-8").readlines()]

    if len(linhas) < 3:
        raise ValueError("Arquivo de entrada deve conter pelo menos 3 linhas: função, x0, x1")

    expr_str = linhas[0].strip()

    try:
        x0 = float(linhas[1].strip())
        x1 = float(linhas[2].strip())
    except Exception as exc:
        raise ValueError(f"Erro convertendo x0 ou x1 para float: {exc}")

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

    F_num = lambdify(x, expr, modules=["numpy"])

    try:
        _ = float(F_num(x0))
        _ = float(F_num(x1))
    except Exception as exc:
        raise RuntimeError(f"Erro avaliando F nos chutes iniciais: {exc}")

    return F_num, x0, x1, tolerancia


def main(caminho_entrada: str = "../entrada.txt"):
    F, x0, x1, tolerancia = ler_arquivo_entrada(caminho_entrada)

    t0 = time.time()
    try:
        raiz, erro, iteracoes = secante(F, x0, x1, tolerancia=tolerancia, max_iter=1000)
    except Exception as e:
        print(f"Erro durante execução do método da secante: {e}")
        raise
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
