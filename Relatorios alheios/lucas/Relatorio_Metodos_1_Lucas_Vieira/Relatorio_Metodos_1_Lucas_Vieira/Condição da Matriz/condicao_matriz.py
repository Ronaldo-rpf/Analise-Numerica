import time
import numpy as np

class Matriz:
    def __init__(self, A):
        self.A = A.astype(float)

    def lu(self):
        n = len(self.A)
        L, U = np.eye(n), self.A.copy()
        for i in range(n):
            for j in range(i + 1, n):
                if U[i, i] == 0:
                    raise ZeroDivisionError("Pivô nulo.")
                L[j, i] = U[j, i] / U[i, i]
                U[j] -= L[j, i] * U[i]
        return L, U

    def resolver(self, L, U, b):
        n = len(b)
        y = np.zeros(n)
        for i in range(n):
            y[i] = b[i] - np.dot(L[i, :i], y[:i])
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            x[i] = (y[i] - np.dot(U[i, i+1:], x[i+1:])) / U[i, i]
        return x

    def inversa(self):
        L, U = self.lu()
        n = len(self.A)
        inv = np.zeros((n, n))
        I = np.eye(n)
        for i in range(n):
            inv[:, i] = self.resolver(L, U, I[:, i])
        return inv

    def condicao(self):
        inv = self.inversa()
        return np.linalg.norm(self.A, 2) * np.linalg.norm(inv, 2), inv

def ler_entrada(arquivo):
    with open(arquivo) as f:
        A = [list(map(float, linha.split())) for linha in f if linha.strip()]
    return np.array(A)

def main(arquivo):
    A = ler_entrada(arquivo)
    matriz = Matriz(A)

    inicio = time.time()
    numero, inv = matriz.condicao()
    duracao = time.time() - inicio

    print(f"Número de condição: {numero:.5f}")
    print(f"Tempo: {duracao:.6f}s")

    with open("saida_condicao.txt", "w") as f_out:
        f_out.write(f"Número de condição: {numero:.5f}\n")
        f_out.write("Matriz inversa:\n")
        for linha in inv:
            f_out.write(" ".join(f"{v:.5f}" for v in linha) + "\n")

if __name__ == "__main__":
    main("entrada3.txt")
