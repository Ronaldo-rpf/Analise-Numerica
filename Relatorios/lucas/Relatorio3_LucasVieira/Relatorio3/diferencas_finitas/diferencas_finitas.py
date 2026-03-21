import numpy as np
import math
import matplotlib.pyplot as plt

class DiferencasFinitas:
    def __init__(self, caminho="entrada.txt"):
        self.caminho = caminho
        self.funcao = None
        self.a = None
        self.b = None
        self.ya = None
        self.yb = None
        self.n = None
        self._carregar_entrada()

    def _carregar_entrada(self):
        with open(self.caminho, "r") as f:
            linhas = [l.strip() for l in f.readlines()]

        fx_str = linhas[0]
        self.a = float(linhas[1])
        self.b = float(linhas[2])
        self.ya = float(linhas[3])
        self.yb = float(linhas[4])
        self.n = int(linhas[5])

        env = {
            "math": math, "sin": math.sin, "cos": math.cos,
            "exp": math.exp, "e": math.e
        }

        # f(x,y)
        self.funcao = lambda x, y: eval(fx_str, {**env, "x": x, "y": y})

    def resolver(self):
        f = self.funcao
        a, b = self.a, self.b
        ya, yb = self.ya, self.yb
        n = self.n

        h = (b - a) / n
        xs = np.linspace(a, b, n + 1)

        # Matrizes
        A = np.zeros((n - 1, n - 1))
        B = np.zeros(n - 1)

        for i in range(n - 1):
            xi = a + (i + 1) * h
            y_guess = ya + (i + 1) * (yb - ya) / n

            A[i, i] = -2
            if i > 0:
                A[i, i - 1] = 1
            if i < n - 2:
                A[i, i + 1] = 1

            B[i] = h**2 * f(xi, y_guess)

        # Condições de contorno
        B[0] -= ya
        B[-1] -= yb

        y_internal = np.linalg.solve(A, B)
        ys = [ya] + list(y_internal) + [yb]

        return xs, ys

    @staticmethod
    def salvar(xs, ys, nome_metodo="Diferenças Finitas"):
        with open("saida.txt", "w") as f:
            f.write(f"Método: {nome_metodo}\n\n")
            for x, y in zip(xs, ys):
                f.write(f"x = {x:.6f}, y = {y:.6f}\n")

        print("Resultados salvos em saida.txt.")

    @staticmethod
    def plotar(xs, ys):
        plt.figure(figsize=(8, 5))
        plt.plot(xs, ys, marker="o", linestyle="-")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Evolução da solução - Diferenças Finitas")
        plt.grid(True)
        plt.show()

    def executar(self):
        xs, ys = self.resolver()
        self.salvar(xs, ys)
        self.plotar(xs, ys)


def main():
    dif = DiferencasFinitas()
    dif.executar()


if __name__ == "__main__":
    main()
