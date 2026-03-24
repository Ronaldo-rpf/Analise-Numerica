import numpy as np                                   # importa NumPy como np para operações numéricas (funções trig/exp, arrays, etc.)

class Derivacao:                                     # define a classe `Derivacao` que contém métodos para diferenciação numérica
    def __init__(self):                              # construtor da classe
        self.h = 1e-5  # passo de incremento pequeno    # define o passo h usado nas diferenças finitas (pequeno por padrão)

    def primeira_ordem(self, funcao, x):             # método que estima a derivada de primeira ordem centrada em x
        f_mais = self._avaliar(funcao, x + self.h)   # avalia f(x + h) usando o método privado _avaliar
        f_menos = self._avaliar(funcao, x - self.h)  # avalia f(x - h)
        return (f_mais - f_menos) / (2 * self.h)     # diferença central: (f(x+h) - f(x-h)) / (2h) → aproxima f'(x)

    def segunda_ordem(self, funcao, x):              # método que estima a segunda derivada centrada em x
        f_mais = self._avaliar(funcao, x + self.h)   # avalia f(x + h)
        f_menos = self._avaliar(funcao, x - self.h)  # avalia f(x - h)
        f_central = self._avaliar(funcao, x)         # avalia f(x)
        return (f_mais - 2 * f_central + f_menos) / (self.h ** 2)
                                                     # fórmula de diferenças centrais para segunda derivada:
                                                     # (f(x+h) - 2f(x) + f(x-h)) / h^2 → aproxima f''(x)

    def _avaliar(self, expressao, x):                 # método interno para avaliar a expressão da função em um ponto x
        env = {                                       # ambiente (dicionário) disponibilizado para eval
            "x": x,
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "exp": np.exp, "log": np.log, "sqrt": np.sqrt,
            "pi": np.pi, "e": np.e, "abs": abs, "pow": pow
        }                                             # mapeia nomes comuns para funções/constantes seguras do NumPy/builtins necessários
        try:
            return eval(expressao, {"__builtins__": None}, env)
                                                     # avalia a string `expressao` usando eval com __builtins__ desabilitado
                                                     # e apenas o dicionário `env` acessível — reduz risco, mas não elimina totalmente
        except Exception as e:
            raise ValueError(f"Erro ao avaliar '{expressao}' em x={x}: {e}")
                                                     # captura qualquer erro na avaliação e lança ValueError com mensagem clara

    @staticmethod
    def carregar_arquivo(nome="entrada.txt"):         # método estático para ler linhas não vazias de um arquivo (padrão 'entrada.txt')
        with open(nome, "r") as f:                    # abre o arquivo para leitura (garante fechamento automático)
            return [linha.strip() for linha in f if linha.strip()]
                                                     # retorna lista de linhas sem espaços laterais, ignorando linhas vazias

    @staticmethod
    def salvar_resultados(metodo, resultados):        # método estático que salva os resultados em arquivo apropriado
        arquivos = {
            "1ª Ordem": "saida_primeira_ordem.txt",
            "2ª Ordem": "saida_segunda_ordem.txt"
        }                                             # dicionário que mapeia o nome do método para o arquivo de saída
        nome_arquivo = arquivos.get(metodo, "saida_derivacao.txt")
                                                     # obtém o nome do arquivo; fallback para 'saida_derivacao.txt' se chave não existir

        with open(nome_arquivo, "w") as f:            # abre o arquivo no modo escrita (sobrescreve o existente)
            f.write(f"=== MÉTODO DE DERIVAÇÃO: {metodo.upper()} ===\n\n")
                                                     # escreve um cabeçalho identificando o método (em maiúsculas)
            for i, res in enumerate(resultados, start=1):
                f.write(f"[Função {i}]\n{res}\n")     # para cada resultado escreve um bloco com índice e o conteúdo formantado
                f.write("-" * 50 + "\n")              # separador visual entre resultados
        print(f"Resultados salvos em: {nome_arquivo}")# imprime no console o caminho do arquivo salvo

    @staticmethod
    def interpretar_linha(linha):                     # interpreta uma linha do arquivo com o formato esperado "expressão ; x0"
        """
        Interpreta uma linha do arquivo no formato:
        expressão ; x0
        """
        try:
            expr, x_str = linha.split(";")           # separa a string em duas partes usando ';' como delimitador
            return expr.strip(), float(x_str.strip())# retorna a expressão sem espaços e o valor x0 convertido para float
        except ValueError:
            raise ValueError(f"Linha inválida: '{linha}'. Esperado: f(x);x0")
                                                     # se não for possível separar/convertir lança ValueError com mensagem informativa


def main():                                         # função principal que funciona como interface de linha de comando
    deriv = Derivacao()                             # instancia a classe Derivacao (usa o h padrão definido no __init__)

    print("Selecione o tipo de derivada numérica:")  # menu para o usuário
    print("1 - Primeira Ordem (diferenças centrais)")
    print("2 - Segunda Ordem (diferenças centrais)")

    opcao = input("Opção: ").strip()                 # lê a opção do usuário e remove espaços em branco
    linhas = deriv.carregar_arquivo("entrada.txt")   # carrega as linhas do arquivo 'entrada.txt' (padrão)
    resultados = []                                  # lista para acumular resultados formatados

    if opcao == "1":
        for linha in linhas:
            func, x0 = deriv.interpretar_linha(linha)   # interpreta cada linha (expressão e ponto x0)
            try:
                val = deriv.primeira_ordem(func, x0)    # calcula a derivada de primeira ordem em x0
                resultados.append(f"f(x) = {func} | x0 = {x0} → f'(x0) ≈ {val:.6e}")
                                                     # formata a saída com notação científica e guarda na lista
            except Exception as e:
                resultados.append(f"Erro: {e}")        # registra erro ocorrido para aquela linha
        deriv.salvar_resultados("1ª Ordem", resultados) # salva todos os resultados em arquivo apropriado

    elif opcao == "2":
        for linha in linhas:
            func, x0 = deriv.interpretar_linha(linha)   # interpreta linha
            try:
                val = deriv.segunda_ordem(func, x0)     # calcula segunda derivada em x0
                resultados.append(f"f(x) = {func} | x0 = {x0} → f''(x0) ≈ {val:.6e}")
                                                     # formata resultado para segunda derivada
            except Exception as e:
                resultados.append(f"Erro: {e}")        # registra possíveis erros
        deriv.salvar_resultados("2ª Ordem", resultados) # salva resultados

    else:
        print("Opção inválida!")                       # tratamento simples para opção inválida do usuário


if __name__ == "__main__":                         # se o script for executado diretamente (não importado como módulo)
    main()                                          # executa a função principal
