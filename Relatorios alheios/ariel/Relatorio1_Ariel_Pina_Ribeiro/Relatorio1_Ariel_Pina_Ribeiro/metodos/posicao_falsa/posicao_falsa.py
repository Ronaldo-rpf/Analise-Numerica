from pathlib import Path
import time
from typing import Callable, Tuple

import numpy as np
from sympy import symbols, sympify, lambdify

def posicao_falsa(F: Callable[[float], float], a: float, b: float, tolerancia: float = 1e-6, max_iter: int = 1000) -> Tuple[float, float, int]:
    iteracoes = 0
    c = (a + b) / 2.0
    erro = 0.0

    try:
        Fa = float(F(a))
        Fb = float(F(b))
    except Exception as e:
        raise ValueError(f"Erro avaliando f(a) ou f(b): {e}")

    if Fa == 0.0:
        return a, 0.0, 0
    if Fb == 0.0:
        return b, 0.0, 0
    if Fa * Fb > 0:
        raise ValueError("f(a) e f(b) têm o mesmo sinal. Forneça um intervalo que contenha mudança de sinal.")

    while iteracoes < max_iter:
        Fa = float(F(a))
        Fb = float(F(b))

        denom = (Fb - Fa)
        if denom == 0.0:
            c = (a + b) / 2.0
        else:
            c = (a * Fb - b * Fa) / denom

        Fc = float(F(c))
        erro = abs(Fc)

        if Fa * Fc < 0:
            b = c
        else:
            a = c

        iteracoes += 1

        if erro < tolerancia:
            break

    return c, erro, iteracoes


def ler_arquivo_entrada(caminho: str) -> Tuple[Callable[[float], float], float, float, float]:
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

    f_num = lambdify(x, expr, modules=["numpy"])

    try:
        _ = float(f_num(a))
        _ = float(f_num(b))
    except Exception as exc:
        raise ValueError(f"Erro avaliando a função nos extremos: {exc}")

    return f_num, a, b, tolerancia


def main(caminho_entrada: str = "../entrada.txt"):
    F, a, b, tolerancia = ler_arquivo_entrada(caminho_entrada)

    t0 = time.time()
    raiz, erro, iteracoes = posicao_falsa(F, a, b, tolerancia=tolerancia, max_iter=1000)
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
