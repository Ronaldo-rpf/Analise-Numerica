import numpy as np

class Integrador:
    def __init__(self, arquivo="entrada.txt"):
        self.arquivo = arquivo

    # --- avaliação segura da expressão ---
    def _eval(self, expr, x):
        ctx = {
            "x": x,
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "exp": np.exp, "log": np.log, "sqrt": np.sqrt,
            "pi": np.pi, "e": np.e, "abs": abs, "pow": pow
        }
        try:
            return eval(expr, {"__builtins__": None}, ctx)
        except Exception as exc:
            raise ValueError(f"Erro ao avaliar '{expr}' em x={x}: {exc}")

    # --- leitura ---
    def ler_entradas(self):
        linhas = []
        with open(self.arquivo, "r") as f:
            raw = [l.strip() for l in f if l.strip()]

        for i, linha in enumerate(raw, start=1):
            partes = linha.split(";")
            if len(partes) != 3:
                print(f"[Aviso] Linha {i} ignorada (esperado 3 campos): {linha}")
                continue
            func = partes[0].strip()
            intervalo_s = partes[1].strip()
            n_s = partes[2].strip()
            try:
                a_str, b_str = intervalo_s.split(",")
                a, b = float(a_str), float(b_str)
                n = int(n_s)
                linhas.append((func, (a, b), n))
            except Exception as exc:
                print(f"[Erro] Linha {i} inválida: {exc}")
        return linhas

    # --- salvar resultados ---
    @staticmethod
    def salvar_resultados(resultados, metodo):
        arquivo_saida = "saida_final.txt"
        with open(arquivo_saida, "a", encoding="utf-8") as f:
            f.write(f"\n[Método: {metodo}]\n")
            for i, val in enumerate(resultados, start=1):
                f.write(f"Função {i}: {val:.6e}\n")
        print(f"[OK] Resultados salvos em '{arquivo_saida}'.")

    # --- métodos numéricos ---
    def trapezio_simples(self, func, intervalo, n=None):
        a, b = intervalo
        fa = self._eval(func, a)
        fb = self._eval(func, b)
        return (b - a) * (fa + fb) / 2

    def trapezio_multiplo(self, func, intervalo, n):
        a, b = intervalo
        h = (b - a) / n
        xs = a + h * np.arange(0, n + 1)
        vals = np.array([self._eval(func, x) for x in xs])
        soma = vals[0] + vals[-1] + 2 * vals[1:-1].sum()
        return (h / 2) * soma

    def simpson_1_3(self, func, intervalo, n):
        if n < 2: n = 2
        if n % 2 != 0: n += 1
        a, b = intervalo
        h = (b - a) / n
        xs = a + h * np.arange(0, n + 1)
        vals = np.array([self._eval(func, x) for x in xs])
        soma = vals[0] + vals[-1] + 4 * vals[1:-1:2].sum() + 2 * vals[2:-1:2].sum()
        return (h / 3) * soma

    def simpson_3_8(self, func, intervalo, n):
        if n < 3: n = 3
        if n % 3 != 0: n += (3 - n % 3)
        a, b = intervalo
        h = (b - a) / n
        xs = a + h * np.arange(0, n + 1)
        vals = np.array([self._eval(func, x) for x in xs])
        soma = vals[0] + vals[-1]
        for i in range(1, n):
            soma += vals[i] * (3 if i % 3 != 0 else 2)
        return (3 * h / 8) * soma

    def richardson(self, func, intervalo, n):
        Tn = self.trapezio_multiplo(func, intervalo, n)
        T2n = self.trapezio_multiplo(func, intervalo, 2 * n)
        return (4 * T2n - Tn) / 3

    def gauss(self, func, intervalo, n):
        xi, wi = np.polynomial.legendre.leggauss(n)
        a, b = intervalo
        ts = 0.5 * (b - a) * xi + 0.5 * (b + a)
        vals = np.array([self._eval(func, t) for t in ts])
        return 0.5 * (b - a) * np.dot(wi, vals)


def main():
    integrador = Integrador("entrada.txt")
    print("Escolha o método de integração:")
    print("1 - Trapézio simples\n2 - Trapézio múltiplo\n3 - Simpson 1/3\n4 - Simpson 3/8\n5 - Richardson\n6 - Quadratura de Gauss")

    opcao = input("Opção: ").strip()
    linhas = integrador.ler_entradas()
    if not linhas: return

    resultados = []
    ng = None
    if opcao == "6":
        ng = int(input("Informe o número de pontos para Gauss (n>=1): "))

    for func, intervalo, n in linhas:
        try:
            if opcao == "1": resultados.append(integrador.trapezio_simples(func, intervalo, n)); metodo="Trapézio simples"
            elif opcao == "2": resultados.append(integrador.trapezio_multiplo(func, intervalo, n)); metodo="Trapézio múltiplo"
            elif opcao == "3": resultados.append(integrador.simpson_1_3(func, intervalo, n)); metodo="Simpson 1/3"
            elif opcao == "4": resultados.append(integrador.simpson_3_8(func, intervalo, n)); metodo="Simpson 3/8"
            elif opcao == "5": resultados.append(integrador.richardson(func, intervalo, n)); metodo="Richardson"
            elif opcao == "6": resultados.append(integrador.gauss(func, intervalo, ng)); metodo="Quadratura de Gauss"
        except Exception as e:
            resultados.append(f"Erro: {e}")

    if resultados: integrador.salvar_resultados(resultados, metodo)

if __name__ == "__main__":
    main()
2