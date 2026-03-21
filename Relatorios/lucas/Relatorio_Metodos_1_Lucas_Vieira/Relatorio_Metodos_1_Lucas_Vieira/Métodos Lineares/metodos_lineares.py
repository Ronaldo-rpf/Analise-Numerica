import time
import numpy as np


class SistemasLineares:
    def __init__(self, A, b):
        self.A = A.astype(float)
        self.b = b.astype(float)

    def gauss(self):
        A, b = self.A.copy(), self.b.copy()
        n = len(b)
        for k in range(n - 1):
            if A[k, k] == 0:
                raise ZeroDivisionError("Pivô nulo.")
            for i in range(k + 1, n):
                m = A[i, k] / A[k, k]
                A[i, k:] -= m * A[k, k:]
                b[i] -= m * b[k]
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            x[i] = (b[i] - np.dot(A[i, i + 1:], x[i + 1:])) / A[i, i]
        return x, None

    def lu(self):
        A, b = self.A.copy(), self.b.copy()
        n = len(A)
        L, U = np.eye(n), A.copy()
        for i in range(n):
            for j in range(i + 1, n):
                if U[i, i] == 0:
                    raise ZeroDivisionError("Pivô nulo.")
                L[j, i] = U[j, i] / U[i, i]
                U[j] -= L[j, i] * U[i]
        y = np.zeros(n)
        for i in range(n):
            y[i] = b[i] - np.dot(L[i, :i], y[:i])
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            x[i] = (y[i] - np.dot(U[i, i + 1:], x[i + 1:])) / U[i, i]
        return x, None

    def jacobi(self, tol=1e-10, max_iter=1000):
        A, b = self.A, self.b
        n = len(b)
        x = np.zeros(n)
        for k in range(max_iter):
            x_novo = np.copy(x)
            for i in range(n):
                s = np.dot(A[i], x) - A[i, i] * x[i]
                if A[i, i] == 0:
                    raise ZeroDivisionError("Zero na diagonal.")
                x_novo[i] = (b[i] - s) / A[i, i]

            if np.isinf(x_novo).any() or np.isnan(x_novo).any():
                return None, k

            if np.linalg.norm(x_novo - x, np.inf) < tol:
                return x_novo, k + 1
            x = x_novo
        return x, max_iter

    def seidel(self, tol=1e-10, max_iter=1000):
        A, b = self.A, self.b
        n = len(b)
        x = np.zeros(n)
        for k in range(max_iter):
            x_novo = np.copy(x)
            for i in range(n):
                s1 = np.dot(A[i, :i], x_novo[:i])
                s2 = np.dot(A[i, i + 1:], x[i + 1:])
                if A[i, i] == 0:
                    raise ZeroDivisionError("Zero na diagonal.")
                x_novo[i] = (b[i] - s1 - s2) / A[i, i]

            if np.isinf(x_novo).any() or np.isnan(x_novo).any():
                return None, k

            if np.linalg.norm(x_novo - x, np.inf) < tol:
                return x_novo, k + 1
            x = x_novo
        return x, max_iter


def ler_entrada(arquivo):
    with open(arquivo) as f:
        n = int(f.readline())
        A, b = [], []
        for _ in range(n):
            linha = list(map(float, f.readline().split()))
            A.append(linha[:-1])
            b.append(linha[-1])
    return np.array(A), np.array(b)


def main(arquivo, metodo):
    A, b = ler_entrada(arquivo)
    sistema = SistemasLineares(A, b)

    inicio = time.time()
    if metodo == "gauss":
        sol, it = sistema.gauss()
    elif metodo == "lu":
        sol, it = sistema.lu()
    elif metodo == "jacobi":
        sol, it = sistema.jacobi()
    elif metodo == "gauss_seidel":
        sol, it = sistema.seidel()
    else:
        raise ValueError("Método inválido.")
    duracao = time.time() - inicio

    solucao = [round(float(v), 6) for v in sol]
    print(f"\nMétodo: {metodo}")
    print(f"Solução: {solucao}")
    if it:
        print(f"Iterações: {it}")
    print(f"Tempo: {duracao:.6f}s")

    with open(f"saida_{metodo}.txt", "w") as f_out:
        f_out.write(f"Solução: {solucao}\n")
        if it:
            f_out.write(f"Iterações: {it}\n")
        f_out.write(f"Tempo: {duracao:.6f}\n")


if __name__ == "__main__":
    opcoes = {
        "1": "gauss",
        "2": "lu",
        "3": "jacobi",
        "4": "gauss_seidel"
    }
    print("Escolha o método:")
    print("1 - Gauss")
    print("2 - Decomposição LU")
    print("3 - Jacobi")
    print("4 - Gauss-Seidel")
    escolha = input("Digite o número do método: ").strip()
    if escolha not in opcoes:
        raise ValueError("Opção inválida.")
    main("entrada2.txt", opcoes[escolha])

