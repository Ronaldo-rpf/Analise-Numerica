import time
import numpy as np
from sympy import symbols, sympify, lambdify, diff

class Raizes:
    def __init__(self, funcao, derivada):
        self.f = funcao
        self.f_linha = derivada

    def bisseccao(self, a, b, tol, max_iter=1000):
        for k in range(max_iter):
            meio = (a + b) / 2
            erro = abs(self.f(meio))
            if erro < tol or (b - a) / 2 < tol:
                return meio, erro, k + 1
            if self.f(a) * self.f(meio) < 0:
                b = meio
            else:
                a = meio
        return meio, abs(self.f(meio)), max_iter

    def newton(self, a, b, tol, max_iter=1000):
        x = (a + b) / 2
        for k in range(max_iter):
            fx = self.f(x)
            dfx = self.f_linha(x)
            if abs(dfx) < 1e-10:
                raise ZeroDivisionError("Derivada próxima de zero, método instável.")
            novo = x - fx / dfx
            erro = abs(fx)
            if erro < tol:
                return novo, erro, k + 1
            x = novo
        return x, abs(self.f(x)), max_iter

    def posicao_falsa(self, a, b, tol, max_iter=1000):
        for k in range(max_iter):
            fa, fb = self.f(a), self.f(b)
            if fb - fa == 0:
                raise ZeroDivisionError("Divisão por zero na posição falsa.")
            meio = (a * fb - b * fa) / (fb - fa)
            fc = self.f(meio)
            erro = abs(fc)
            if erro < tol:
                return meio, erro, k + 1
            if fa * fc < 0:
                b = meio
            else:
                a = meio
        return meio, abs(self.f(meio)), max_iter

    def secante(self, x0, x1, tol, max_iter=1000):
        for k in range(max_iter):
            f0, f1 = self.f(x0), self.f(x1)
            if abs(f1 - f0) < 1e-10:
                raise ZeroDivisionError("Divisão por valor muito pequeno na secante.")
            x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
            erro = abs(self.f(x2))
            if erro < tol:
                return x2, erro, k + 1
            x0, x1 = x1, x2
        return x2, abs(self.f(x2)), max_iter


def ler_entrada(arquivo):
    with open(arquivo) as f:
        expressao = f.readline().strip().replace("e", "E")
        valores = list(map(float, [linha for linha in f if linha.strip()]))
    x = symbols("x")
    expr = sympify(expressao)
    return lambdify(x, expr, "numpy"), lambdify(x, diff(expr, x), "numpy"), valores

def main(arquivo, metodo):
    f, f_linha, dados = ler_entrada(arquivo)
    tol = dados[2] if len(dados) > 2 else 1e-8
    met = Raizes(f, f_linha)

    inicio = time.time()
    if metodo == "bisseccao":
        raiz, erro, it = met.bisseccao(dados[0], dados[1], tol)
    elif metodo == "newton_raphson":
        raiz, erro, it = met.newton(dados[0], dados[1], tol)
    elif metodo == "falsa_posicao":
        raiz, erro, it = met.posicao_falsa(dados[0], dados[1], tol)
    elif metodo == "secante":
        raiz, erro, it = met.secante(dados[0], dados[1], tol)
    else:
        raise ValueError("Método inválido.")
    duracao = time.time() - inicio

    print(f"\nMétodo: {metodo}")
    print(f"Raiz encontrada: {raiz}")
    print(f"Erro: {erro}")
    print(f"Iterações: {it}")
    print(f"Tempo: {duracao:.6f}s")

    with open(f"saida_{metodo}.txt", "w") as f_out:
        f_out.write(f"Raiz: {raiz}\nErro: {erro}\nIterações: {it}\nTempo: {duracao:.6f}\n")


if __name__ == "__main__":
    opcoes = {
        "1": "bisseccao",
        "2": "newton_raphson",
        "3": "falsa_posicao",
        "4": "secante"
    }
    print("Escolha o método:")
    print("1 - Bissecção")
    print("2 - Newton-Raphson")
    print("3 - Falsa Posição")
    print("4 - Secante")
    escolha = input("Digite o número do método: ").strip()
    if escolha not in opcoes:
        raise ValueError("Opção inválida.")
    main("entrada.txt", opcoes[escolha])
