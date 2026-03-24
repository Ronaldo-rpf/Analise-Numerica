import numpy as np                                    # importa a biblioteca NumPy com o apelido `np` (operações numéricas e arrays)

class Aproximacao:                                    # define a classe `Aproximacao` que agrupará métodos de ajuste/approx
    def __init__(self):                              # método construtor da classe
        pass                                         # sem inicializações necessárias no momento (placeholder)

    def linear(self, dados):                         # método para ajustar uma reta por mínimos quadrados (regressão linear)
        xs = np.array([x for x, y in dados])        # extrai as coordenadas x de `dados` e coloca em um array NumPy
        ys = np.array([y for x, y in dados])        # extrai as coordenadas y de `dados` e coloca em um array NumPy

        media_x, media_y = np.mean(xs), np.mean(ys) # calcula as médias de x e y
        numerador = np.sum((xs - media_x) * (ys - media_y))  # soma do produto das diferenças (covariância numerador)
        denominador = np.sum((xs - media_x) ** 2)    # soma dos quadrados das diferenças de x (variância de x)

        a1 = numerador / denominador if denominador != 0 else 0.0  # coeficiente angular (slope). Protege divisão por zero.
        a0 = media_y - a1 * media_x                 # coeficiente linear (intercept) a partir das médias

        # Coeficiente de correlação (r)
        denom_r = np.sqrt(np.sum((xs - media_x) ** 2) * np.sum((ys - media_y) ** 2))
                                                     # denominador do coeficiente de correlação: sqrt(Var(x)*Var(y))
        r = numerador / denom_r if denom_r != 0 else 0.0
                                                     # coeficiente de correlação linear (Pearson). Protege divisão por zero.

        return f"y = {a0:.4e} + {a1:.4e}x | r = {r:.4f}"
                                                     # retorna uma string formatada com os coeficientes (notação científica) e r

    def mmq_discreto(self, pares, grau):             # ajuste por MMQ para dados discretos com polinômio de grau `grau`
        xs = np.array([x for x, y in pares])        # extrai x dos pares (lista de tuplas)
        ys = np.array([y for x, y in pares])        # extrai y dos pares

        # Monta matriz manualmente 
        M = np.column_stack([xs ** i for i in range(grau + 1)])
                                                     # cria matriz M cujas colunas são [1, x, x^2, ..., x^grau]
                                                     # column_stack empilha colunas formando matriz de Vandermonde (ordem crescente de potência)
        # Resolve pelo método dos quadrados mínimos (QR)
        Q, R = np.linalg.qr(M)                      # fatoração QR de M (Q ortogonal, R triangular superior)
        coef = np.linalg.solve(R, Q.T @ ys)[::-1]   # resolve R * a = Q^T * y para obter coeficientes; [::-1] inverte ordem p/ decrescente

        return self._formatar_polinomio(coef)       # formata o vetor de coeficientes em uma string apresentável (polinômio)

    def mmq_continuo(self, funcao_str, a, b, grau=3):# ajuste por MMQ para função contínua definida por `funcao_str` no intervalo [a, b]
        env = {
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "exp": np.exp, "log": np.log,
            "pi": np.pi, "e": np.e
        }                                            # ambiente seguro parcial para avaliar expressões: mapeia nomes para funções NumPy e constantes
        f = lambda x: eval(funcao_str, {**env, "x": x})
                                                     # cria função f(x) que avalia a string `funcao_str` com `eval`
                                                     # observa: usar eval tem riscos se `funcao_str` vier de fonte não confiável

        # Integração com pontos densos
        xs = np.linspace(a, b, 1500)                # gera 1500 pontos igualmente espaçados no intervalo [a, b] para integração numérica

        # Montagem do sistema via produto interno dos monômios
        A = np.zeros((grau + 1, grau + 1))          # matriz do sistema (Gram) inicializada com zeros
        B = np.zeros(grau + 1)                      # vetor do lado direito inicializado com zeros

        for i in range(grau + 1):                   # percorre as linhas (exponentes para monômios)
            for j in range(grau + 1):               # percorre as colunas
                A[i, j] = np.trapz(xs ** (i + j), xs)
                                                     # A[i,j] = integral de x^(i+j) dx sobre [a,b], aproximada por trapézio usando os pontos xs
            B[i] = np.trapz(f(xs) * xs ** i, xs)    # B[i] = integral de f(x) * x^i dx sobre [a,b], aproximada por trapézio

        coef = np.linalg.solve(A, B)[::-1]          # resolve o sistema A * coef_rev = B; [::-1] inverte para ordem decrescente
        return f"f(x) ≈ {self._formatar_polinomio(coef)}"
                                                     # retorna string com polinômio aproximante formatado

    @staticmethod
    def ler_arquivo(caminho):                        # método estático para ler arquivo de texto e retornar linhas não vazias
        with open(caminho, "r") as f:                # abre arquivo no modo leitura (garante fechamento com `with`)
            return [linha.strip() for linha in f if linha.strip()]
                                                     # lê linhas, remove espaços laterais e filtra linhas vazias

    @staticmethod
    def salvar_arquivo(nome_metodo, conteudo):       # método estático para salvar resultados em arquivo
        arquivos = {
            "Linear": "saida_regressao.txt",
            "Discreto": "saida_discreto.txt",
            "Continuo": "saida_continuo.txt"
        }                                            # mapeamento entre nome do método e nome do arquivo de saída
        nome_arquivo = arquivos.get(nome_metodo, "saida.txt")
                                                     # escolhe o nome do arquivo ou usa "saida.txt" como fallback
        with open(nome_arquivo, "w") as f:           # abre o arquivo para escrita (sobrescreve existente)
            f.write(f"=== Método: {nome_metodo} ===\n\n")
                                                     # escreve um cabeçalho identificando o método
            if isinstance(conteudo, list):           # se `conteudo` for lista (vários resultados), escreve cada conjunto
                for i, item in enumerate(conteudo, 1):
                    f.write(f"Conjunto {i}:\n{item}\n\n")
            else:
                f.write(str(conteudo) + "\n")        # se não for lista, escreve o conteúdo diretamente

    @staticmethod
    def parse_pares(linha):                           # converte uma linha de texto em pares numéricos (x,y)
        # Mais robusto: aceita separadores variados e ignora espaços extras
        import re                                   # importa o módulo de expressões regulares localmente (apenas neste escopo)
        pares = re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", linha)
                                                     # encontra todas as ocorrências de números (inteiros, decimais, notação científica) na linha
        return list(zip(map(float, pares[::2]), map(float, pares[1::2])))
                                                     # agrupa em tuplas (x,y) pegando elementos pares e ímpares da lista `pares` e convertendo para float

    @staticmethod
    def _formatar_polinomio(coef):                    # formata vetor de coeficientes em string polinomial legível
        """Formata o polinômio com sinais e potências corretas"""
        grau = len(coef) - 1                         # determina o grau do polinômio (tamanho do vetor menos 1)
        termos = []                                  # lista para acumular termos formatados
        for i, c in enumerate(coef):                 # percorre coeficientes (espera-se ordem decrescente de potência)
            pot = grau - i                           # potência associada a este coeficiente
            sinal = "+" if c >= 0 else "-"          # determina sinal do termo
            valor = abs(c)                          # usa valor absoluto para evitar sinal duplo ao formatar
            if pot == 0:
                termo = f"{sinal} {valor:.4e}"      # termo constante formatado em notação científica
            elif pot == 1:
                termo = f"{sinal} {valor:.4e}x"     # termo linear
            else:
                termo = f"{sinal} {valor:.4e}x^{pot}"# termo com potência > 1
            termos.append(termo)                    # adiciona termo à lista
        polinomio = " ".join(termos).lstrip("+ ").replace("+ -", "- ")
                                                     # junta termos em uma string, remove um "+" inicial se houver e corrige padrões "+ -"
        return f"y = {polinomio}"                    # retorna a string completa do polinômio

def main():                                         # função principal do script (ponto de entrada quando executado diretamente)
    calc = Aproximacao()                            # instancia a classe Aproximacao

    print("Selecione o método de aproximação:")     # imprime menu para o usuário
    print("1 - Regressão Linear")
    print("2 - Ajuste Discreto (MMQ)")
    print("3 - Ajuste Contínuo (MMQ)")

    opcao = input("Escolha: ").strip()             # lê a opção do usuário e remove espaços extras

    if opcao in ("1", "2"):
        dados = calc.ler_arquivo("entrada1.txt")   # para opções 1 e 2 lê o arquivo `entrada1.txt`
    elif opcao == "3":
        dados = calc.ler_arquivo("entrada2.txt")   # para opção 3 lê `entrada2.txt`
    else:
        print("Opção inválida!")                   # tratamento simples para opção inválida
        return

    if opcao == "1":
        resultados = [calc.linear(calc.parse_pares(l)) for l in dados]
                                                     # para cada linha do arquivo, parseia pares e calcula regressão linear
        calc.salvar_arquivo("Linear", resultados)   # salva os resultados em arquivo apropriado

    elif opcao == "2":
        grau = int(input("Informe o grau do polinômio: "))  # solicita ao usuário o grau do polinômio
        resultados = [calc.mmq_discreto(calc.parse_pares(l), grau) for l in dados]
                                                     # para cada linha, parseia pares e ajusta polinômio discreto de dado grau
        calc.salvar_arquivo("Discreto", resultados) # salva resultados

    elif opcao == "3":
        resultados = []
        for linha in dados:
            func_str, intervalo = linha.split(';')  # espera que cada linha tenha "expressão; a,b"
            a, b = map(float, intervalo.split(',')) # separa e converte os limites do intervalo para float
            resultados.append(calc.mmq_continuo(func_str, a, b))
                                                     # calcula a aproximação contínua para cada linha
        calc.salvar_arquivo("Continuo", resultados)# salva resultados

if __name__ == "__main__":                         # verifica se o script está sendo executado diretamente (não importado)
    main()                                         # chama a função principal
