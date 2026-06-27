import math

# ==========================================
# FUNÇÕES DE APOIO 
# ==========================================

def avaliar_funcao_pvc(expressao, x_val, y_val, z_val):
    """
    Avalia a função de 2ª ordem f(x, y, y') onde 'z' representa a derivada y'.
    
    Parâmetros:
    expressao : EDO em formato de string isolando y'' (que é o f(...) em si).
    x_val     : Valor da variável independente x.
    y_val     : Valor da variável dependente y.
    z_val     : Valor da derivada primeira z (y').
    """
    ambiente_seguro = {
        "x": x_val, "y": y_val, "z": z_val,
        "math": math, "e": math.e, "exp": math.exp, 
        "sin": math.sin, "cos": math.cos
    }
    return eval(expressao, {"__builtins__": None}, ambiente_seguro)

def ler_arquivo_pvc(caminho):
    """
    Lê os parâmetros do Problema de Valor de Contorno (PVC) do arquivo texto.
    Espera 7 linhas: função, x0, y0, xf, yf, h, tolerancia.

    Parâmetros:
    caminho : String com o nome/caminho do arquivo.
    """
    with open(caminho, 'r') as file_in:
        linhas = [linha.strip() for linha in file_in if linha.strip()]
        
    funcao_str = linhas[0]
    x0 = float(linhas[1])
    y0 = float(linhas[2])   # Contorno inicial
    xf = float(linhas[3])
    yf = float(linhas[4])   # Contorno final (o "alvo")
    h = float(linhas[5])
    tol = float(linhas[6])  # Tolerância de erro para aceitar o tiro
    
    return funcao_str, x0, y0, xf, yf, h, tol

def gravar_cabecalho_pvc(arquivo_saida, nome_metodo, funcao_str, x0, y0, xf, yf, h, tol):
    """
    Escreve as informações iniciais do Problema de Valor de Contorno (PVC) no arquivo de saída.
    
    Parâmetros:
    arquivo_saida : Objeto do arquivo de texto que receberá o relatório.
    nome_metodo   : String contendo o nome do método numérico em execução.
    funcao_str    : A EDO de 2ª ordem original em formato de string isolando y''.
    x0            : Valor numérico da variável independente no contorno inicial.
    y0            : Valor numérico da variável dependente no contorno inicial.
    xf            : Valor numérico da variável independente no contorno final.
    yf            : Valor numérico da variável dependente no contorno final (o alvo desejado).
    h             : Tamanho numérico do passo de incremento.
    tol           : Tolerância máxima de erro permitida para aceitar o resultado final.
    """
    arquivo_saida.write(f"====== RELATORIO: METODO {nome_metodo.upper()} ======\n\n")
    arquivo_saida.write(f"EDO de 2a Ordem: y'' = {funcao_str}\n")
    arquivo_saida.write(f"Contorno Inicial: y({x0}) = {y0}\n")
    arquivo_saida.write(f"Contorno Final (Alvo): y({xf}) = {yf}\n")
    arquivo_saida.write(f"Passo (h) = {h} | Tolerancia = {tol}\n\n")

def rk4_sistema(funcao_str, x0, y0, z0, xf, h, gravar_passos, arquivo_saida=None):
    """
    Resolve um sistema de EDOs acopladas (y' = z e z' = f(x, y, z)) usando Runge-Kutta de 4ª Ordem.
    Funciona como uma simulação para calcular o trajeto de cada tiro isolado, onde vai bater.
    
    Parâmetros:
    funcao_str    : A EDO de 2ª ordem em formato de string.
    x0            : Ponto de partida da variável independente x.
    y0            : Ponto de partida da variável dependente y.
    z0            : Inclinação inicial "chutada" para este tiro específico (z = y'), assim o problema se transforma em um PVI temporariamente.
    xf            : Ponto final de x onde o tiro deve parar para checagem.
    h             : Tamanho numérico do passo de incremento.
    gravar_passos : Booleano (True/False) indicando se deve escrever o passo a passo no arquivo de texto. 
    arquivo_saida : Objeto do arquivo de texto para relatório (opcional, por conta do gravar_passos).
    
    Retorno:
    Uma tupla contendo o valor final de y atingido no tiro (y_atual) e a lista completa de coordenadas geradas.
    """
    x_atual, y_atual, z_atual = x0, y0, z0
    pontos = [(x_atual, y_atual)]
    n = int(round((xf - x0) / h)) # quantas iterações terão 
    
    if gravar_passos and arquivo_saida: # só entra aqui no tiro "certeiro", no final 
        arquivo_saida.write("\n--- GRAVANDO TRAJETO DO TIRO CERTEIRO (Passo a Passo RK4) ---\n")
        arquivo_saida.write(f"Iteracao 0: x = {x_atual:.4f}, y = {y_atual:.4f}, z(y') = {z_atual:.4f}\n")
    
    for i in range(1, n + 1):
        # k1
        k1_y = z_atual
        k1_z = avaliar_funcao_pvc(funcao_str, x_atual, y_atual, z_atual)
        
        # k2
        k2_y = z_atual + (h / 2.0) * k1_z
        k2_z = avaliar_funcao_pvc(funcao_str, x_atual + (h / 2.0), y_atual + (h / 2.0) * k1_y, z_atual + (h / 2.0) * k1_z)
        
        # k3
        k3_y = z_atual + (h / 2.0) * k2_z
        k3_z = avaliar_funcao_pvc(funcao_str, x_atual + (h / 2.0), y_atual + (h / 2.0) * k2_y, z_atual + (h / 2.0) * k2_z)
        
        # k4
        k4_y = z_atual + h * k3_z
        k4_z = avaliar_funcao_pvc(funcao_str, x_atual + h, y_atual + h * k3_y, z_atual + h * k3_z)
        
        y_prox = y_atual + (h / 6.0) * (k1_y + 2*k2_y + 2*k3_y + k4_y)
        z_prox = z_atual + (h / 6.0) * (k1_z + 2*k2_z + 2*k3_z + k4_z)
        x_prox = x_atual + h
        
        if gravar_passos and arquivo_saida:
            arquivo_saida.write(f"Iteracao {i}: x = {x_prox:.4f} -> y_prox = {y_prox:.4f}\n")
            
        x_atual, y_atual, z_atual = x_prox, y_prox, z_prox
        pontos.append((x_atual, y_atual))
        
    return y_atual, pontos # y_atual onde o tiro acertou

# ==========================================
# MÉTODOS DE APROXIMAÇÃO PVC
# ==========================================

def metodo_shooting(funcao_str, x0, y0, xf, yf, h, tol, arquivo_saida):
    """
    Resolve um Problema de Valor de Contorno (PVC) usando o Método do Tiro (Shooting).
    Interpola os ângulos de inclinação usando o Método da Secante até atingir o alvo dentro da tolerância.
    
    Parâmetros:
    funcao_str    : A EDO de 2ª ordem original em formato de string.
    x0            : Ponto inicial de x.
    y0            : Valor inicial de y (condição de contorno 1).
    xf            : Ponto final de x.
    yf            : Valor final de y desejado (condição de contorno 2, o nosso "alvo").
    h             : Tamanho numérico do passo de incremento para o disparo.
    tol           : Tolerância máxima aceitável para o erro final em relação ao alvo.
    arquivo_saida : Objeto do arquivo de texto para escrever o relatório de calibração.
    
    Retorno:
    A lista de tuplas (x, y) contendo todas as coordenadas do trajeto do "tiro perfeito" validado.
    """
    gravar_cabecalho_pvc(arquivo_saida, "DO TIRO (SHOOTING)", funcao_str, x0, y0, xf, yf, h, tol)
    
    arquivo_saida.write("--- FASE 1: CALIBRANDO A MIRA (Metodo da Secante) ---\n")
    
    # Chute 1: A inclinação da reta que liga o ponto inicial ao alvo
    z0 = (yf - y0) / (xf - x0) if xf != x0 else 0.0 # inclinação da reta, ele tenta mirar reto na direção do alvo, mas a EDO vai puxar o disparo ou pra cima ou pra baixo
    y_final_0, _ = rk4_sistema(funcao_str, x0, y0, z0, xf, h, False)
    erro_0 = y_final_0 - yf # distância entre o local onde a bala caiu e onde ela deveria ter caído 
    
    arquivo_saida.write(f"Tiro 1: Inclinacao inicial (z0) = {z0:.4f} | Atingiu y({xf}) = {y_final_0:.4f} | Erro = {erro_0:.4f}\n")
    
    if abs(erro_0) <= tol: # se for uma linha reta já acaba
        z_vencedor = z0
    else:
        # Chute 2: Um leve incremento no ângulo
        z1 = z0 + 0.1
        y_final_1, _ = rk4_sistema(funcao_str, x0, y0, z1, xf, h, False)
        erro_1 = y_final_1 - yf
        
        arquivo_saida.write(f"Tiro 2: Inclinacao inicial (z1) = {z1:.4f} | Atingiu y({xf}) = {y_final_1:.4f} | Erro = {erro_1:.4f}\n")
        
        iteracao = 3
        max_iter = 50
        # A secante precisa de dois tiros pra começar
        # Loop da Secante para encontrar o ângulo perfeito - liga dois pontos para saber o intervalo em que o próximo tiro vai
        while abs(erro_1) > tol and iteracao <= max_iter: # enquanto a tolerância não for atingida 
            if (erro_1 - erro_0) == 0: # tiros no mesmo lugar - muito difícil
                arquivo_saida.write("FALHA: Divisao por zero na Secante.\n")
                return None
                
            # Fórmula da Secante - que vai ajustar o disparo cada vez mais
            z2 = z1 - erro_1 * (z1 - z0) / (erro_1 - erro_0) # novo ângulo calculado
            
            y_final_2, _ = rk4_sistema(funcao_str, x0, y0, z2, xf, h, False) # trajeto todo em silêncio 
            erro_2 = y_final_2 - yf
            
            arquivo_saida.write(f"Tiro {iteracao}: Inclinacao inicial ajustada (z) = {z2:.4f} | Atingiu y = {y_final_2:.4f} | Erro = {erro_2:.4f}\n")
            
            # Atualiza variáveis para o próximo tiro
            z0, erro_0 = z1, erro_1
            z1, erro_1 = z2, erro_2 # para calular o novo ângulo z2 
            iteracao += 1
            
        z_vencedor = z1

    arquivo_saida.write(f"\n=> ALVO ATINGIDO! Inclinacao ideal encontrada: z = {z_vencedor:.4f}\n")
    
    _, pontos_finais = rk4_sistema(funcao_str, x0, y0, z_vencedor, xf, h, True, arquivo_saida) # agora mostra a tragetória final
    
    arquivo_saida.write("\n" + "=" * 45 + "\n")
    arquivo_saida.write("RESULTADO FINAL - PONTOS ENCONTRADOS:\n")
    str_pontos = ", ".join([f"({x:.4f}, {y:.4f})" for x, y in pontos_finais])
    arquivo_saida.write(f"Pontos: ( {str_pontos} )\n")
    arquivo_saida.write("=" * 45 + "\n")
    
    return pontos_finais

def resolver_sistema_tridiagonal(a, b, c, d): # uma matriz com três linhas na diagonal no centro 
    """
    Resolve um sistema linear tridiagonal usando o rápido Algoritmo de Thomas.
    
    Parâmetros:
    a : Lista da diagonal inferior (tamanho n, índice 0 ignorado, pois não existe vizinho esquerdo na linha 1).
    b : Lista da diagonal principal (tamanho n, existe em todas as linhas).
    c : Lista da diagonal superior (tamanho n, índice n-1 ignorado, pois não existe vizinho direito na linha n).
    d : Lista do vetor de termos independentes (tamanho n, existe em todas as linhas).
    
    Retorno:
    Lista contendo as raízes do sistema (os valores de y para os pontos internos).
    """
    # Versão da Eliminação de Gauss (Thomas) para matrizes tridiagonais, para maior eficiência. 
    n = len(d)
    c_linha = [0.0] * n
    d_linha = [0.0] * n

    # Fase forward - ida 
    c_linha[0] = c[0] / b[0]
    d_linha[0] = d[0] / b[0]

    for i in range(1, n): # corta todos os vizinhos da esquerda, para que cada ponto dependa somente do vizinho da direita 
        denominador = b[i] - a[i] * c_linha[i-1]
        if i < n - 1:
            c_linha[i] = c[i] / denominador
        d_linha[i] = (d[i] - a[i] * d_linha[i-1]) / denominador

    # Fase backward (substituição regressiva) - volta, o último ponto descobre seu valor e agora ele volta resolvendo todos os outros 
    x = [0.0] * n
    x[-1] = d_linha[-1]
    for i in range(n - 2, -1, -1):
        x[i] = d_linha[i] - c_linha[i] * x[i+1]

    # Resolve todos os pontos internos exatos de uma vez, toda a curva.
    return x

def metodo_diferencas_finitas(funcao_str, x0, y0, xf, yf, h, tol, arquivo_saida):
    """
    Resolve um PVC linear utilizando o Método das Diferenças Finitas.
    Assume que a EDO tem a forma linear y'' = p(x)y' + q(x)y + r(x). Ou seja, p é o coeficiente de y', q de y e r de x.
    
    Parâmetros:
    funcao_str    : A EDO de 2ª ordem em formato de string (usando z para y').
    x0            : Contorno inicial da variável x.
    y0            : Contorno inicial da variável y.
    xf            : Contorno final da variável x.
    yf            : Contorno final da variável y (alvo).
    h             : Tamanho do passo.
    tol           : Tolerância (mantido como parâmetro por compatibilidade no menu, mas ignorado em métodos diretos).
    arquivo_saida : Objeto do arquivo de texto para relatar a montagem e resolução do sistema.
    
    Retorno:
    A lista completa de coordenadas contendo os contornos e os pontos internos calculados.
    """
    gravar_cabecalho_pvc(arquivo_saida, "DIFERENCAS FINITAS", funcao_str, x0, y0, xf, yf, h, tol)
    
    n_passos = int(round((xf - x0) / h))
    n_pontos_internos = n_passos - 1
    
    if n_pontos_internos <= 0:
        arquivo_saida.write("ERRO: O passo (h) e muito grande. Nenhum ponto interno para calcular.\n")
        return None
        
    arquivo_saida.write("--- FASE 1: EXTRAINDO COEFICIENTES p(x), q(x), r(x) ---\n")
    arquivo_saida.write("Assumindo EDO linear da forma: y'' = p(x)*y' + q(x)*y + r(x)\n\n")
    
    # Listas para o Algoritmo de Thomas
    a = [0.0] * n_pontos_internos
    b = [0.0] * n_pontos_internos
    c = [0.0] * n_pontos_internos
    d = [0.0] * n_pontos_internos
    
    xs = [x0 + i * h for i in range(1, n_pontos_internos + 1)] # Todos os pontos do eixo x, toda a sua malha
    
    arquivo_saida.write("--- FASE 2: MONTANDO O SISTEMA TRIDIAGONAL ---\n")
    
    for i in range(n_pontos_internos):
        xi = xs[i]
        
        # Truque para extrair p, q, r dinamicamente da string
        r_i = avaliar_funcao_pvc(funcao_str, xi, 0, 0)          # Se zerarmos o q e o p sobra o r.
        q_i = avaliar_funcao_pvc(funcao_str, xi, 1, 0) - r_i    # Zeramos o p e como já sabemos quanto vale r subtraímos ele.
        p_i = avaliar_funcao_pvc(funcao_str, xi, 0, 1) - r_i    # Mesma ideia do q.
        
        # Formulação das Diferenças Finitas Centrais
        coef_y_ant = -(1.0 + (h / 2.0) * p_i)   # a
        coef_y_atual = (2.0 + (h ** 2) * q_i)   # b
        coef_y_prox = -(1.0 - (h / 2.0) * p_i)  # c
        termo_indep = -(h ** 2) * r_i           # d
        
        # Ajustando os limites das bordas (onde conhecemos y0 e yf)
        if i == 0: # se for o primeiro ponto não tem a, porque ele é o próprio y0
            termo_indep -= coef_y_ant * y0
            b[i] = coef_y_atual
            c[i] = coef_y_prox
        elif i == n_pontos_internos - 1: # se for o último ponto não tem c, porque ele é o próprio yf  
            termo_indep -= coef_y_prox * yf
            a[i] = coef_y_ant
            b[i] = coef_y_atual
        else: # se for os do meio possuem todos e guardamos nas letras normalmente
            a[i] = coef_y_ant
            b[i] = coef_y_atual
            c[i] = coef_y_prox
            
        d[i] = termo_indep
        
        arquivo_saida.write(f"Ponto interno {i+1} (x = {xi:.4f}): p={p_i:.4f}, q={q_i:.4f}, r={r_i:.4f}\n")
        arquivo_saida.write(f"  Eq: ({coef_y_ant:.4f})*y_{i} + ({coef_y_atual:.4f})*y_{i+1} + ({coef_y_prox:.4f})*y_{i+2} = {termo_indep:.4f}\n")

    arquivo_saida.write("\n--- FASE 3: RESOLVENDO O SISTEMA (Algoritmo de Thomas) ---\n")
    
    ys_internos = resolver_sistema_tridiagonal(a, b, c, d)
    
    # Agrupando os pontos calculados com as bordas originais
    pontos_finais = [(x0, y0)]
    for i in range(n_pontos_internos): # os x's
        pontos_finais.append((xs[i], ys_internos[i])) # agrupa com os respectivos y's
    pontos_finais.append((xf, yf))
    
    arquivo_saida.write("\n" + "=" * 45 + "\n")
    arquivo_saida.write("RESULTADO FINAL - PONTOS ENCONTRADOS:\n")
    str_pontos = ", ".join([f"({x:.4f}, {y:.4f})" for x, y in pontos_finais])
    arquivo_saida.write(f"Pontos: ( {str_pontos} )\n")
    arquivo_saida.write("=" * 45 + "\n")
    
    return pontos_finais

# ==========================================
# CÓDIGO PRINCIPAL
# ==========================================

def main():
    caminho_entrada = 'entrada.txt'
    caminho_saida = 'saida.txt'
    
    print("====== RESOLUCAO DE EDOs (PVC) ======")
    print("1 - Metodo do Tiro (Shooting)")
    print("2 - Metodo das Diferencas Finitas")
    print("3 - Sair")
    opcao = input("Escolha o metodo desejado: ")

    if opcao == '3':
        print("Saindo...")
        return

    try:
        funcao_str, x0, y0, xf, yf, h, tol = ler_arquivo_pvc(caminho_entrada)
    except Exception as e:
        print(f"Erro ao ler '{caminho_entrada}'. Verifique se o formato tem 7 linhas. Detalhe: {e}")
        return

    with open(caminho_saida, 'w') as file_out:
        if opcao == '1':
            pontos = metodo_shooting(funcao_str, x0, y0, xf, yf, h, tol, file_out)
        elif opcao == '2':
            pontos = metodo_diferencas_finitas(funcao_str, x0, y0, xf, yf, h, tol, file_out)
        else:
            print("Opcao invalida.")
            return
            
        if pontos:
            print(f"\nSucesso! Relatorio gravado em '{caminho_saida}'.")

if __name__ == "__main__":
    main()

