import numpy as np                      # importa NumPy como 'np' para operações numéricas (vetores, polinômios, etc.)
import re                               # importa o módulo 're' para trabalhar com expressões regulares


class Interpolacao:
    def __init__(self):
        pass                            # construtor vazio: nenhuma inicialização necessária aqui


    def lagrange(self, pontos):
        # Extrai coordenadas x e y dos pontos e garante tipo float
        x_vals = np.array([p[0] for p in pontos], dtype=float)
        y_vals = np.array([p[1] for p in pontos], dtype=float)
        n = len(x_vals)                 # número de pontos

        # Construção do polinômio de Lagrange usando objetos poly1d do NumPy
        p = np.poly1d([0.0])            # inicia polinômio nulo
        for i in range(n):              # para cada ponto i
            termo = np.poly1d([1.0])    # inicia termo L_i(x) = 1
            for j in range(n):          # constrói produto (x - x_j) / (x_i - x_j) para j != i
                if i != j:
                    termo *= np.poly1d([1.0, -x_vals[j]]) / (x_vals[i] - x_vals[j])
            p += y_vals[i] * termo      # soma y_i * L_i(x) ao polinômio resultante

        # Formatação da expressão polinomial para saída legível
        termos = []
        c = p.coeffs                    # coeficientes do polinômio (ordem decrescente)
        grau = len(c) - 1               # grau do polinômio
        for i, v in enumerate(c):       # percorre coeficientes
            pot = grau - i              # potência associada ao coeficiente atual
            if abs(v) > 1e-10:         # ignora coeficientes numericamente zero
                # formata o termo: constante, linear ou potência maior que 1
                termo = f"{v:.4e}" if pot == 0 else (f"{v:.4e}·x^{pot}" if pot > 1 else f"{v:.4e}·x")
                termos.append(termo)
        expressao = " + ".join(termos) # junta termos com ' + ' para formar expressão

        # Retorna string com polinômio formatado e grau
        return (
            f"Polinômio de Lagrange:\n"
            f"P(x) ≈ {expressao}\n"
            f"Grau do polinômio: {grau}\n"
        )


    def newton(self, pontos):
        # Extrai coordenadas x e y dos pontos e garante tipo float
        x_vals = np.array([p[0] for p in pontos], dtype=float)
        y_vals = np.array([p[1] for p in pontos], dtype=float)
        n = len(x_vals)                 # número de pontos

        # Tabela triangular de diferenças divididas (n x n iniciada com zeros)
        tabela = np.zeros((n, n))
        tabela[:, 0] = y_vals           # primeira coluna é y

        # Preenche a tabela de diferenças divididas
        for j in range(1, n):           # coluna j
            for i in range(n - j):     # linha i
                tabela[i, j] = (tabela[i + 1, j - 1] - tabela[i, j - 1]) / (x_vals[i + j] - x_vals[i])
                # fórmula: f[x_i,...,x_{i+j}] = (f[x_{i+1},...,x_{i+j}] - f[x_i,...,x_{i+j-1}])/(x_{i+j}-x_i)

        coef = tabela[0, :]             # coeficientes de Newton são a primeira linha da tabela

        # Construção do polinômio de Newton a partir dos coeficientes divididos
        p = np.poly1d([0.0])            # polinômio inicial (zero)
        for i in range(n):              # para cada coeficiente
            termo = np.poly1d([1.0])    # termo multiplicativo inicial (produto de (x - x_k))
            for k in range(i):         # produto (x - x_0)(x - x_1)...(x - x_{i-1})
                termo *= np.poly1d([1.0, -x_vals[k]])
            p += coef[i] * termo       # adiciona coef[i] * produto ao polinômio resultante

        # Formatação da expressão polinomial para saída legível (mesma lógica usada em Lagrange)
        termos = []
        c = p.coeffs
        grau = len(c) - 1
        for i, v in enumerate(c):
            pot = grau - i
            if abs(v) > 1e-10:
                termo = f"{v:.4e}" if pot == 0 else (f"{v:.4e}·x^{pot}" if pot > 1 else f"{v:.4e}·x")
                termos.append(termo)
        expressao = " + ".join(termos)

        # Retorna string com polinômio de Newton e grau
        return (
            f"Polinômio de Newton:\n"
            f"P(x) ≈ {expressao}\n"
            f"Grau do polinômio: {grau}\n"
        )


    @staticmethod
    def carregar_arquivo(nome="entrada.txt"):
        # Lê arquivo e retorna lista de linhas não vazias (sem alterações nas linhas)
        with open(nome, "r") as f:
            return [linha.strip() for linha in f if linha.strip()]


    @staticmethod
    def salvar_resultados(metodo, resultados):
        # Dicionário que mapeia método para arquivo de saída correspondente
        arquivos = {
            "Lagrange": "saida_lagrange.txt",
            "Newton": "saida_newton.txt"
        }
        nome_arquivo = arquivos.get(metodo, "saida_interp.txt")  # fallback caso método não esteja no dicionário

        # Abre arquivo e escreve todos os resultados formatados
        with open(nome_arquivo, "w") as f:
            f.write(f"=== MÉTODO DE INTERPOLAÇÃO: {metodo.upper()} ===\n\n")
            for i, res in enumerate(resultados, start=1):
                f.write(f"[Conjunto {i}]\n")  # índice do conjunto de pontos
                f.write(res)                  # conteúdo retornado pelos métodos (strings formatadas)
                f.write("\n" + "-" * 60 + "\n")
        print(f"Resultados salvos em: {nome_arquivo}")  # feedback no console


    @staticmethod
    def interpretar_pares(linha):
        # Usa regex para capturar pares "x,y" possivelmente com sinais, decimais e notação científica
        pares = re.findall(r"([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?),([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)", linha)
        # Converte cada par encontrado em tupla de floats e retorna lista de tuplas (x, y)
        return [(float(x), float(y)) for x, y in pares]


def main():
    interp = Interpolacao()           # instancia objeto de interpolação

    # Menu para escolha do método
    print("Selecione o método de interpolação:")
    print("1 - Lagrange")
    print("2 - Newton")

    opcao = input("Opção: ").strip()  # lê opção do usuário e remove espaços
    linhas = interp.carregar_arquivo("entrada.txt")  # lê linhas do arquivo de entrada
    resultados = []                    # lista para acumular resultados formatados

    if opcao == "1":
        for linha in linhas:
            pares = interp.interpretar_pares(linha)  # interpreta os pares (x,y) da linha
            resultados.append(interp.lagrange(pares))# calcula polinômio de Lagrange e guarda resultado
        interp.salvar_resultados("Lagrange", resultados)  # salva tudo em arquivo correspondente

    elif opcao == "2":
        for linha in linhas:
            pares = interp.interpretar_pares(linha)  # interpreta os pares (x,y) da linha
            resultados.append(interp.newton(pares))  # calcula polinômio de Newton e guarda resultado
        interp.salvar_resultados("Newton", resultados)    # salva tudo em arquivo correspondente

    else:
        print("Opção inválida!")         # tratamento simples para opção inválida


if __name__ == "__main__":
    main()                             # executa a função principal quando o script é rodado diretamente

