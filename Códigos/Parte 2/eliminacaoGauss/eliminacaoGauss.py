
def eliminacao_gauss(A, b, arquivo_saida):
    """
    Resolve um sistema linear Ax = b usando Eliminação de Gauss Ingênua.
    
    Parâmetros:
    A             : Matriz de coeficientes (lista de listas).
    b             : Vetor de termos independentes (lista).
    arquivo_saida : Objeto de arquivo aberto para gravar o relatório.
    """
    n = len(b) # Diz o tamanho do sistema
    
    arquivo_saida.write("--- FASE 1: ELIMINACAO PROGRESSIVA ---\n")
    
    # Passo 1: Eliminação Progressiva - zera tudo abaixo da diagonal principal
    # O laço 'k' avança pela diagonal principal (os pivôs)
    for k in range(n - 1): # Não chega na última coluna porque não há nada abaixo para zerar
        arquivo_saida.write(f"\nEliminando variaveis abaixo do pivo A({k+1}, {k+1}) = {A[k][k]}:\n")
        
        # O laço 'i' desce nas linhas abaixo do pivô para zerar os elementos
        for i in range(k + 1, n): # Sempre embaixo do pivô
            
            # Verificação da divisão por zero, se o pivô for 0
            if A[k][k] == 0.0:
                arquivo_saida.write("ERRO FATAL: Pivo igual a zero detectado. O metodo falhou.\n")
                return None # Retorna uma lista vazia
            
            # Calcula o fator (multiplicador)
            fator = A[i][k] / A[k][k]
            
            # O laço 'j' percorre as colunas atualizando os valores da linha 'i', aplicando de fato o fator, pula a primeira coluna porque ela já será 0
            for j in range(k + 1, n):
                A[i][j] = A[i][j] - fator * A[k][j]
            
            # Atualiza o termo independente (lado direito da equação) da linha 'i'
            b[i] = b[i] - fator * b[k]
            
            # Força o valor abaixo do pivô a ser exatamente zero para evitar possíveis arredondamentos, que nem são gerados porque a conta não é feita
            A[i][k] = 0.0
            
            # Grava o progresso no arquivo
            arquivo_saida.write(f"Linha {i+1} = Linha {i+1} - ({fator:.4f}) * Linha {k+1}\n")
            
    arquivo_saida.write("\n--- FASE 2: SUBSTITUICAO REGRESSIVA ---\n")
    
    # Passo 2: Substituição Regressiva - substitui os valores encontrados
    x = [0.0] * n  # Cria um vetor vazio para armazenar as respostas
    
    # Calcula o último x (xn) isoladamente, pois a última linha só tem 1 variável
    x[n - 1] = b[n - 1] / A[n - 1][n - 1]
    arquivo_saida.write(f"x({n}) = {x[n-1]:.4f}\n")
    
    # Resolve as equações de baixo para cima
    for i in range(n - 2, -1, -1):
        soma = b[i] # lado direito da equação
        for j in range(i + 1, n):
            soma = soma - A[i][j] * x[j] # Passa todos os termos conhecidos pro lado direito da equação
        x[i] = soma / A[i][i] # Guarda o próximo valor encontrado
        arquivo_saida.write(f"x({i+1}) = {x[i]:.4f}\n")
        
    return x # Retorna a lista com as soluções das variáveis

# ==========================================
# CÓDIGO PRINCIPAL: LEITURA E ESCRITA
# ==========================================

caminho_entrada = 'entrada.txt'
caminho_saida = 'saida.txt'

try:
    # Lendo os dados da matriz do arquivo de entrada
    A = []
    b = []
    
    with open(caminho_entrada, 'r') as file_in:
        linhas = file_in.readlines()
        
        # A primeira linha diz o tamanho do sistema (n)
        n = int(linhas[0].strip())
        
        # As próximas linhas contêm a matriz aumentada
        for iteracao in range(1, n + 1):
            # Transforma a linha do txt em uma lista de floats, e vai fazendo isso com todas as linhas da iteração
            valores = list(map(float, linhas[iteracao].strip().split()))
            
            # Tudo até o penúltimo é a matriz A, o último é o vetor b
            A.append(valores[:-1]) # Esse fatiamento não inclui o último elemento
            b.append(valores[-1]) # Pega somente o último elemento

    # Criando o arquivo de saída e executando o método
    with open(caminho_saida, 'w') as file_out:
        
        file_out.write("====== RELATORIO DE SISTEMAS LINEARES ======\n")
        file_out.write(f"Tamanho do sistema: {n}x{n}\n")
        file_out.write("============================================\n\n")

        solucao = eliminacao_gauss(A, b, file_out)

        if solucao:
            file_out.write("\n" + "-" * 45 + "\n")
            file_out.write("SOLUCAO FINAL ENCONTRADA:\n")
            
            # Formatando a lista de pontos com parênteses
            pontos_solucao = "(" + ", ".join([f"{val:.4f}" for val in solucao]) + ")"
            file_out.write(f"Vetor x = {pontos_solucao}\n")
            file_out.write("-" * 45 + "\n")

    print(f"\nSucesso! Os calculos de matriz foram realizados e salvos no arquivo '{caminho_saida}'.\n")

except FileNotFoundError:
    print(f"Erro: O arquivo '{caminho_entrada}' nao foi encontrado na mesma pasta.")
except Exception as e:
    print(f"Ocorreu um erro durante a execucao: {e}")