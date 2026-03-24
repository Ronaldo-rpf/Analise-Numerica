import numpy as np
import math

class CalculadorDerivadas:
    def __init__(self, passo=1e-5):
        self.passo = passo
        self.funcoes_matematicas = {
            'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            'exp': math.exp, 'log': math.log, 'sqrt': math.sqrt,
            'pi': math.pi, 'e': math.e, 'abs': abs, 'pow': math.pow
        }
    
    def computar_derivada_primeira(self, expressao, ponto_x):
        """
        Calcula a derivada de primeira ordem usando diferenças centrais
        """
        h = self.passo
        
        # Avaliar função nos pontos x+h e x-h
        f_mais = self._avaliar_expressao(expressao, ponto_x + h)
        f_menos = self._avaliar_expressao(expressao, ponto_x - h)
        
        # Aplicar fórmula das diferenças centrais
        return (f_mais - f_menos) / (2 * h)
    
    def computar_derivada_segunda(self, expressao, ponto_x):
        """
        Calcula a derivada de segunda ordem usando diferenças centrais
        """
        h = self.passo
        
        # Avaliar função nos pontos x+h, x, e x-h
        f_mais = self._avaliar_expressao(expressao, ponto_x + h)
        f_centro = self._avaliar_expressao(expressao, ponto_x)
        f_menos = self._avaliar_expressao(expressao, ponto_x - h)
        
        # Aplicar fórmula da segunda derivada
        return (f_mais - 2 * f_centro + f_menos) / (h ** 2)
    
    def _avaliar_expressao(self, expressao, valor_x):
        """
        Avalia uma expressão matemática em um ponto específico
        """
        ambiente = self.funcoes_matematicas.copy()
        ambiente['x'] = valor_x
        
        try:
            # Usar eval com ambiente restrito para segurança
            return eval(expressao, {"__builtins__": {}}, ambiente)
        except Exception as erro:
            raise ValueError(f"Erro na avaliação: {str(erro)}")

class ProcessadorArquivos:
    @staticmethod
    def carregar_dados_entrada(nome_arquivo="entrada.txt"):
        """
        Carrega e parseia o arquivo de entrada
        """
        try:
            with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
                linhas = [linha.strip() for linha in arquivo if linha.strip()]
            
            dados_processados = []
            for numero_linha, linha in enumerate(linhas, 1):
                if ';' not in linha:
                    print(f"Aviso: Linha {numero_linha} ignorada - formato inválido")
                    continue
                
                try:
                    expressao, valor_str = linha.split(';', 1)
                    expressao = expressao.strip()
                    ponto_x = float(valor_str.strip())
                    dados_processados.append((expressao, ponto_x))
                except ValueError as e:
                    print(f"Erro na linha {numero_linha}: {e}")
                    continue
            
            return dados_processados
        
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo {nome_arquivo} não encontrado")
    
    @staticmethod
    def salvar_resultados(resultados, nome_metodo, nome_arquivo="saida.txt"):
        """
        Salva os resultados no arquivo de saída
        """
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(f"Método: {nome_metodo}\n")
            
            for indice, (expressao, valor, sucesso) in enumerate(resultados, 1):
                if sucesso:
                    arquivo.write(f"Função {indice}: {valor}\n")
                else:
                    arquivo.write(f"Função {indice}: ERRO - {valor}\n")

def executar_derivacao_numerica():
    """
    Função principal para executar o sistema de derivação numérica
    """
    print("Sistema de Cálculo de Derivadas Numéricas")
    print("=" * 50)
    
    # Inicializar componentes
    calculador = CalculadorDerivadas()
    processador = ProcessadorArquivos()
    
    # Selecionar método
    print("\nMétodos disponíveis:")
    print("1 - Derivada de Primeira Ordem")
    print("2 - Derivada de Segunda Ordem")
    
    opcao = input("\nDigite sua escolha (1 ou 2): ").strip()
    
    if opcao not in ['1', '2']:
        print("Erro: Opção inválida!")
        return
    
    # Carregar dados de entrada
    try:
        dados_entrada = processador.carregar_dados_entrada()
        if not dados_entrada:
            print("Nenhum dado válido encontrado no arquivo de entrada.")
            return
    except FileNotFoundError as e:
        print(f"Erro: {e}")
        return
    
    print(f"\nProcessando {len(dados_entrada)} função(ões)...")
    
    # Processar cada função
    resultados = []
    metodo_nome = ""
    
    for expressao, ponto_x in dados_entrada:
        try:
            if opcao == '1':
                valor_derivada = calculador.computar_derivada_primeira(expressao, ponto_x)
                metodo_nome = "Derivada Numérica de Primeira Ordem"
            else:
                valor_derivada = calculador.computar_derivada_segunda(expressao, ponto_x)
                metodo_nome = "Derivada Numérica de Segunda Ordem"
            
            resultados.append((expressao, f"{valor_derivada:.6g}", True))
            
        except Exception as erro:
            resultados.append((expressao, str(erro), False))
    
    # Salvar resultados
    processador.salvar_resultados(resultados, metodo_nome)
    
    # Exibir resumo
    sucessos = sum(1 for _, _, sucesso in resultados if sucesso)
    print(f"\nProcessamento concluído:")
    print(f"- Total de funções: {len(resultados)}")
    print(f"- Calculadas com sucesso: {sucessos}")
    print(f"- Com erro: {len(resultados) - sucessos}")
    print(f"Resultados salvos em 'saida.txt'")

if __name__ == "__main__":
    executar_derivacao_numerica()
