import numpy as np
import math

class IntegradorNumerico:
    def __init__(self):
        self.funcoes_matematicas = {
            'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            'exp': math.exp, 'log': math.log, 'sqrt': math.sqrt,
            'pi': math.pi, 'e': math.e, 'abs': abs, 'pow': math.pow
        }
    
    def avaliar_funcao(self, expressao, valor_x):
        """
        Avalia uma expressão matemática em um ponto específico
        """
        ambiente = self.funcoes_matematicas.copy()
        ambiente['x'] = valor_x
        
        try:
            return eval(expressao, {"__builtins__": {}}, ambiente)
        except Exception as erro:
            raise ValueError(f"Erro ao avaliar '{expressao}' em x={valor_x}: {str(erro)}")
    
    def integrar_trapezio_simples(self, expressao, limite_a, limite_b):
        """
        Calcula integral pelo método do trapézio simples
        """
        f_a = self.avaliar_funcao(expressao, limite_a)
        f_b = self.avaliar_funcao(expressao, limite_b)
        
        return (limite_b - limite_a) * (f_a + f_b) / 2
    
    def integrar_trapezio_multiplo(self, expressao, limite_a, limite_b, num_subdivisoes):
        """
        Calcula integral pelo método do trapézio múltiplo
        """
        if num_subdivisoes < 1:
            raise ValueError("Número de subdivisões deve ser positivo")
        
        largura_passo = (limite_b - limite_a) / num_subdivisoes
        soma = self.avaliar_funcao(expressao, limite_a) + self.avaliar_funcao(expressao, limite_b)
        
        for i in range(1, num_subdivisoes):
            x_i = limite_a + i * largura_passo
            soma += 2 * self.avaliar_funcao(expressao, x_i)
        
        return (largura_passo / 2) * soma
    
    def integrar_simpson_um_terco(self, expressao, limite_a, limite_b, num_subdivisoes):
        """
        Calcula integral pelo método de Simpson 1/3
        """
        if num_subdivisoes % 2 != 0:
            raise ValueError("Número de subdivisões deve ser par para Simpson 1/3")
        
        largura_passo = (limite_b - limite_a) / num_subdivisoes
        soma = self.avaliar_funcao(expressao, limite_a) + self.avaliar_funcao(expressao, limite_b)
        
        for i in range(1, num_subdivisoes):
            x_i = limite_a + i * largura_passo
            peso = 4 if i % 2 == 1 else 2
            soma += peso * self.avaliar_funcao(expressao, x_i)
        
        return (largura_passo / 3) * soma
    
    def integrar_simpson_tres_oitavos(self, expressao, limite_a, limite_b, num_subdivisoes):
        """
        Calcula integral pelo método de Simpson 3/8
        """
        if num_subdivisoes % 3 != 0:
            raise ValueError("Número de subdivisões deve ser múltiplo de 3 para Simpson 3/8")
        
        largura_passo = (limite_b - limite_a) / num_subdivisoes
        soma = self.avaliar_funcao(expressao, limite_a) + self.avaliar_funcao(expressao, limite_b)
        
        for i in range(1, num_subdivisoes):
            x_i = limite_a + i * largura_passo
            peso = 3 if i % 3 != 0 else 2
            soma += peso * self.avaliar_funcao(expressao, x_i)
        
        return (3 * largura_passo / 8) * soma
    
    def integrar_extrapolacao_richardson(self, expressao, limite_a, limite_b, num_subdivisoes):
        """
        Calcula integral usando extrapolação de Richardson
        """
        integral_n = self.integrar_trapezio_multiplo(expressao, limite_a, limite_b, num_subdivisoes)
        integral_2n = self.integrar_trapezio_multiplo(expressao, limite_a, limite_b, 2 * num_subdivisoes)
        
        return (4 * integral_2n - integral_n) / 3
    
    def integrar_quadratura_gauss(self, expressao, limite_a, limite_b, num_pontos):
        """
        Calcula integral usando quadratura de Gauss-Legendre
        """
        if num_pontos < 1:
            raise ValueError("Número de pontos deve ser positivo")
        
        # Obter pontos e pesos de Gauss-Legendre
        pontos, pesos = np.polynomial.legendre.leggauss(num_pontos)
        
        soma = 0.0
        for ponto, peso in zip(pontos, pesos):
            # Transformar do intervalo [-1, 1] para [a, b]
            x_transformado = 0.5 * (limite_b - limite_a) * ponto + 0.5 * (limite_b + limite_a)
            soma += peso * self.avaliar_funcao(expressao, x_transformado)
        
        return 0.5 * (limite_b - limite_a) * soma

class GerenciadorIntegracao:
    def __init__(self):
        self.integrador = IntegradorNumerico()

    def processar_arquivo_entrada(self, nome_arquivo="entrada.txt", requer_subdivisoes=True):
        """
        Lê e processa o arquivo de entrada
        """
        try:
            with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
                linhas = [linha.strip() for linha in arquivo if linha.strip()]
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo {nome_arquivo} não encontrado")
        
        dados_processados = []
        for numero_linha, linha in enumerate(linhas, 1):
            try:
                partes = linha.split(';')
                
                # Para trapézio simples, podemos aceitar linhas com ou sem subdivisões
                if not requer_subdivisoes:
                    if len(partes) == 2:
                        # Formato: função; intervalo
                        expressao = partes[0].strip()
                        intervalo = list(map(float, partes[1].split(',')))
                        subdivisoes = None
                    elif len(partes) == 3:
                        # Formato: função; intervalo; subdivisões (ignoramos as subdivisões)
                        expressao = partes[0].strip()
                        intervalo = list(map(float, partes[1].split(',')))
                        subdivisoes = None
                    else:
                        print(f"Aviso: Linha {numero_linha} ignorada - formato inválido")
                        continue
                else:
                    # Para outros métodos, requer exatamente 3 partes
                    if len(partes) != 3:
                        print(f"Aviso: Linha {numero_linha} ignorada - formato inválido")
                        continue
                    expressao = partes[0].strip()
                    intervalo = list(map(float, partes[1].split(',')))
                    subdivisoes = int(partes[2])
                
                if len(intervalo) != 2:
                    print(f"Aviso: Linha {numero_linha} ignorada - intervalo inválido")
                    continue
                
                dados_processados.append((expressao, intervalo, subdivisoes))
                
            except Exception as erro:
                print(f"Erro processando linha {numero_linha}: {str(erro)}")
                continue
        
        return dados_processados


    def executar_metodo_integracao(self, dados, metodo, pontos_gauss=None):
        """
        Executa o método de integração selecionado
        """
        resultados = []
        
        nomes_metodos = {
            "trapezio_simples": "Trapézio Simples",
            "trapezio_multiplo": "Trapézio Múltiplo", 
            "simpson_1_3": "Simpson 1/3",
            "simpson_3_8": "Simpson 3/8",
            "richardson": "Extrapolação de Richardson",
            "gauss": f"Quadratura de Gauss ({pontos_gauss} pontos)" if pontos_gauss else "Quadratura de Gauss"
        }
        
        nome_metodo = nomes_metodos.get(metodo, "Método Desconhecido")
        
        for expressao, intervalo, subdivisoes in dados:
            try:
                a, b = intervalo
                
                # Ajustar número de subdivisões conforme necessário
                subdiv_ajustada = subdivisoes
                
                if metodo == "simpson_1_3" and subdivisoes % 2 != 0:
                    subdiv_ajustada = subdivisoes + 1  # Tornar par
                    print(f"Aviso: Ajustando subdivisões de {subdivisoes} para {subdiv_ajustada} (método requer número par)")
                
                elif metodo == "simpson_3_8" and subdivisoes % 3 != 0:
                    subdiv_ajustada = subdivisoes + (3 - subdivisoes % 3)  # Tornar múltiplo de 3
                    print(f"Aviso: Ajustando subdivisões de {subdivisoes} para {subdiv_ajustada} (método requer múltiplo de 3)")
                
                if metodo == "trapezio_simples":
                    resultado = self.integrador.integrar_trapezio_simples(expressao, a, b)
                elif metodo == "trapezio_multiplo":
                    resultado = self.integrador.integrar_trapezio_multiplo(expressao, a, b, subdiv_ajustada)
                elif metodo == "simpson_1_3":
                    resultado = self.integrador.integrar_simpson_um_terco(expressao, a, b, subdiv_ajustada)
                elif metodo == "simpson_3_8":
                    resultado = self.integrador.integrar_simpson_tres_oitavos(expressao, a, b, subdiv_ajustada)
                elif metodo == "richardson":
                    resultado = self.integrador.integrar_extrapolacao_richardson(expressao, a, b, subdiv_ajustada)
                elif metodo == "gauss":
                    resultado = self.integrador.integrar_quadratura_gauss(expressao, a, b, pontos_gauss)
                else:
                    raise ValueError("Método de integração desconhecido")
                
                resultados.append((expressao, resultado, True))
                
            except Exception as erro:
                resultados.append((expressao, str(erro), False))
        
        return resultados, nome_metodo
    
    def salvar_resultados(self, resultados, nome_metodo, nome_arquivo="saida.txt"):
        """
        Salva os resultados no arquivo de saída
        """
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(f"Método: {nome_metodo}\n")
            
            for indice, (expressao, resultado, sucesso) in enumerate(resultados, 1):
                if sucesso:
                    arquivo.write(f"Integral da função {indice}: {resultado:.4e}\n")
                else:
                    arquivo.write(f"Integral da função {indice}: ERRO - {resultado}\n")

def main():
    """
    Função principal do sistema de integração numérica
    """
    print("Sistema de Integração Numérica")
    print("=" * 50)
    
    gerenciador = GerenciadorIntegracao()
    
    # Menu de métodos
    print("\nMétodos disponíveis:")
    print("1 - Trapézio Simples")
    print("2 - Trapézio Múltiplo")
    print("3 - Simpson 1/3")
    print("4 - Simpson 3/8")
    print("5 - Extrapolação de Richardson")
    print("6 - Quadratura de Gauss")
    
    opcao = input("\nSelecione o método (1-6): ").strip()
    
    # Configurações específicas por método
    pontos_gauss = None
    requer_subdivisoes = True
    
    if opcao == "1":
        metodo = "trapezio_simples"
        requer_subdivisoes = False
    elif opcao == "2":
        metodo = "trapezio_multiplo"
    elif opcao == "3":
        metodo = "simpson_1_3"
    elif opcao == "4":
        metodo = "simpson_3_8"
    elif opcao == "5":
        metodo = "richardson"
    elif opcao == "6":
        metodo = "gauss"
        try:
            pontos_gauss = int(input("Número de pontos para Gauss (>= 1): "))
            if pontos_gauss < 1:
                raise ValueError("Deve ser pelo menos 1")
        except ValueError as e:
            print(f"Erro: {e}")
            return
    else:
        print("Opção inválida!")
        return
    
    # Processar arquivo de entrada
    try:
        dados = gerenciador.processar_arquivo_entrada(requer_subdivisoes=requer_subdivisoes)
        if not dados:
            print("Nenhum dado válido encontrado.")
            return
    except FileNotFoundError as e:
        print(f"Erro: {e}")
        return
    
    print(f"\nProcessando {len(dados)} função(ões)...")
    
    # Executar integração
    resultados, nome_metodo = gerenciador.executar_metodo_integracao(
        dados, metodo, pontos_gauss
    )
    
    # Salvar resultados
    gerenciador.salvar_resultados(resultados, nome_metodo)
    
    # Relatório final
    sucessos = sum(1 for _, _, sucesso in resultados if sucesso)
    print(f"\nProcessamento concluído:")
    print(f"- Total de funções: {len(resultados)}")
    print(f"- Integradas com sucesso: {sucessos}")
    print(f"- Com erro: {len(resultados) - sucessos}")
    print(f"Resultados salvos em 'saida.txt'")

if __name__ == "__main__":
    main()
