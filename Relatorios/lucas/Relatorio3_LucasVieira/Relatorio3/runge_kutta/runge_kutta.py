import math
import matplotlib.pyplot as plt

class RungeKutta:
    """Resolve EDO de 1ª ordem via Runge–Kutta de 3ª e 4ª ordem."""

    def __init__(self, caminho_entrada="entrada.txt"):
        self.caminho_entrada = caminho_entrada

        # Dados do arquivo
        self.f = None
        self.x0 = None
        self.y0 = None
        self.h = None
        self.n = None

        self._carregar()

  
    def _carregar(self):
        with open(self.caminho_entrada, "r") as arq:
            linhas = [linha.strip() for linha in arq.readlines()]

        fx_str = linhas[0]
        self.x0 = float(linhas[1])
        self.y0 = float(linhas[2])
        self.h = float(linhas[3])
        self.n = int(linhas[4])

        def func(x, y):
            return eval(
                fx_str,
                {
                    "x": x, "y": y,
                    "math": math, "sin": math.sin, "cos": math.cos,
                    "exp": math.exp, "e": math.e
                }
            )

        self.f = func

  
    def resolver_rk3(self):
        x = self.x0
        y = self.y0

        xs = [x]
        ys = [y]

        for _ in range(self.n):
            k1 = self.f(x, y)
            k2 = self.f(x + self.h/2, y + (self.h * k1)/2)
            k3 = self.f(x + self.h, y - self.h*k1 + 2*self.h*k2)

            y += (self.h / 6) * (k1 + 4*k2 + k3)
            x += self.h

            xs.append(x)
            ys.append(y)

        return xs, ys

    def resolver_rk4(self):
        x = self.x0
        y = self.y0

        xs = [x]
        ys = [y]

        for _ in range(self.n):
            k1 = self.f(x, y)
            k2 = self.f(x + self.h/2, y + (self.h * k1)/2)
            k3 = self.f(x + self.h/2, y + (self.h * k2)/2)
            k4 = self.f(x + self.h, y + self.h * k3)

            y += (self.h / 6) * (k1 + 2*k2 + 2*k3 + k4)
            x += self.h

            xs.append(x)
            ys.append(y)

        return xs, ys

    @staticmethod
    def salvar(nome_arquivo, xs, ys, metodo):
        with open(nome_arquivo, "w") as arq:
            arq.write(f"Método: {metodo}\n")
            for x, y in zip(xs, ys):
                arq.write(f"x = {x:.6f}, y = {y:.6f}\n")

    @staticmethod
    def plotar(xs, ys, titulo):
        plt.figure(figsize=(8, 5))
        plt.plot(xs, ys, marker="o", linestyle="-")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title(titulo)
        plt.grid(True)
        plt.show()


def main():
    rk = RungeKutta()

    # Executar RK3
    xs3, ys3 = rk.resolver_rk3()
    RungeKutta.salvar("saida_rk3.txt", xs3, ys3, "Runge-Kutta 3ª Ordem")
    RungeKutta.plotar(xs3, ys3, "Evolução da solução - RK3")

    # Executar RK4
    xs4, ys4 = rk.resolver_rk4()
    RungeKutta.salvar("saida_rk4.txt", xs4, ys4, "Runge-Kutta 4ª Ordem")
    RungeKutta.plotar(xs4, ys4, "Evolução da solução - RK4")

    print("Resultados salvos em:")
    print(" - saida_rk3.txt")
    print(" - saida_rk4.txt")


if __name__ == "__main__":
    main()
