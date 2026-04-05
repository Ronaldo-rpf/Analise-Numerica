# Método Iterativo
# Usado em supercomputadores e placas de vídeo

def jacobi(A, b, arquivo_saida, max_iter=50, tolerancia=1e-2):
    """
    Resolve um sistema linear Ax = b usando o Método Iterativo de Jacobi-Richardson.

    Parâmetros:
    A             : Matriz de coeficientes (lista de listas).
    b             : Vetor de termos independentes (lista).
    arquivo_saida : Objeto de arquivo aberto para gravar o relatório.
    max_iter      : Número máximo de iterações permitidas.
    tolerancia    : Erro relativo máximo aceito para parar o loop.
    """

    n = len(A)
    x = [0.0] * n  # Chute inicial (vetor de zeros)
    
    arquivo_saida.write("--- INICIO DO METODO DE JACOBI ---\n")
    arquivo_saida.write(f"Tolerancia alvo: {tolerancia}\n\n")

    # Verificação de zeros na diagonal
    for i in range(n):
        if A[i][i] == 0.0:
            arquivo_saida.write(f"ERRO FATAL: Zero encontrado na diagonal principal na linha {i+1}. O metodo vai falhar por divisao por zero. Reorganize as linhas.\n")
            return None

    for iteracao in range(1, max_iter + 1):
        arquivo_saida.write(f"--- Iteracao {iteracao} ---\n")
        
        # Uma cópia congelada dos valores da iteração anterior
        x_antigo = list(x) 
        # Uma lista temporária para guardar os novos valores simultâneos
        x_novo = [0.0] * n 
        
        sentinela = 1 # Controle de convergência

        # Calcula todos os novos valores baseados somente no x_antigo
        for i in range(n):
            soma = b[i]
            for j in range(n):
                if i != j:
                    # Diferente do G-Seidel, aqui sempre usa o x_antigo
                    soma -= A[i][j] * x_antigo[j]
            
            x_novo[i] = soma / A[i][i]
            arquivo_saida.write(f"x({i+1}) calculado = {x_novo[i]:.6f}\n")

        # Atualiza o vetor oficial com os novos valores todos de uma vez
        x = list(x_novo)

        # Cálculo do erro relativo 
        maior_diferenca = max(abs(x[i] - x_antigo[i]) for i in range(n))
        maior_elemento = max(abs(x[i]) for i in range(n))
        
        erro_relativo = 0.0
        if maior_elemento != 0:
            erro_relativo = maior_diferenca / maior_elemento

        arquivo_saida.write(f"Erro relativo maximo atual: {erro_relativo:.6f}\n\n")

        # Verifica se o erro ficou menor que o epsilon estipulado
        if erro_relativo < tolerancia:
            arquivo_saida.write(f"CONVERGENCIA ATINGIDA na iteracao {iteracao}!\n")
            sentinela = 0
            break

    if sentinela == 1:
        arquivo_saida.write(f"AVISO: O limite de {max_iter} iteracoes foi atingido sem convergencia total. O sistema pode ser divergente.\n")

    return x

# ==========================================
# CÓDIGO PRINCIPAL: LEITURA E ESCRITA
# ==========================================

caminho_entrada = 'entrada.txt'
caminho_saida = 'saida.txt'

try:
    A = []
    b = []
    
    # Leitura do arquivo (matriz A e vetor b)
    with open(caminho_entrada, 'r') as file_in:
        linhas = file_in.readlines()
        n = int(linhas[0].strip())
        
        for i in range(1, n + 1):
            valores = list(map(float, linhas[i].strip().split()))
            A.append(valores[:-1])
            b.append(valores[-1])

    with open(caminho_saida, 'w') as file_out:
        file_out.write("====== RELATORIO DE SISTEMAS LINEARES ======\n")
        file_out.write(f"Metodo: Jacobi\n")
        file_out.write(f"Tamanho do sistema: {n}x{n}\n")
        file_out.write("============================================\n\n")

        solucao = jacobi(A, b, file_out, tolerancia=1e-2)

        if solucao:
            file_out.write("\n" + "-" * 45 + "\n")
            file_out.write("SOLUCAO FINAL ENCONTRADA:\n")
            
            pontos_solucao = "(" + ", ".join([f"{val:.4f}" for val in solucao]) + ")"
            
            file_out.write(f"Vetor x = {pontos_solucao}\n")
            file_out.write("-" * 45 + "\n")

    print(f"\nSucesso! O algoritmo de Jacobi rodou e salvou no '{caminho_saida}'.\n")

except FileNotFoundError:
    print(f"Erro: O arquivo '{caminho_entrada}' nao foi encontrado na mesma pasta.")
except Exception as e:
    print(f"Ocorreu um erro durante a execucao: {e}")

