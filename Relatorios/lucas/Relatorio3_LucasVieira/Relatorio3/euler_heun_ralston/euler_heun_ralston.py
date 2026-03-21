import math
import matplotlib.pyplot as plt  # ← IMPORTAÇÃO DO GRÁFICO

class EulerHeunRalston:
    def __init__(self, caminho="entrada.txt"):
        self.caminho = caminho
        self.funcao = None
        self.x0 = None
        self.y0 = None
        self.h = None
        self.n = None
        self._carregar_entrada()

    def _carregar_entrada(self):
        with open(self.caminho, "r") as f:
            linhas = [l.strip() for l in f.readlines()]

        func_str = linhas[0]
        self.x0 = float(linhas[1])
        self.y0 = float(linhas[2])
        self.h = float(linhas[3])
        self.n = int(linhas[4])

        env = {
            "math": math, "sin": math.sin, "cos": math.cos,
            "exp": math.exp, "e": math.e
        }

        self.funcao = lambda x, y: eval(func_str, {**env, "x": x, "y": y})

    def euler(self):
        return self._resolver(lambda x, y: y + self.h * self.funcao(x, y))

    def euler_modificado(self):
        def passo(x, y):
            k1 = self.funcao(x, y)
            k2 = self.funcao(x + self.h, y + self.h * k1)
            return y + (self.h / 2) * (k1 + k2)
        return self._resolver(passo)

    def heun(self):
        def passo(x, y):
            k1 = self.funcao(x, y)
            k2 = self.funcao(x + self.h, y + self.h * k1)
            return y + (self.h / 2) * (k1 + k2)
        return self._resolver(passo)

    def ralston(self):
        def passo(x, y):
            k1 = self.funcao(x, y)
            k2 = self.funcao(x + (3/4)*self.h, y + (3/4)*self.h * k1)
            return y + (self.h/3) * (k1 + 2*k2)
        return self._resolver(passo)

    def _resolver(self, passo_func):
        xs, ys = [self.x0], [self.y0]
        x, y = self.x0, self.y0

        for _ in range(self.n):
            y = passo_func(x, y)
            x += self.h
            xs.append(x)
            ys.append(y)

        return xs, ys

    @staticmethod
    def salvar(nome_metodo, xs, ys):
        arquivos = {
            "Euler": "saida_euler.txt",
            "Euler Modificado": "saida_euler_modificado.txt",
            "Heun": "saida_heun.txt",
            "Ralston": "saida_ralston.txt"
        }

        arq = arquivos.get(nome_metodo, "saida.txt")
        with open(arq, "w") as f:
            f.write(f"Método: {nome_metodo}\n\n")
            for x, y in zip(xs, ys):
                f.write(f"x = {x:.6f}, y = {y:.6f}\n")

        print(f"Resultados salvos em {arq}.")

    # ------------------------------------------------------------
    # FUNÇÃO NOVA: GERAR GRÁFICO
    # ------------------------------------------------------------
    def gerar_grafico(self, xs, ys, metodo):
        plt.figure(figsize=(8, 5))
        plt.plot(xs, ys, marker="o")
        plt.title(f"Evolução da Solução - Método: {metodo}")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    # ------------------------------------------------------------
    # Interface principal
    # ------------------------------------------------------------
    def executar(self):
        print("Escolha o método:")
        print("1 - Euler")
        print("2 - Euler Modificado")
        print("3 - Heun")
        print("4 - Ralston")

        escolha = input("Digite o número do método: ").strip()

        metodos = {
            "1": (self.euler, "Euler"),
            "2": (self.euler_modificado, "Euler Modificado"),
            "3": (self.heun, "Heun"),
            "4": (self.ralston, "Ralston")
        }

        if escolha not in metodos:
            print("Opção inválida.")
            return

        metodo_func, nome = metodos[escolha]
        xs, ys = metodo_func()
        
        self.salvar(nome, xs, ys)
        self.gerar_grafico(xs, ys, nome)  # ← GERANDO O GRÁFICO


def main():
    edo = EulerHeunRalston()
    edo.executar()


if __name__ == "__main__":
    main()
