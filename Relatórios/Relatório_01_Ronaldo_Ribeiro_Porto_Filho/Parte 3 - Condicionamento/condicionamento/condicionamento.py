
def norma_infinita(matriz):
    """
    Calcula a Norma Infinita (Norma Linha) de uma matriz.
    É a maior soma dos valores absolutos dos elementos de uma linha.
    """
    maior_soma = 0.0
    for linha in matriz:
        soma_linha = sum(abs(x) for x in linha)
        if soma_linha > maior_soma:
            maior_soma = soma_linha
    return maior_soma

def fatoracao_lu(A):
    """
    Realiza a Fase 1 da Fatoracao LU (descobre L e U).
    """
    n = len(A)
    L = [[0.0] * n for _ in range(n)]
    U = [[0.0] * n for _ in range(n)]

    # Inicializa a diagonal principal de L com 1s 
    for i in range(n):
        L[i][i] = 1.0

    # Processo de Decomposicao
    for i in range(n):
        # Laco para preencher a matriz U
        for j in range(i, n): 
            soma = 0.0
            for k in range(i):
                soma += L[i][k] * U[k][j]
            U[i][j] = A[i][j] - soma
            
        # Laco para preencher a matriz L
        for j in range(i + 1, n): 
            # Verificacao da divisao por zero
            if U[i][i] == 0.0:
                return None, None # Retorna vazio indicando falha
                
            soma = 0.0
            for k in range(i):
                soma += L[j][k] * U[k][i]
            L[j][i] = (A[j][i] - soma) / U[i][i]

    return L, U

def resolver_lu(L, U, b):
    """
    Realiza as Fases 2 e 3 do algoritmo LU (Substituicao Progressiva e Regressiva).
    """
    n = len(b)
    
    # FASE 2: SUBSTITUICAO PROGRESSIVA (L * y = b)
    y = [0.0] * n
    for i in range(n):
        soma = 0.0
        for j in range(i):
            soma += L[i][j] * y[j]
        y[i] = b[i] - soma

    # FASE 3: SUBSTITUICAO REGRESSIVA (U * x = y)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        soma = 0.0
        for j in range(i + 1, n): 
            soma += U[i][j] * x[j]
        x[i] = (y[i] - soma) / U[i][i]
        
    return x

def calcular_matriz_inversa(A):
    """
    Calcula a matriz inversa resolvendo o sistema A*x = I usando Fatoração LU repetidas vezes.
    """
    n = len(A)
    # Fase 1 apenas uma vez
    L, U = fatoracao_lu(A)
    
    if L is None:
        return None # Falhou, pivô zero

    inversa = [[0.0] * n for _ in range(n)]

    # Para cada coluna da Matriz Identidade, rodam as Fases 2 e 3
    for j in range(n):
        # Cria a coluna j da Identidade (tudo zero, exceto o elemento j que é 1)
        vetor_identidade = [0.0] * n
        vetor_identidade[j] = 1.0

        # Encontra a coluna j da matriz inversa
        coluna_inversa = resolver_lu(L, U, vetor_identidade)

        # Transfere o resultado para a matriz inversa final
        for i in range(n):
            inversa[i][j] = coluna_inversa[i]

    return inversa

def analise_condicionamento(A, arquivo_saida):
    """
    Orquestra o cálculo do número de condição e grava o relatório.
    """
    n = len(A)
    arquivo_saida.write("--- PASSO 1: CALCULO DA NORMA DE [A] ---\n")
    norma_A = norma_infinita(A)
    arquivo_saida.write(f"Norma Infinita de A = {norma_A:.5f}\n\n")

    arquivo_saida.write("--- PASSO 2: CALCULO DA MATRIZ INVERSA ---\n")
    arquivo_saida.write("Utilizando Fatoracao LU para resolver A*x = I\n")
    inversa = calcular_matriz_inversa(A)
    
    if inversa is None:
        arquivo_saida.write("ERRO: Matriz singular. Nao e possivel calcular a inversa nem o condicionamento.\n")
        return

    arquivo_saida.write("Matriz Inversa [A^-1] encontrada com sucesso.\n\n")

    arquivo_saida.write("--- PASSO 3: CALCULO DA NORMA DE [A^-1] ---\n")
    norma_inversa = norma_infinita(inversa)
    arquivo_saida.write(f"Norma Infinita de A^-1 = {norma_inversa:.5f}\n\n")

    arquivo_saida.write("--- PASSO 4: NUMERO DE CONDICAO ---\n")
    condicionamento = norma_A * norma_inversa
    arquivo_saida.write(f"Cond(A) = ||A|| * ||A^-1||\n")
    arquivo_saida.write(f"Cond(A) = {norma_A:.5f} * {norma_inversa:.5f}\n")
    arquivo_saida.write(f"Cond(A) = {condicionamento:.5f}\n\n")

    # Avaliação do resultado
    arquivo_saida.write("--- AVALIACAO FINAL ---\n")
    if condicionamento < 100:
        arquivo_saida.write("Status: Matriz BEM CONDICIONADA. Solucoes serao estaveis.\n")
    elif condicionamento < 10000:
        arquivo_saida.write("Status: Matriz com CONDICIONAMENTO MODERADO. Fique atento a erros de precisao.\n")
    else:
        arquivo_saida.write("Status: Matriz MAL CONDICIONADA! O sistema e hipersensivel a perturbacoes.\n")

    return condicionamento, inversa

# ==========================================
# CÓDIGO PRINCIPAL: LEITURA E ESCRITA
# ==========================================

caminho_entrada = 'entrada.txt'
caminho_saida = 'saida.txt'

try:
    A = []
    
    with open(caminho_entrada, 'r') as file_in:
        linhas = file_in.readlines()
        for linha in linhas:
            if linha.strip(): # Ignora linhas em branco
                valores = list(map(float, linha.strip().split()))
                A.append(valores)

    n = len(A)

    with open(caminho_saida, 'w') as file_out:
        file_out.write("====== RELATORIO DE CONDICIONAMENTO ======\n")
        file_out.write(f"Tamanho da matriz: {n}x{n}\n")
        file_out.write("Norma utilizada: Norma Infinita (Norma Linha)\n")
        file_out.write("==============================================\n\n")

        resultado = analise_condicionamento(A, file_out)

        if resultado:
            condicionamento, inversa = resultado
            file_out.write("\n" + "-" * 50 + "\n")
            file_out.write("VISUALIZACAO DA MATRIZ INVERSA GERADA:\n")
            for linha in inversa:
                # Formatando como uma tupla de valores
                linha_formatada = "(" + ", ".join([f"{val:8.5f}" for val in linha]) + ")"
                file_out.write(linha_formatada + "\n")
            file_out.write("-" * 50 + "\n")

    print(f"\nSucesso! A analise de condicionamento rodou e salvou no '{caminho_saida}'.\n")

except FileNotFoundError:
    print(f"Erro: O arquivo '{caminho_entrada}' nao foi encontrado na mesma pasta.")
except Exception as e:
    print(f"Ocorreu um erro durante a execucao: {e}")