import numpy as np
from math import *

class AproximadorNumerico:
    def __init__(self):
        self.funcoes_permitidas = {
            'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
            'exp': np.exp, 'log': np.log, 'sqrt': np.sqrt,
            'e': np.e, 'pi': np.pi
        }
    
    def calcular_regressao_linear(self, dados):
        """Calcula regressão linear com coeficiente de correlação"""
        valores_x = [ponto[0] for ponto in dados]
        valores_y = [ponto[1] for ponto in dados]
        
        n = len(valores_x)
        soma_x = sum(valores_x)
        soma_y = sum(valores_y)
        soma_xy = sum(x * y for x, y in zip(valores_x, valores_y))
        soma_x2 = sum(x ** 2 for x in valores_x)
        soma_y2 = sum(y ** 2 for y in valores_y)
        
        # Coeficientes da reta
        denominador = n * soma_x2 - soma_x ** 2
        if abs(denominador) < 1e-10:
            return "Erro: dados colineares"
        
        coeficiente_angular = (n * soma_xy - soma_x * soma_y) / denominador
        coeficiente_linear = (soma_y - coeficiente_angular * soma_x) / n
        
        # Coeficiente de correlação
        numerador_corr = n * soma_xy - soma_x * soma_y
        denominador_corr = sqrt((n * soma_x2 - soma_x ** 2) * (n * soma_y2 - soma_y ** 2))
        correlacao = numerador_corr / denominador_corr if denominador_corr != 0 else 0
        
        return {
            'equacao': f"y = {coeficiente_linear:.6f} + {coeficiente_angular:.6f}x",
            'correlacao': f"{correlacao:.6f}"
        }
    
    def ajustar_polinomio_discreto(self, dados, grau_polinomio):
        """Ajusta polinômio por mínimos quadrados para dados discretos"""
        x = np.array([p[0] for p in dados])
        y = np.array([p[1] for p in dados])
        
        # Construir matriz de Vandermonde
        matriz_vander = np.column_stack([x ** i for i in range(grau_polinomio + 1)])
        
        # Resolver sistema normal A^T A c = A^T y
        matriz_transposta = matriz_vander.T
        A = matriz_transposta @ matriz_vander
        b = matriz_transposta @ y
        
        try:
            coeficientes = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            coeficientes = np.linalg.lstsq(A, b, rcond=None)[0]
        
        # Formatar equação polinomial
        termos = []
        for expoente, coef in enumerate(coeficientes):
            if abs(coef) < 1e-10:
                continue
            if expoente == 0:
                termos.append(f"{coef:.6f}")
            elif expoente == 1:
                termos.append(f"{coef:.6f}x")
            else:
                termos.append(f"{coef:.6f}x^{expoente}")
        
        return " + ".join(termos) if termos else "0"
    
    def aproximar_funcao_continua(self, expressao_funcao, limite_inferior, limite_superior, grau_polinomio=3):
        """Aproxima função contínua por polinômio usando mínimos quadrados"""
        # Definir função a partir da expressão
        def funcao(x):
            ambiente = self.funcoes_permitidas.copy()
            ambiente['x'] = x
            return eval(expressao_funcao, {"__builtins__": None}, ambiente)
        
        # Discretizar intervalo para cálculo numérico
        num_pontos = 2000
        pontos_x = np.linspace(limite_inferior, limite_superior, num_pontos)
        
        # Calcular produtos internos
        dimensao = grau_polinomio + 1
        matriz_A = np.zeros((dimensao, dimensao))
        vetor_b = np.zeros(dimensao)
        
        for i in range(dimensao):
            for j in range(dimensao):
                # ∫ x^(i+j) dx aproximado numericamente
                potencia = pontos_x ** (i + j)
                matriz_A[i, j] = np.trapz(potencia, pontos_x)
            
            # ∫ f(x) * x^i dx
            produto = funcao(pontos_x) * (pontos_x ** i)
            vetor_b[i] = np.trapz(produto, pontos_x)
        
        try:
            coeficientes = np.linalg.solve(matriz_A, vetor_b)
        except np.linalg.LinAlgError:
            coeficientes = np.linalg.lstsq(matriz_A, vetor_b, rcond=None)[0]
        
        # Formatar polinômio resultante
        termos = []
        for expoente, coef in enumerate(coeficientes):
            if abs(coef) < 1e-10:
                continue
            if expoente == 0:
                termos.append(f"{coef:.6f}")
            elif expoente == 1:
                termos.append(f"{coef:.6f}x")
            else:
                termos.append(f"{coef:.6f}x^{expoente}")
        
        return " + ".join(termos) if termos else "0"

def processar_dados_entrada(linha):
    """Converte string de entrada em lista de tuplas (x,y)"""
    pontos = []
    for elemento in linha.split():
        try:
            x, y = map(float, elemento.split(','))
            pontos.append((x, y))
        except ValueError:
            continue
    return pontos

def executar_analise():
    aproximador = AproximadorNumerico()
    
    print("Métodos de Aproximação Numérica")
    print("1 - Regressão Linear")
    print("2 - Mínimos Quadrados - Caso Discreto")
    print("3 - Mínimos Quadrados - Caso Contínuo")
    
    opcao = input("\nSelecione o método (1-3): ").strip()
    
    try:
        with open("entrada.txt", "r") as arquivo:
            linhas = [linha.strip() for linha in arquivo if linha.strip()]
    except FileNotFoundError:
        print("Erro: arquivo 'entrada.txt' não encontrado")
        return
    
    resultados = []
    
    if opcao == "1":
        for linha in linhas:
            dados = processar_dados_entrada(linha)
            if len(dados) < 2:
                continue
            resultado = aproximador.calcular_regressao_linear(dados)
            resultados.append(f"{resultado['equacao']} | r = {resultado['correlacao']}")
        
        with open("saida.txt", "w") as arquivo:
            arquivo.write("REGRESSÃO LINEAR\n")
            arquivo.write("\n".join(resultados))
    
    elif opcao == "2":
        if not linhas:
            print("Erro: arquivo de entrada vazio")
            return
        
        try:
            grau = int(linhas[-1])
            linhas_dados = linhas[:-1]
        except ValueError:
            print("Erro: última linha deve conter o grau do polinômio")
            return
        
        for linha in linhas_dados:
            dados = processar_dados_entrada(linha)
            if len(dados) <= grau:
                resultados.append("Erro: número de pontos insuficiente para o grau especificado")
                continue
            polinomio = aproximador.ajustar_polinomio_discreto(dados, grau)
            resultados.append(f"P(x) = {polinomio}")
        
        with open("saida.txt", "w") as arquivo:
            arquivo.write("MMQ DISCRETO\n")
            arquivo.write("\n".join(resultados))
            
    elif opcao == "3":
        resultados = []
        for linha in linhas:
            if ';' in linha:
                try:
                    func_str, intervalo_str = linha.split(';')
                    a, b = map(float, intervalo_str.split(','))
                    resultado = aproximador.aproximar_funcao_continua(func_str.strip(), a, b)
                    resultados.append(f"f(x) ≈ {resultado}")
                except Exception as e:
                    resultados.append(f"Erro: {str(e)}")
            else:
                try:
                    dados = processar_dados_entrada(linha)
                    if len(dados) < 2:
                        continue

                    x_vals = [p[0] for p in dados]
                    y_vals = [p[1] for p in dados]
                    a, b = min(x_vals), max(x_vals)

                    polinomio = aproximador.ajustar_polinomio_discreto(dados, 3)  # grau 3
                    resultados.append(f"f(x) ≈ {polinomio} para x ∈ [{a}, {b}]")
                except Exception as e:
                    resultados.append(f"Erro: {str(e)}")
        
        with open("saida.txt", "w") as arquivo:
            arquivo.write("MMQ Contínuo\n")
            arquivo.write("\n".join(resultados))
    
    else:
        print("Opção inválida!")
        return
    
    print(f"\nAnálise concluída. Resultados salvos em 'saida.txt'")
    print(f"Total de conjuntos processados: {len(resultados)}")

if __name__ == "__main__":
    executar_analise()
