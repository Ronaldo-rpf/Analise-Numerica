import numpy as np
import time
from sympy import symbols, sympify, diff, lambdify, exp, E

def metodo_bissecao(func, limite_esq, limite_dir, tol=1e-6, max_iter=1000):
    passos = 0
    erro_atual = 0.0
    meio = (limite_esq + limite_dir) / 2
    while (abs(limite_dir - limite_esq) / 2 > tol) and (passos < max_iter):
        meio = (limite_esq + limite_dir) / 2
        if abs(func(meio)) < tol:
            break
        if func(limite_esq) * func(meio) < 0:
            limite_dir = meio
        else:
            limite_esq = meio
        passos += 1
        erro_atual = abs(limite_dir - limite_esq) / 2
    return meio, erro_atual, passos
    
def metodo_newton(func, func_deriv, x_inicial, x_final, tol=1e-6, max_iter=1000):
    iter_count = 0
    erro = 0.0
    x = (x_inicial + x_final) / 2
    while iter_count < max_iter:
        f_val = func(x)
        deriv_val = func_deriv(x)
        if deriv_val == 0:
            raise ZeroDivisionError("Derivada igual a zero.")
        novo_x = x - f_val / deriv_val
        erro = abs(novo_x - x)
        x = novo_x
        iter_count += 1
        if erro < tol:
            break
    return x, erro, iter_count

def metodo_falsa_posicao(func, a, b, tol=1e-6, max_iter=1000):
    k = 0
    erro = 0.0
    c = a
    while k < max_iter:
        fa, fb = func(a), func(b)
        c = (a * fb - b * fa) / (fb - fa)
        fc = func(c)
        erro = abs(fc)
        if fa * fc < 0:
            b = c
        else:
            a = c
        k += 1
        if erro < tol:
            break
    return c, erro, k

def metodo_secante(func, x0, x1, tol=1e-6, max_iter=1000):
    passos = 0
    erro = 0.0
    prox = x1
    while passos < max_iter:
        f0, f1 = func(x0), func(x1)
        if f1 - f0 == 0:
            raise ZeroDivisionError("Divisão por zero na secante.")
        prox = x1 - f1 * (x1 - x0) / (f1 - f0)
        erro = abs(prox - x1)
        x0, x1 = x1, prox
        passos += 1
        if erro < tol:
            break
    return prox, erro, passos

def carregar_dados(caminho):
    with open(caminho, "r") as arquivo:
        funcao_txt = arquivo.readline().strip()
        linhas = [linha.strip() for linha in arquivo if linha.strip()]
    x = symbols("x")
    expr = sympify(funcao_txt, locals={"E": E, "exp": exp})
    f = lambdify(x, expr, "numpy")
    derivada = diff(expr, x).doit()   
    f_deriv = lambdify(x, derivada, "numpy")
    parametros = [float(valor) for valor in linhas]
    return f, f_deriv, parametros

def executar(arquivo, metodo="bissecao"):
    f, f_deriv, parametros = carregar_dados(arquivo)
    if metodo in ("bissecao", "falsa_posicao", "newton_raphson"):
        a, b = parametros[0], parametros[1]
        tol = parametros[2] if len(parametros) > 2 else 1e-8
    elif metodo == "secante":
        x0, x1 = parametros[0], parametros[1]
        tol = parametros[2] if len(parametros) > 2 else 1e-8
    else:
        raise ValueError("Método inválido.")
    inicio = time.time()
    if metodo == "bissecao":
        raiz, erro, it = metodo_bissecao(f, a, b, tol)
    elif metodo == "newton_raphson":
        raiz, erro, it = metodo_newton(f, f_deriv, a, b, tol)
    elif metodo == "falsa_posicao":
        raiz, erro, it = metodo_falsa_posicao(f, a, b, tol)
    else: 
        raiz, erro, it = metodo_secante(f, x0, x1, tol)
    fim = time.time()
    print(f"\n>>> Método escolhido: {metodo}")
    print(f"Raiz aproximada: {raiz}")
    print(f"Erro estimado: {erro}")
    print(f"Iterações: {it}")
    print(f"Tempo: {fim - inicio:.6f} segundos")
    with open("saida.txt", "w", encoding="utf-8") as out:
        out.write(f"Método escolhido: {metodo}\n")
        out.write(f"Raiz aproximada: {raiz}\n")
        out.write(f"Erro estimado: {erro}\n")
        out.write(f"Iterações: {it}\n")
        out.write(f"Tempo: {fim - inicio:.6f} segundos\n")
        out.flush()

if __name__ == "__main__":
    arq = "entrada.txt"
    metodo = input("Método (bissecao, newton_raphson, falsa_posicao, secante): ").strip()
    executar(arq, metodo)
