import numpy as np

class Interpolador:
    def __init__(self):
        pass
    
    def construir_polinomio_lagrange(self, pontos):
        """
        Constrói o polinômio interpolador usando o método de Lagrange
        """
        x_valores = [p[0] for p in pontos]
        y_valores = [p[1] for p in pontos]
        n_pontos = len(pontos)
        
        # Inicializar polinômio como zero
        polinomio_final = np.poly1d(0.0)
        
        for i in range(n_pontos):
            # Construir polinômio base L_i(x)
            polinomio_base = np.poly1d(1.0)
            denominador = 1.0
            
            for j in range(n_pontos):
                if i != j:
                    # Multiplicar por (x - x_j)
                    termo = np.poly1d([1.0, -x_valores[j]])
                    polinomio_base *= termo
                    # Acumular denominador (x_i - x_j)
                    denominador *= (x_valores[i] - x_valores[j])
            
            # Normalizar o polinômio base e adicionar ao resultado
            polinomio_base /= denominador
            polinomio_final += y_valores[i] * polinomio_base
        
        return self._formatar_polinomio(polinomio_final)
    
    def construir_polinomio_newton(self, pontos):
        """
        Constrói o polinômio interpolador usando o método de Newton
        com diferenças divididas
        """
        x_valores = [p[0] for p in pontos]
        y_valores = [p[1] for p in pontos]
        n_pontos = len(pontos)
        
        # Calcular diferenças divididas
        diferencas = self._calcular_diferencas_divididas(x_valores, y_valores)
        
        # Construir polinômio incrementalmente
        polinomio_resultante = np.poly1d(0.0)
        produto_acumulado = np.poly1d(1.0)
        
        for i in range(n_pontos):
            # Adicionar termo: a_i * (x - x_0)(x - x_1)...(x - x_{i-1})
            polinomio_resultante += diferencas[i] * produto_acumulado
            
            # Atualizar produto acumulado para próximo termo
            if i < n_pontos - 1:
                produto_acumulado *= np.poly1d([1.0, -x_valores[i]])
        
        return self._formatar_polinomio(polinomio_resultante)
    
    def _calcular_diferencas_divididas(self, x_valores, y_valores):
        """
        Calcula a tabela de diferenças divididas
        """
        n = len(x_valores)
        # Inicializar tabela
        tabela = np.zeros((n, n))
        tabela[:,0] = y_valores
        
        # Preencher tabela de diferenças
        for j in range(1, n):
            for i in range(n - j):
                tabela[i,j] = (tabela[i+1,j-1] - tabela[i,j-1]) / (x_valores[i+j] - x_valores[i])
        
        # Coeficientes são a primeira linha da tabela
        return tabela[0,:]
    
    def _formatar_polinomio(self, polinomio):
        """
        Formata o polinômio para exibição amigável
        """
        coeficientes = polinomio.coeffs
        n = len(coeficientes)
        
        termos = []
        for i, coef in enumerate(coeficientes):
            potencia = n - i - 1
            # Ignorar coeficientes muito próximos de zero
            if abs(coef) < 1e-10:
                continue
            
            # Formatar termo baseado na potência
            if potencia == 0:
                termos.append(f"{coef:.4g}")
            elif potencia == 1:
                termos.append(f"{coef:.4g}x")
            else:
                termos.append(f"{coef:.4g}x^{potencia}")
        
        if not termos:
            return "P(x) ≈ 0"
        
        return "P(x) ≈ " + " + ".join(termos)

class GerenciadorArquivos:
    def __init__(self):
        pass
    
    def ler_pontos_entrada(self, nome_arquivo="entrada.txt"):
        """
        Lê os pontos de entrada do arquivo
        """
        try:
            with open(nome_arquivo, 'r') as arquivo:
                linhas = [linha.strip() for linha in arquivo if linha.strip()]
            return linhas
        except FileNotFoundError:
            print(f"Erro: Arquivo {nome_arquivo} não encontrado.")
            return []
    
    def escrever_resultados(self, resultados, metodo, nome_arquivo="saida.txt"):
        """
        Escreve os resultados no arquivo de saída
        """
        try:
            with open(nome_arquivo, 'w') as arquivo:
                arquivo.write(f"Método: {metodo}\n")
                for resultado in resultados:
                    arquivo.write(resultado + "\n")
            print(f"Resultados salvos em {nome_arquivo}")
        except Exception as e:
            print(f"Erro ao escrever arquivo: {e}")
    
    def parse_linha_pontos(self, linha):
        """
        Converte uma linha de texto em lista de pontos (x,y)
        """
        pontos = []
        for par in linha.split():
            try:
                x, y = par.split(',')
                pontos.append((float(x), float(y)))
            except ValueError:
                print(f"Aviso: Par inválido ignorado: {par}")
                continue
        return pontos

def main():
    interpolador = Interpolador()
    gerenciador = GerenciadorArquivos()
    
    print("Sistema de Interpolação Polinomial")
    print("=" * 40)
    print("1 - Método de Lagrange")
    print("2 - Método de Newton (Diferenças Divididas)")
    print("=" * 40)
    
    opcao = input("Escolha o método (1 ou 2): ").strip()
    
    # Ler dados de entrada
    linhas = gerenciador.ler_pontos_entrada()
    if not linhas:
        return
    
    resultados = []
    
    if opcao == "1":
        print("Processando interpolação de Lagrange...")
        for i, linha in enumerate(linhas):
            pontos = gerenciador.parse_linha_pontos(linha)
            if len(pontos) < 2:
                print(f"Aviso: Linha {i+1} não tem pontos suficientes")
                continue
            
            polinomio = interpolador.construir_polinomio_lagrange(pontos)
            resultados.append(polinomio)
            print(f"Conjunto {i+1}: {len(pontos)} pontos processados")
        
        gerenciador.escrever_resultados(resultados, "Interpolação de Lagrange")
    
    elif opcao == "2":
        print("Processando interpolação de Newton...")
        for i, linha in enumerate(linhas):
            pontos = gerenciador.parse_linha_pontos(linha)
            if len(pontos) < 2:
                print(f"Aviso: Linha {i+1} não tem pontos suficientes")
                continue
            
            polinomio = interpolador.construir_polinomio_newton(pontos)
            resultados.append(polinomio)
            print(f"Conjunto {i+1}: {len(pontos)} pontos processados")
        
        gerenciador.escrever_resultados(resultados, "Interpolação de Newton (Diferenças Divididas)")
    
    else:
        print("Opção inválida! Por favor, escolha 1 ou 2.")
        return
    
    print(f"\nProcessamento concluído: {len(resultados)} conjuntos interpolados")

if __name__ == "__main__":
    main()
