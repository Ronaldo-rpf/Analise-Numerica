import numpy as np  # Importa NumPy para cálculos numéricos

class Integracao:
    def __init__(self, arquivo_entrada="entrada.txt"):
        self.arquivo = arquivo_entrada  # Armazena o nome do arquivo de entrada


    def avaliar_funcao(self, expressao, x_valor):
        # Define funções permitidas no ambiente do eval
        ambiente = {
            "x": x_valor,
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "exp": np.exp, "log": np.log, "sqrt": np.sqrt,
            "pi": np.pi, "e": np.e, "abs": abs, "pow": pow
        }
        try:
            # Avalia a expressão matemática em x
            return eval(expressao, {"__builtins__": None}, ambiente)
        except Exception as e:
            # Erro caso a expressão seja inválida
            raise ValueError(f"Erro avaliando '{expressao}' em x={x_valor}: {e}")

    def ler_arquivo(self):
        linhas_validas = []  # Lista para armazenar apenas entradas válidas
        with open(self.arquivo, "r") as f:
            raw = [l.strip() for l in f if l.strip()]  # Remove linhas vazias

        for i, linha in enumerate(raw, start=1):
            campos = linha.split(";")  # Divide em função; intervalo; n
            if len(campos) != 3:
                print(f"[Aviso] Linha {i} ignorada (esperado 3 campos): {linha}")
                continue
            func, intervalo_str, n_str = campos
            try:
                # Divide o intervalo "a,b"
                a_str, b_str = intervalo_str.split(",")
                a, b = float(a_str), float(b_str)  # Converte limites
                n = int(n_str)  # Converte n
                linhas_validas.append((func.strip(), (a, b), n))  # Salva a entrada válida
            except Exception as exc:
                print(f"[Erro] Linha {i} inválida: {exc}")
        return linhas_validas

  
    def salvar_resultados(self, metodo, resultados, entradas):
     arquivos = {
        "trapezio_simples": "saida_trapezio_simples.txt",
        "trapezio_multiplo": "saida_trapezio_multiplo.txt",
        "simpson_13_simples": "saida_simpson13_simples.txt",
        "simpson_13": "saida_simpson13.txt",
        "simpson_38_simples": "saida_simpson38_simples.txt",
        "simpson_38": "saida_simpson38.txt",
        "richardson": "saida_richardson.txt",
        "gauss": "saida_gauss.txt"
    }
     nome_arq = arquivos.get(metodo, "saida.txt")  # Seleciona nome do arquivo correto

     with open(nome_arq, "w") as f:
        f.write(f"=== RESULTADOS DE INTEGRAÇÃO: {metodo.upper()} ===\n\n")
        for idx, (res, entrada) in enumerate(zip(resultados, entradas), start=1):
            func, intervalo, n = entrada
            f.write(f"[Função {idx}]\n")  # Identificador da função
            f.write(f"Expressão: {func}\n")  # Função usada
            f.write(f"Intervalo: [{intervalo[0]}, {intervalo[1]}]\n")  # Intervalo a,b
            if n is not None:
                f.write(f"Subdivisões: {n}\n")  # Número de subintervalos
            f.write(f"Resultado da integral: {res:.6e}\n")  # Resultado numérico formatado
            f.write("-" * 60 + "\n")
     print(f"[OK] Resultados gravados em '{nome_arq}'.")

 
    def trapezio_unico(self, func, intervalo, n=None):
        a, b = intervalo  # Limites
        # Fórmula do trapézio simples
        return (b - a) * (self.avaliar_funcao(func, a) + self.avaliar_funcao(func, b)) / 2

    def trapezio_composto(self, func, intervalo, n):
        if n <= 0:
            raise ValueError("n deve ser positivo.")
        a, b = intervalo
        h = (b - a) / n  # Largura dos subintervalos
        xs = a + h * np.arange(n + 1)  # Pontos de integração
        ys = np.array([self.avaliar_funcao(func, x) for x in xs])  # Avaliação nos pontos
        soma = ys[0] + ys[-1] + 2 * np.sum(ys[1:-1])  # Soma ponderada
        return (h / 2) * soma  # Fórmula final

    def simpson_1_3_simples(self, func, intervalo):
        a, b = intervalo
        m = (a + b) / 2  # Ponto médio
        fa = self.avaliar_funcao(func, a)
        fm = self.avaliar_funcao(func, m)
        fb = self.avaliar_funcao(func, b)
        # Fórmula de Simpson 1/3 simples
        return (b - a) * (fa + 4 * fm + fb) / 6

    def simpson_1_3(self, func, intervalo, n):
        if n < 2: n = 2  # n mínimo
        if n % 2 != 0: n += 1  # Ajuste para ser par
        a, b = intervalo
        h = (b - a) / n
        xs = a + h * np.arange(n + 1)
        ys = np.array([self.avaliar_funcao(func, x) for x in xs])
        soma = ys[0] + ys[-1] + 4 * ys[1:-1:2].sum() + 2 * ys[2:-1:2].sum()
        return (h / 3) * soma

  
    def simpson_3_8_simples(self, func, intervalo):
        a, b = intervalo
        h = (b - a) / 3  # 3 subdivisões
        x1, x2 = a + h, a + 2 * h  # Pontos auxiliares
        fa = self.avaliar_funcao(func, a)
        f1 = self.avaliar_funcao(func, x1)
        f2 = self.avaliar_funcao(func, x2)
        fb = self.avaliar_funcao(func, b)
        return (3 * h / 8) * (fa + 3 * f1 + 3 * f2 + fb)

    def simpson_3_8(self, func, intervalo, n):
        if n < 3: n = 3  # n mínimo
        if n % 3 != 0: n += (3 - n % 3)  # Ajusta para múltiplo de 3
        a, b = intervalo
        h = (b - a) / n
        xs = a + h * np.arange(n + 1)
        ys = np.array([self.avaliar_funcao(func, x) for x in xs])
        soma = ys[0] + ys[-1] + sum([3*ys[i] if i % 3 != 0 else 2*ys[i] for i in range(1, n)])
        return (3 * h / 8) * soma

    def richardson_extrapolacao(self, func, intervalo, n):
        if n <= 0: raise ValueError("n deve ser positivo para Richardson")
        Tn = self.trapezio_composto(func, intervalo, n)  # Trapézio com n
        T2n = self.trapezio_composto(func, intervalo, 2 * n)  # Trapézio com 2n
        return (4*T2n - Tn)/3  # Fórmula de Richardson

    def gauss_legendre(self, func, intervalo, n):
        if n <= 0: raise ValueError("n deve ser >= 1 para Gauss")
        a, b = intervalo
        xi, wi = np.polynomial.legendre.leggauss(n)  # Obtém raízes e pesos
        ts = 0.5*(b - a)*xi + 0.5*(b + a)  # Mapeia para [a,b]
        ys = np.array([self.avaliar_funcao(func, t) for t in ts])  # Avaliação
        return 0.5*(b - a)*np.dot(wi, ys)  # Combinação linear com pesos


def main():
    integrador = Integracao("entrada.txt")  # Instancia o integrador

    print("Escolha o método de integração:")
    print("1 - Trapézio único")
    print("2 - Trapézio composto")
    print("3 - Simpson 1/3 simples")
    print("4 - Simpson 1/3 composto")
    print("5 - Simpson 3/8 simples")
    print("6 - Simpson 3/8 composto")
    print("7 - Richardson")
    print("8 - Quadratura de Gauss")

    opcao = input("Opção: ").strip()  # Lê a escolha do usuário
    linhas = integrador.ler_arquivo()  # Lê dados do arquivo
    if not linhas:
        print("[Erro] Nenhuma linha válida encontrada.")
        return

    resultados = []  # Guarda resultados das integrais
    metodo_chave = None  # Nome do método escolhido (para salvar arquivo)

    if opcao == "8":
        try:
            n_gauss = int(input("Informe o número de pontos Gauss (>=1): "))
            if n_gauss < 1: raise ValueError
        except Exception:
            print("[Erro] Valor inválido para n. Abortando.")
            return

    for func, intervalo, n in linhas:
        try:
            if opcao == "1":
                res = integrador.trapezio_unico(func, intervalo)
                metodo_chave = "trapezio_simples"
            elif opcao == "2":
                res = integrador.trapezio_composto(func, intervalo, n)
                metodo_chave = "trapezio_multiplo"
            elif opcao == "3":
                res = integrador.simpson_1_3_simples(func, intervalo)
                metodo_chave = "simpson_13_simples"
            elif opcao == "4":
                res = integrador.simpson_1_3(func, intervalo, n)
                metodo_chave = "simpson_13"
            elif opcao == "5":
                res = integrador.simpson_3_8_simples(func, intervalo)
                metodo_chave = "simpson_38_simples"
            elif opcao == "6":
                res = integrador.simpson_3_8(func, intervalo, n)
                metodo_chave = "simpson_38"
            elif opcao == "7":
                res = integrador.richardson_extrapolacao(func, intervalo, n)
                metodo_chave = "richardson"
            elif opcao == "8":
                res = integrador.gauss_legendre(func, intervalo, n_gauss)
                metodo_chave = "gauss"
            else:
                print("Opção inválida.")
                return
            resultados.append(res)  # Salva resultado da integração
        except Exception as e:
            print(f"[Erro] Função ignorada: {e}")

    if resultados and metodo_chave:
     integrador.salvar_resultados(metodo_chave, resultados, linhas)  # Gera arquivo final



if __name__ == "__main__":
    main()  # Executa o programa
