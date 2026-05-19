import numpy as np

# ==========================================
# FUNÇÕES DE APOIO
# ==========================================

def formatar_poly1d(p):
    """
    Transforma um objeto polinômio do NumPy (poly1d) em uma string matemática limpa e formatada.
    
    Parâmetros:
    p : Objeto poly1d da biblioteca NumPy que contém os coeficientes da equação.
    """
    termos = []
    coeficientes = p.coeffs # pega os coeficientes numéricos
    grau = len(coeficientes) - 1
    
    for i, coef in enumerate(coeficientes):
        if abs(coef) > 1e-10: # Ignora zeros gerados por imprecisão do float 
            g = grau - i
            sinal = "+" if coef >= 0 and len(termos) > 0 else ("" if coef >= 0 else "-")
            valor = abs(coef)
            
            if g == 0:
                termos.append(f"{sinal} {valor:.4f}".strip())
            elif g == 1:
                termos.append(f"{sinal} {valor:.4f}x".strip())
            else:
                termos.append(f"{sinal} {valor:.4f}x^{g}".strip())
                
    if not termos: return "0.0000"
    return " ".join(termos)

# ==========================================
# MÉTODOS DE INTERPOLAÇÃO
# ==========================================

def interpolacao_lagrange(pontos, arquivo_saida):
    """
    Calcula o polinômio interpolador para um conjunto de dados usando o Método de Lagrange.
    
    Parâmetros:
    pontos        : Lista de coordenadas (x, y) dos dados de entrada.
    arquivo_saida : Objeto do arquivo de texto para escrever o relatório passo a passo.
    """
    n = len(pontos)
    x = [p[0] for p in pontos] # separa x de y's
    y = [p[1] for p in pontos]
    
    arquivo_saida.write("--- FASE 1: CONSTRUCAO DOS POLINOMIOS BASE L_i(x) ---\n")
    
    polinomio_final = np.poly1d(0.0) # cria um objeto do NumPy que vale 0, e vai juntando as partes calculadas nele.
    
    for i in range(n): # complexidade O(n²)
        Li = np.poly1d(1.0) # polinômio base 
        denominador = 1.0
        arquivo_saida.write(f"\nCalculando L_{i}(x) para o ponto ({x[i]}, {y[i]}):\n")
        
        # constrói os multiplicadores (x - x_j) / (x_i - x_j)
        for j in range(n):
            if i != j: # evita divisão por 0 
                termo = np.poly1d([1.0, -x[j]]) # Representa (x - x_j)
                Li *= termo
                denominador *= (x[i] - x[j])
                arquivo_saida.write(f"  Multiplicando por (x - {x[j]}) / ({x[i]} - {x[j]})\n") # NumPy faz toda a álgebra complicada
        
        Li = Li / denominador
        termo_final = Li * y[i]
        polinomio_final += termo_final
        
        arquivo_saida.write(f"  L_{i}(x) resultante = {formatar_poly1d(Li)}\n")
        arquivo_saida.write(f"  Adicionando ao polinomio principal: {y[i]} * L_{i}(x)\n")
        
    return polinomio_final

def interpolacao_newton(pontos, arquivo_saida):
    """
    Calcula o polinômio interpolador para um conjunto de dados usando o Método de Newton (Diferenças Divididas).
    
    Parâmetros:
    pontos        : Lista de coordenadas (x, y) dos dados de entrada.
    arquivo_saida : Objeto do arquivo de texto para escrever o relatório com a tabela e a equação.
    """
    n = len(pontos)
    x = [p[0] for p in pontos] # separa x de y's
    y = [p[1] for p in pontos]
    
    arquivo_saida.write("--- FASE 1: TABELA DE DIFERENCAS DIVIDIDAS ---\n")
    
    # matriz para a tabela de diferenças
    dd = [[0.0] * n for _ in range(n)]
    
    # A primeira coluna é formada por y
    for i in range(n):
        dd[i][0] = y[i]
        
    # preeche as partes seguintes da tabela
    for j in range(1, n):
        for i in range(n - j):
            dd[i][j] = (dd[i+1][j-1] - dd[i][j-1]) / (x[i+j] - x[i])
            
    arquivo_saida.write("x        | Ordem 0  | Ordem 1  | ...\n")
    for i in range(n):
        linha = [f"{dd[i][j]:.4f}" for j in range(n - i)]
        arquivo_saida.write(f"{x[i]:<8.4f} | " + " | ".join(linha) + "\n")
        
    arquivo_saida.write("\n--- FASE 2: CONSTRUCAO DO POLINOMIO ---\n")
    
    # A primeira linha da tabela de diferenças contém os coeficientes da equação de Newton.
    coeficientes = dd[0] 
    arquivo_saida.write(f"Coeficientes de Newton (primeira linha da tabela):\n")
    arquivo_saida.write(f"{[round(c, 4) for c in coeficientes]}\n\n")
    
    polinomio_final = np.poly1d(0.0) # cria um objeto do NumPy que vale 0, e vai juntando as partes calculadas nele.
    termo = np.poly1d(1.0) 
    
    # Somando as partes do polinômio
    for i in range(n):
        adicao = coeficientes[i] * termo
        polinomio_final += adicao
        arquivo_saida.write(f"Passo {i+1}: Adicionando {coeficientes[i]:.4f} * ({formatar_poly1d(termo)})\n")
        
        if i < n - 1: # atualiza o multiplicador 
            termo *= np.poly1d([1.0, -x[i]])
            
    return polinomio_final

# ==========================================
# CÓDIGO PRINCIPAL: LEITURA E MENU
# ==========================================

def ler_arquivo(caminho):
    """
    Lê um conjunto de coordenadas (x, y) de um arquivo de texto para uso na interpolação.
    
    Parâmetros:
    caminho : Caminho (string) para o arquivo de texto.
    """
    pontos = []
    with open(caminho, 'r') as file_in:
        for linha in file_in:
            if linha.strip():
                valores = list(map(float, linha.strip().split()))
                pontos.append((valores[0], valores[1])) # pega o x e o y
    return pontos

def main():
    caminho_entrada = 'entrada.txt'
    caminho_saida = 'saida.txt'
    
    print("====== MENU DE INTERPOLACAO ======")
    print("1 - Metodo de Lagrange")
    print("2 - Metodo de Newton (Diferencas Divididas)")
    print("3 - Sair")
    opcao = input("Escolha o metodo desejado: ")

    if opcao == '3':
        print("Saindo...")
        return

    try:
        pontos = ler_arquivo(caminho_entrada)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_entrada}' nao foi encontrado.")
        return
    except Exception as e:
        print(f"Erro ao ler os dados: {e}")
        return

    with open(caminho_saida, 'w') as file_out:
        lista_pontos = "(" + ", ".join([f"({x}, {y})" for x, y in pontos]) + ")"
        file_out.write(f"Conjunto de dados lido: {lista_pontos}\n\n")

        if opcao == '1':
            file_out.write("====== RELATORIO: INTERPOLACAO DE LAGRANGE ======\n\n")
            polinomio = interpolacao_lagrange(pontos, file_out)
        elif opcao == '2':
            file_out.write("====== RELATORIO: INTERPOLACAO DE NEWTON ======\n\n")
            polinomio = interpolacao_newton(pontos, file_out)
        else:
            print("Opcao invalida.")
            return

        if polinomio is not None:
            file_out.write("\n" + "=" * 55 + "\n")
            file_out.write("RESULTADO FINAL - POLINOMIO INTERPOLADOR UNICO:\n")
            file_out.write(f"P(x) = {formatar_poly1d(polinomio)}\n")
            file_out.write("=" * 55 + "\n")
            print(f"\nSucesso! Relatorio gravado em '{caminho_saida}'.")
            
if __name__ == "__main__":
    main()
    