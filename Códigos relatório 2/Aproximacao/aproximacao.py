import math
import copy

# ==========================================
# FUNÇÕES DE APOIO E MÉTODOS MATEMÁTICOS
# ==========================================

def avaliar_funcao(expressao, x_val):
    """Avalia uma função matemática em formato de string de forma segura."""
    ambiente_seguro = {"x": x_val, "math": math}
    # Impede o uso de comandos do sistema no eval
    return eval(expressao, {"__builtins__": None}, ambiente_seguro)

def integracao_simpson(expressao, a, b, n=1000):
    """
    Calcula a integral definida de uma função usando a Regra de Simpson 1/3.
    Usaremos isso para calcular o vetor b do MMQ Contínuo.
    """
    if n % 2 != 0:
        n += 1 # O número de subintervalos deve ser par
        
    h = (b - a) / n
    soma = avaliar_funcao(expressao, a) + avaliar_funcao(expressao, b)
    
    for i in range(1, n):
        x_i = a + i * h
        f_xi = avaliar_funcao(expressao, x_i)
        if i % 2 == 0:
            soma += 2 * f_xi
        else:
            soma += 4 * f_xi
            
    return (h / 3) * soma

def eliminacao_gauss(A, b, arquivo_saida):
    """Resolve o sistema Ax = b usando Eliminação de Gauss."""
    n = len(b)
    A_copia = copy.deepcopy(A)
    b_copia = copy.deepcopy(b)
    
    arquivo_saida.write("\n[SISTEMA LINEAR] --- FASE 1: ELIMINACAO PROGRESSIVA ---\n")
    
    for k in range(n - 1):
        for i in range(k + 1, n):
            if A_copia[k][k] == 0.0:
                arquivo_saida.write("ERRO FATAL: Pivo igual a zero detectado no sistema.\n")
                return None
            
            fator = A_copia[i][k] / A_copia[k][k]
            for j in range(k + 1, n):
                A_copia[i][j] = A_copia[i][j] - fator * A_copia[k][j]
            b_copia[i] = b_copia[i] - fator * b_copia[k]
            A_copia[i][k] = 0.0
            arquivo_saida.write(f"Linha {i+1} = Linha {i+1} - ({fator:.4f}) * Linha {k+1}\n")
            
    arquivo_saida.write("\n[SISTEMA LINEAR] --- FASE 2: SUBSTITUICAO REGRESSIVA ---\n")
    
    x = [0.0] * n
    x[n - 1] = b_copia[n - 1] / A_copia[n - 1][n - 1]
    
    for i in range(n - 2, -1, -1):
        soma = b_copia[i]
        for j in range(i + 1, n):
            soma = soma - A_copia[i][j] * x[j]
        x[i] = soma / A_copia[i][i]
        
    return x

# ==========================================
# MÉTODOS DE APROXIMAÇÃO
# ==========================================

def regressao_linear(pontos, arquivo_saida):
    n = len(pontos)
    if n < 2: return None

    arquivo_saida.write("--- FASE 1: CALCULO DOS SOMATORIOS ---\n")
    soma_x, soma_y, soma_xy, soma_x2 = 0.0, 0.0, 0.0, 0.0
    
    for x, y in pontos:
        soma_x += x
        soma_y += y
        soma_xy += x * y
        soma_x2 += x ** 2
        
    denominador = (n * soma_x2) - (soma_x ** 2)
    if denominador == 0.0: return None
        
    a1 = ((n * soma_xy) - (soma_x * soma_y)) / denominador
    a0 = (soma_y - (a1 * soma_x)) / n
    return [a0, a1]

def aproximacao_polinomial_discreta(pontos, grau, arquivo_saida):
    n = len(pontos)
    m = grau + 1 
    if n < m: return None

    arquivo_saida.write(f"--- FASE 1: EQUACOES NORMAIS DISCRETAS (Grau {grau}) ---\n")
    A = [[0.0] * m for _ in range(m)]
    b = [0.0] * m
    
    for i in range(m):
        for j in range(m):
            A[i][j] = sum((p[0] ** (i + j)) for p in pontos)
        b[i] = sum((p[1] * (p[0] ** i)) for p in pontos)
        
    arquivo_saida.write("\nMatriz dos Coeficientes (Somatorios de X):\n")
    for linha in A: arquivo_saida.write(f"{[round(v, 4) for v in linha]}\n")
    arquivo_saida.write(f"\nVetor Independente (Somatorios de Y * X^i):\n")
    arquivo_saida.write(f"{[round(v, 4) for v in b]}\n")
    
    return eliminacao_gauss(A, b, arquivo_saida)

def aproximacao_polinomial_continua(funcao_str, a, b_lim, grau, arquivo_saida):
    """Calcula o MMQ Contínuo integrando as funções no intervalo [a, b_lim]."""
    m = grau + 1
    
    arquivo_saida.write(f"--- FASE 1: EQUACOES NORMAIS CONTINUAS (Grau {grau}) ---\n")
    arquivo_saida.write(f"Funcao alvo: f(x) = {funcao_str} | Intervalo: [{a}, {b_lim}]\n\n")
    
    A = [[0.0] * m for _ in range(m)]
    b = [0.0] * m
    
    # Preenchendo a matriz A com a integral exata de x^(i+j)
    # A integral de x^k dx de 'a' até 'b_lim' é (b_lim^(k+1) - a^(k+1))/(k+1)
    for i in range(m):
        for j in range(m):
            potencia = i + j
            integral_x = (b_lim**(potencia + 1) - a**(potencia + 1)) / (potencia + 1)
            A[i][j] = integral_x
            
        # Preenchendo o vetor b numéricamente: integral de f(x)*x^i
        expr_b = f"({funcao_str}) * (x**{i})"
        b[i] = integracao_simpson(expr_b, a, b_lim)

    arquivo_saida.write("Matriz dos Coeficientes (Integral de x^(i+j)):\n")
    for linha in A: arquivo_saida.write(f"{[round(v, 4) for v in linha]}\n")
    arquivo_saida.write(f"\nVetor Independente (Integral de f(x)*x^i):\n")
    arquivo_saida.write(f"{[round(v, 4) for v in b]}\n")
    
    return eliminacao_gauss(A, b, arquivo_saida)

# ==========================================
# CÓDIGO PRINCIPAL: LEITURA E MENU
# ==========================================

def ler_arquivo(caminho, opcao):
    """Adapta a leitura do arquivo dependendo do método escolhido."""
    linhas_validas = []
    with open(caminho, 'r') as file_in:
        for linha in file_in:
            if linha.strip():
                linhas_validas.append(linha.strip())
                
    if opcao in ['1', '2']: # Ler coordenadas (x, y)
        pontos = []
        for linha in linhas_validas:
            valores = list(map(float, linha.split()))
            pontos.append((valores[0], valores[1]))
        return pontos
        
    elif opcao == '3': # Ler função e intervalo
        # Exemplo de entrada esperada: math.cos(x) ; 0 , 1.5
        primeira_linha = linhas_validas[0]
        funcao_str, intervalo_str = primeira_linha.split(';')
        a_str, b_str = intervalo_str.split(',')
        return funcao_str.strip(), float(a_str), float(b_str)

def formatar_polinomio(coeficientes):
    termos = []
    for i, coef in enumerate(coeficientes):
        sinal = "+" if coef >= 0 and i > 0 else ""
        if i == 0: termos.append(f"{coef:.4f}")
        elif i == 1: termos.append(f"{sinal} {coef:.4f}x")
        else: termos.append(f"{sinal} {coef:.4f}x^{i}")
    return " ".join(termos)

def main():
    caminho_entrada = 'entrada.txt'
    caminho_saida = 'saida.txt'
    
    print("====== MENU DE ANALISE NUMERICA ======")
    print("1 - Regressao Linear")
    print("2 - Aproximacao Polinomial Discreta")
    print("3 - Aproximacao Polinomial Continua")
    print("4 - Sair")
    opcao = input("Escolha o metodo desejado: ")

    if opcao == '4':
        print("Saindo...")
        return

    try:
        dados = ler_arquivo(caminho_entrada, opcao)
    except Exception as e:
        print(f"Erro ao ler '{caminho_entrada}': Verifique se o formato bate com a opcao escolhida. Detalhe: {e}")
        return

    with open(caminho_saida, 'w') as file_out:
        if opcao in ['1', '2']:
            pontos = dados
            # Convertendo lista para exibição seguindo a regra de formatação com parênteses
            str_pontos = "( " + ", ".join([f"({x}, {y})" for x, y in pontos]) + " )"
            file_out.write(f"Lista de pontos: {str_pontos}\n\n")

            if opcao == '1':
                file_out.write("====== RELATORIO: REGRESSAO LINEAR ======\n\n")
                coeficientes = regressao_linear(pontos, file_out)
            else:
                grau = int(input("Digite o grau do polinomio desejado: "))
                file_out.write(f"====== RELATORIO: APROXIMACAO DISCRETA (Grau {grau}) ======\n\n")
                coeficientes = aproximacao_polinomial_discreta(pontos, grau, file_out)

        elif opcao == '3':
            funcao_str, a, b_lim = dados
            grau = int(input("Digite o grau do polinomio desejado para a aproximacao: "))
            file_out.write(f"====== RELATORIO: APROXIMACAO CONTINUA (Grau {grau}) ======\n\n")
            coeficientes = aproximacao_polinomial_continua(funcao_str, a, b_lim, grau, file_out)
            
        if coeficientes:
            file_out.write("\n" + "=" * 45 + "\n")
            file_out.write("RESULTADO FINAL - EQUACAO ENCONTRADA:\n")
            file_out.write(f"f(x) = {formatar_polinomio(coeficientes)}\n")
            file_out.write("=" * 45 + "\n")
            print(f"\nSucesso! Relatorio gravado em '{caminho_saida}'.")
        else:
            print("\nFalha na execucao do metodo. Verifique o arquivo de saida para erros.")

if __name__ == "__main__":
    main()
