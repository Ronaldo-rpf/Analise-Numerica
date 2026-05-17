# Método Iterativo
# É muito parecido com o método de Jacobi, mas bem mais rápido

def gauss_seidel(A, b, arquivo_saida, max_iter=50, tolerancia=1e-4, relaxamento=1.0): # Mude o relaxamento caso haja divergência, diminua ele para os valores mudarem mais suavemente
    """
    Resolve um sistema linear Ax = b usando o Método Iterativo de Gauss-Seidel.

    Parâmetros:
    A             : Matriz de coeficientes (lista de listas).
    b             : Vetor de termos independentes (lista).
    arquivo_saida : Objeto de arquivo aberto para gravar o relatório.
    max_iter      : Número máximo de iterações permitidas.
    tolerancia    : Erro relativo máximo aceito para parar o loop.
    relaxamento   : Fator lambda (1.0 = Gauss-Seidel padrão).
    """
    n = len(A)
    x = [0.0] * n  # Chute inicial (vetor de zeros)
    
    arquivo_saida.write("--- INICIO DO METODO DE GAUSS-SEIDEL ---\n")
    arquivo_saida.write(f"Tolerancia alvo: {tolerancia * 100}%\n")
    arquivo_saida.write(f"Fator de relaxamento: {relaxamento}\n\n")

    # Verificação de zeros na diagonal (Problema de Divisão por Zero)
    for i in range(n):
        if A[i][i] == 0.0:
            arquivo_saida.write(f"ERRO FATAL: Zero encontrado na diagonal principal na linha {i+1}. O metodo vai falhar por divisao por zero. Reorganize as linhas do sistema.\n")
            return None

    for iteracao in range(1, max_iter + 1):
        arquivo_saida.write(f"--- Iteracao {iteracao} ---\n")
        x_antigo = list(x)  # Guarda os valores da iteração anterior para calcular o erro, um por um
        sentinela = 1  # Variável para controlar se atingimos a tolerância (1 = erro ainda alto)

        for i in range(n): # Faz para todas as linhas
            soma = b[i]
            # Subtrai os outros termos da equação (isolando a variável da diagonal)
            for j in range(n): # Faz para todas as colunas (variáveis)
                if i != j:
                    soma -= A[i][j] * x[j]
            
            # Calcula o novo valor e aplica a fórmula de relaxamento
            novo_valor = soma / A[i][i] # Aproximação matemática de fato 
            x[i] = relaxamento * novo_valor + (1.0 - relaxamento) * x_antigo[i] # Usa na próxima iteração
            
            arquivo_saida.write(f"x({i+1}) calculado = {x[i]:.6f}\n")

        # Cálculo do erro relativo (verificando a convergência)
        maior_erro_relativo = 0.0
        for i in range(n):
            if x[i] != 0.0:
                ea = abs((x[i] - x_antigo[i]) / x[i]) 
                if ea > maior_erro_relativo:
                    maior_erro_relativo = ea

        arquivo_saida.write(f"Maior erro relativo atual: {maior_erro_relativo * 100:.6f}%\n\n")

        # Se o maior erro for menor que a tolerância, o sistema convergiu
        if maior_erro_relativo <= tolerancia:
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
    
    with open(caminho_entrada, 'r') as file_in:
        linhas = file_in.readlines()
        n = int(linhas[0].strip())
        
        for i in range(1, n + 1):
            valores = list(map(float, linhas[i].strip().split()))
            A.append(valores[:-1])
            b.append(valores[-1])

    with open(caminho_saida, 'w') as file_out:
        file_out.write("====== RELATORIO DE SISTEMAS LINEARES ======\n")
        file_out.write(f"Metodo: Gauss-Seidel\n")
        file_out.write(f"Tamanho do sistema: {n}x{n}\n")
        file_out.write("============================================\n\n")

        solucao = gauss_seidel(A, b, file_out)

        if solucao:
            file_out.write("\n" + "-" * 45 + "\n")
            file_out.write("SOLUCAO FINAL ENCONTRADA:\n")
            
            # Formatando a lista com parênteses
            pontos_solucao = "(" + ", ".join([f"{val:.4f}" for val in solucao]) + ")"
            
            file_out.write(f"Vetor x = {pontos_solucao}\n")
            file_out.write("-" * 45 + "\n")

    print(f"\nSucesso! O algoritmo de Gauss-Seidel rodou e salvou no '{caminho_saida}'.\n")

except FileNotFoundError:
    print(f"Erro: O arquivo '{caminho_entrada}' nao foi encontrado na mesma pasta.")
except Exception as e:
    print(f"Ocorreu um erro durante a execucao: {e}")