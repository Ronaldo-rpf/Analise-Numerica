import time
from pathlib import Path
from typing import Callable, Tuple

import numpy as np
from sympy import symbols, sympify, lambdify, E


def bissecao(F: Callable[[float], float], a: float, b: float, tolerancia: float = 1e-6, maximo_iteracoes: int = 1000) -> Tuple[float, float, int]:
    iteracoes = 0
    erro = 0.0
    c = (a + b) / 2.0 

    while abs(b - a) / 2.0 > tolerancia and iteracoes < maximo_iteracoes:
        c = (a + b) / 2.0

        if abs(F(c)) < tolerancia:
            break

        if F(a) * F(c) < 0:
            b = c
        else:
            a = c

        iteracoes += 1
        erro = abs(b - a) / 2.0

    return c, erro, iteracoes


def ler_entrada(arquivo: str):
    caminho = Path(arquivo)
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {arquivo}")

    with caminho.open('r', encoding='utf-8') as f:
        linhas = [ln.rstrip('\n') for ln in f.readlines()]

    if len(linhas) < 3:
        raise ValueError("Arquivo de entrada deve conter pelo menos 3 linhas: função, a, b")

    func_str = linhas[0].strip()
    try:
        a = float(linhas[1].strip())
        b = float(linhas[2].strip())
    except Exception as exc:
        raise ValueError(f"Erro ao converter a ou b para float: {exc}")

    tolerancia = 1e-8
    if len(linhas) >= 4:
        tol_str = linhas[3].strip()
        if tol_str:
            try:
                tolerancia = float(tol_str)
            except Exception as exc:
                raise ValueError(f"Tolerância inválida: {exc}")

    func_str = func_str.replace('e', 'E')

    x = symbols('x')
    expr = sympify(func_str)
    f_num = lambdify(x, expr, 'numpy')

    return f_num, a, b, tolerancia


def main(arquivo_entrada: str):
    F, a, b, tolerancia = ler_entrada(arquivo_entrada)

    start_time = time.time()

    raiz, erro, iteracoes = bissecao(F, a, b, tolerancia)

    tempo_execucao = time.time() - start_time

    with open('saida.txt', 'w', encoding='utf-8') as f_saida:
        f_saida.write(f"{raiz}\n")
        f_saida.write(f"{erro}\n")
        f_saida.write(f"{iteracoes}\n")
        f_saida.write(f"{tempo_execucao:.6f}\n")

    print("Arquivo de saída salvo em: 'saida.txt'!")


if __name__ == '__main__':
    arquivo_entrada = '../entrada.txt'
    try:
        main(arquivo_entrada)
    except Exception as e:
        print(f"Erro: {e}")
        raise
