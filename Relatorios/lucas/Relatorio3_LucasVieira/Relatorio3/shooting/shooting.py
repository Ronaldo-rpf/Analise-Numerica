import math
import matplotlib.pyplot as plt

class Shooting:
    """Resolve um BVP de 2ª ordem y'' = f(x, y, y') via método Shooting com RK4."""

    def __init__(self, caminho_entrada="entrada.txt"):
        self.caminho_entrada = caminho_entrada

        # Variáveis carregadas do arquivo
        self.f = None
        self.a = None
        self.b = None
        self.ya = None
        self.yb = None
        self.s0 = None
        self.s1 = None
        self.h = None
        self.n = None

        # Tolerância do método secante
        self.tol = 1e-5
        self.max_iter = 100

        # Carregar dados
        self._carregar()

    def _carregar(self):
        with open(self.caminho_entrada, "r") as arq:
            linhas = [linha.strip() for linha in arq.readlines()]

        fx_str = linhas[0]
        self.a = float(linhas[1])
        self.b = float(linhas[2])
        self.ya = float(linhas[3])
        self.yb = float(linhas[4])
        self.s0 = float(linhas[5])
        self.s1 = float(linhas[6])
        self.h = float(linhas[7])

        self.n = int((self.b - self.a) / self.h)

        # Interpretador da função f(x, y, dy)
        def func(x, y, dy):
            return eval(
                fx_str,
                {
                    "x": x, "y": y, "dy": dy,
                    "math": math,
                    "sin": math.sin, "cos": math.cos,
                    "exp": math.exp, "e": math.e
                }
            )

        self.f = func

    def _rk4_segunda_ordem(self, chute):
        x = self.a
        y = self.ya
        dy = chute

        xs = [x]
        ys = [y]

        for _ in range(self.n):
            h = self.h

            k1 = h * dy
            l1 = h * self.f(x, y, dy)

            k2 = h * (dy + l1 / 2)
            l2 = h * self.f(x + h/2, y + k1/2, dy + l1/2)

            k3 = h * (dy + l2 / 2)
            l3 = h * self.f(x + h/2, y + k2/2, dy + l2/2)

            k4 = h * (dy + l3)
            l4 = h * self.f(x + h, y + k3, dy + l3)

            y += (k1 + 2*k2 + 2*k3 + k4) / 6
            dy += (l1 + 2*l2 + 2*l3 + l4) / 6
            x += h

            xs.append(x)
            ys.append(y)

        return ys[-1], xs, ys

    def resolver(self):
        f0, _, _ = self._rk4_segunda_ordem(self.s0)
        f0 -= self.yb

        f1, _, _ = self._rk4_segunda_ordem(self.s1)
        f1 -= self.yb

        for _ in range(self.max_iter):
            if abs(f1) <= self.tol:
                break

            s = self.s1 - f1 * (self.s1 - self.s0) / (f1 - f0)

            fs, xs_s, ys_s = self._rk4_segunda_ordem(s)
            fs -= self.yb

            self.s0, f0 = self.s1, f1
            self.s1, f1 = s, fs

        return xs_s, ys_s

    @staticmethod
    def salvar(caminho, xs, ys):
        with open(caminho, "w") as arq:
            arq.write("Método: Shooting\n")
            for x, y in zip(xs, ys):
                arq.write(f"x = {x:.6f}, y = {y:.6f}\n")

    @staticmethod
    def plotar(xs, ys):
        plt.figure(figsize=(8, 5))
        plt.plot(xs, ys, marker="o", linestyle="-")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Evolução da solução - Método Shooting")
        plt.grid(True)
        plt.show()


def main():
    solver = Shooting()
    xs, ys = solver.resolver()
    Shooting.salvar("saida.txt", xs, ys)
    Shooting.plotar(xs, ys)
    print("Resultados salvos em saida.txt.")


if __name__ == "__main__":
    main()
