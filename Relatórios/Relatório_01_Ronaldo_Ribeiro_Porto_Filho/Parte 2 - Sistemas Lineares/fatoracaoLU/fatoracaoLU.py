# Método Direto
# Menos uso computacional para quando os valores de b mudarem, dividi a matriz A em dua A = LU, mas quando muda b não precisaria recalcular LU de novo
# A matriz deve ser quadrada, pivô não pode ser 0, arredondamentos erram às vezes

def fatoracao_lu(A, b, arquivo_saida):
    """
    Resolve um sistema linear Ax = b usando Fatoração LU.

    Parâmetros:
    A             : Matriz de coeficientes (lista de listas).
    b             : Vetor de termos independentes (lista).
    arquivo_saida : Objeto de arquivo aberto para gravar o relatório.
    """

    n = len(A)
    
    # Cria as matrizes L e U vazias (preenchidas com zeros)
    L = [[0.0] * n for _ in range(n)] # 1's na diagonal principal e abaixo dela os fatores, o resto é 0.
    U = [[0.0] * n for _ in range(n)] # Primeira fase do método de Gauss, números abaixo da diagonal principal zerados.
    
    arquivo_saida.write("--- FASE 1: FATORACAO A = L * U ---\n")
    
    # Inicializa a diagonal principal de L com 1s 
    for i in range(n):
        L[i][i] = 1.0

    # Processo de Decomposição
    for i in range(n): # Primeiro calcula toda a linha i da matriz U, depois toda a coluna i da matriz L
        # Laço para preencher a matriz U (linha i, coluna j)
        for j in range(i, n): 
            soma = 0.0
            for k in range(i):
                soma += L[i][k] * U[k][j] # Coluna vezes linha 
            U[i][j] = A[i][j] - soma
            
        # Laço para preencher a matriz L (linha j, coluna i)
        for j in range(i + 1, n): # Anda pelas linhas 
            # Verificação da armadilha da divisão por zero
            if U[i][i] == 0.0:
                arquivo_saida.write(f"\nERRO FATAL: Pivo U[{i}][{i}] e zero. A fatoracao falhou.\n")
                return None
                
            soma = 0.0
            for k in range(i):
                soma += L[j][k] * U[k][i]
            L[j][i] = (A[j][i] - soma) / U[i][i] # Pivô na diagonal igual no Gauss 

    # Imprime as matrizes no relatório para você conferir
    arquivo_saida.write("\nMatriz [L] (Inferior com os fatores):\n")
    for linha in L: # Percorre todas as linha
        arquivo_saida.write("  " + "  ".join([f"{val:8.4f}" for val in linha]) + "\n") # Percorre as colunas
        
    arquivo_saida.write("\nMatriz [U] (Superior):\n")
    for linha in U:
        arquivo_saida.write("  " + "  ".join([f"{val:8.4f}" for val in linha]) + "\n")

    arquivo_saida.write("\n--- FASE 2: SUBSTITUICAO PROGRESSIVA (L * y = b) ---\n") # De cima pra baixo
    y = [0.0] * n
    for i in range(n):
        soma = 0.0
        for j in range(i):
            soma += L[i][j] * y[j] # Percorre as colunas de L e as linhas de 'y'
        y[i] = b[i] - soma # Parecido com o processo da fase 1, não tem divisão porque a diagonal principal tem 1's (álgebra pura)
        arquivo_saida.write(f"y({i+1}) = {y[i]:.4f}\n")

    arquivo_saida.write("\n--- FASE 3: SUBSTITUICAO REGRESSIVA (U * x = y) ---\n") # A resposta real (x) a partir do vetor 'y' anterior - De baixo pra cima, igual no Gauss
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        soma = 0.0
        for j in range(i + 1, n): # na diagonal e à direita dela, não roda o primeiro loop 
            soma += U[i][j] * x[j]
        x[i] = (y[i] - soma) / U[i][i] # (álgebra pura)
        arquivo_saida.write(f"x({i+1}) = {x[i]:.4f}\n")

    return x

# ==========================================
# CÓDIGO PRINCIPAL: LEITURA E ESCRITA
# ==========================================

caminho_entrada = 'entrada.txt'
caminho_saida = 'saida.txt'

try:
    A = []
    b = []
    
    with open(caminho_entrada, 'r') as file_in:
        linhas = file_in.readlines()
        n = int(linhas[0].strip())
        
        for iteracao in range(1, n + 1):
            valores = list(map(float, linhas[iteracao].strip().split()))
            A.append(valores[:-1])
            b.append(valores[-1])

    with open(caminho_saida, 'w') as file_out:
        file_out.write("====== RELATORIO DE SISTEMAS LINEARES ======\n")
        file_out.write(f"Metodo: Fatoracao LU\n")
        file_out.write(f"Tamanho do sistema: {n}x{n}\n")
        file_out.write("============================================\n\n")

        solucao = fatoracao_lu(A, b, file_out)

        if solucao:
            file_out.write("\n" + "-" * 45 + "\n")
            file_out.write("SOLUCAO FINAL ENCONTRADA:\n")
            # Formatando a lista de pontos com parênteses
            pontos_solucao = "(" + ", ".join([f"{val:.4f}" for val in solucao]) + ")"
            file_out.write(f"Vetor x = {pontos_solucao}\n")
            file_out.write("-" * 45 + "\n")

    print(f"\nSucesso! O algoritmo de Fatoracao LU rodou e salvou no '{caminho_saida}'.\n")

except FileNotFoundError:
    print(f"Erro: O arquivo '{caminho_entrada}' nao foi encontrado na mesma pasta.")
except Exception as e:
    print(f"Ocorreu um erro durante a execucao: {e}")