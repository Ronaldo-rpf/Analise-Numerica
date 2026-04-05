import numpy as np
import time
from sympy import symbols, sympify, lambdify, E

def bissecao(F, a, b, tolerancia=1e-6, maximo_iteracoes=1000):
    iteracoes = 0
    erro = 0.0

    while abs(b - a) / 2 > tolerancia and iteracoes < maximo_iteracoes:

        c = (a + b) / 2

        if abs(F(c)) < tolerancia:
            break

        if F(a) * F(c) < 0:
            b = c
        else:
            a = c

        iteracoes += 1
        erro = abs(b - a) / 2

    return c, erro, iteracoes


def ler_entrada(arquivo):
    with open(arquivo, 'r') as f:

        func_str = f.readline().strip()
        a = float(f.readline().strip())
        b = float(f.readline().strip())

        tolerancia = f.readline().strip()
        tolerancia = float(tolerancia) if tolerancia else 1e-8

    #func_str = func_str.replace('e', 'E')

    x = symbols('x')
    F = sympify(func_str)
    f = lambdify(x, F, "numpy")

    return f, a, b, tolerancia


def main(arquivo_entrada):

    F, a, b, tolerancia = ler_entrada(arquivo_entrada)

    start_time = time.time()

    raiz, erro, iteracoes = bissecao(F, a, b, tolerancia)

    tempo_execucao = time.time() - start_time

    print(f"Raiz encontrada: {raiz}")
    print(f"Erro final: {erro}")
    print(f"Número de iterações: {iteracoes}")
    print(f"Tempo de execução: {tempo_execucao:.6f} segundos")

    with open('bissecao3.2.txt', 'w') as f_saida:
        f_saida.write(f"{raiz}\n")
        f_saida.write(f"{erro}\n")
        f_saida.write(f"{iteracoes}\n")
        f_saida.write(f"{tempo_execucao:.6f}\n")


if __name__ == "__main__":
    arquivo_entrada = "entrada.txt"
    main(arquivo_entrada)