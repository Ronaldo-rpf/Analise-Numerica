import math

# ==========================================
# FUNÇÕES DE APOIO 
# ==========================================

def avaliar_funcao_edo(expressao, x_val, y_val):
    """
    Avalia uma função matemática f(x, y) em formato de string para o python ler sem problemas.

    Parâmetros:
    expressao : A string contendo a função matemática.
    x_val     : O valor numérico que substituirá a variável 'x' na expressão.
    y_val     : O valor numérico que substituirá a variável 'y' na expressão.
    """
    ambiente_seguro = {
        "x": x_val, "y": y_val, # onde tiver x substitua por x_val e etc.
        "math": math, "e": math.e, "exp": math.exp, 
        "sin": math.sin, "cos": math.cos
    }
    # Transforma a expressão em código executável injetando os valores atuais de x e y
    return eval(expressao, {"__builtins__": None}, ambiente_seguro)

def ler_arquivo_edo(caminho):
    """
    Lê os parâmetros do Problema de Valor Inicial (PVI) do arquivo texto.
    
    Parâmetros:
    caminho : String com o nome/caminho do arquivo.
    """
    with open(caminho, 'r') as file_in:
        linhas = [linha.strip() for linha in file_in if linha.strip()]
        
    funcao_str = linhas[0]
    x0 = float(linhas[1])
    y0 = float(linhas[2])
    h = float(linhas[3])
    n = int(linhas[4])
    
    return funcao_str, x0, y0, h, n

def gravar_cabecalho_relatorio(arquivo_saida, nome_metodo, funcao_str, x0, y0, h, n):
    """
    Escreve as informações iniciais do problema no arquivo de saída.
    """
    arquivo_saida.write(f"====== RELATORIO: METODO DE {nome_metodo.upper()} ======\n\n")
    arquivo_saida.write(f"Equacao Diferencial: dy/dx = {funcao_str}\n")
    arquivo_saida.write(f"Condicoes Iniciais: x0 = {x0}, y0 = {y0}\n")
    arquivo_saida.write(f"Passo (h) = {h} | Iteracoes (n) = {n}\n\n")
    arquivo_saida.write("--- INICIANDO ITERACOES ---\n")

def formatar_e_gravar_resultado(arquivo_saida, pontos):
    """
    Formata a lista de pontos processados e escreve o resultado final no arquivo.
    """
    arquivo_saida.write("\n" + "=" * 45 + "\n")
    arquivo_saida.write("RESULTADO FINAL - PONTOS ENCONTRADOS:\n")
    
    str_pontos = ", ".join([f"({x:.4f}, {y:.4f})" for x, y in pontos])
    arquivo_saida.write(f"Pontos: ( {str_pontos} )\n")
    arquivo_saida.write("=" * 45 + "\n")

# ==========================================
# MÉTODOS DE APROXIMAÇÃO
# ==========================================

def metodo_euler(funcao_str, x0, y0, h, n, arquivo_saida):
    """
    Resolve uma EDO utilizando o Método de Euler Simples.
    Ele assume que a inclinação inicial se mantém constante durante todo o passo.
    """
    gravar_cabecalho_relatorio(arquivo_saida, "Euler", funcao_str, x0, y0, h, n)
    
    x_atual, y_atual = x0, y0
    pontos = [(x_atual, y_atual)] # Lista para guardar as coordenadas para o relatório
    arquivo_saida.write(f"Iteracao 0: x = {x_atual:.4f}, y = {y_atual:.4f}\n")
    
    for i in range(1, n + 1):
        # Passo 1: Calcular a inclinação f(x, y) no ponto atual
        f_xy = avaliar_funcao_edo(funcao_str, x_atual, y_atual) # retorna o valor da derivada nesses pontos, a inclinação da reta tangente.
        
        # Passo 2: Calcular o próximo y usando a fórmula de Euler
        y_prox = y_atual + h * f_xy
        x_prox = x_atual + h
        
        arquivo_saida.write(f"Iteracao {i}: f({x_atual:.4f}, {y_atual:.4f}) = {f_xy:.4f} -> y_prox = {y_prox:.4f}\n")
        
        # Atualiza as variáveis para a próxima iteração
        x_atual, y_atual = x_prox, y_prox
        pontos.append((x_atual, y_atual))
        
    formatar_e_gravar_resultado(arquivo_saida, pontos)
    return pontos

def metodo_heun(funcao_str, x0, y0, h, n, arquivo_saida):
    """
    Resolve uma EDO utilizando o Método de Heun (Preditor-Corretor).
    Ele tenta prever o ponto final e usa a média das inclinações (inicial e final) para dar o passo real.
    """
    gravar_cabecalho_relatorio(arquivo_saida, "Heun (Preditor-Corretor)", funcao_str, x0, y0, h, n)
    
    x_atual, y_atual = x0, y0
    pontos = [(x_atual, y_atual)]
    arquivo_saida.write(f"Iteracao 0: x = {x_atual:.4f}, y = {y_atual:.4f}\n")
    
    for i in range(1, n + 1):
        # ETAPA PREDITORA
        # Calcula a inclinação no ponto inicial (k1)
        f_xy1 = avaliar_funcao_edo(funcao_str, x_atual, y_atual)
        
        # Faz um "chute" de onde estará o ponto final do passo usando Euler simples
        x_prox = x_atual + h
        y_predito = y_atual + h * f_xy1
        
        # ETAPA CORRETORA
        # Calcula a inclinação no ponto que foi predito (k2)
        f_xy2 = avaliar_funcao_edo(funcao_str, x_prox, y_predito)
        
        # Calcula o y definitivo tirando a média das duas inclinações
        y_prox = y_atual + (h / 2.0) * (f_xy1 + f_xy2)
        
        arquivo_saida.write(f"Iteracao {i}:\n")
        arquivo_saida.write(f"  k1 (Atual) = {f_xy1:.4f} | k2 (Predito em {x_prox:.4f}) = {f_xy2:.4f}\n")
        arquivo_saida.write(f"  y_prox = {y_prox:.4f}\n")
        
        x_atual, y_atual = x_prox, y_prox
        pontos.append((x_atual, y_atual))
        
    formatar_e_gravar_resultado(arquivo_saida, pontos)
    return pontos

def metodo_euler_modificado(funcao_str, x0, y0, h, n, arquivo_saida):
    """
    Resolve uma EDO utilizando o Método de Euler Modificado (também chamado de Ponto Médio).
    Ele dá meio passo para encontrar a inclinação central e a utiliza para o passo inteiro.
    """
    gravar_cabecalho_relatorio(arquivo_saida, "Euler Modificado (Ponto Medio)", funcao_str, x0, y0, h, n)
    
    x_atual, y_atual = x0, y0
    pontos = [(x_atual, y_atual)]
    arquivo_saida.write(f"Iteracao 0: x = {x_atual:.4f}, y = {y_atual:.4f}\n")
    
    for i in range(1, n + 1):
        # k1: Avalia a inclinação exatamente no início do intervalo
        k1 = avaliar_funcao_edo(funcao_str, x_atual, y_atual)
        
        # Encontra as coordenadas do "ponto médio" dando apenas meio passo (h/2)
        x_medio = x_atual + (h / 2.0)
        y_medio = y_atual + (h / 2.0) * k1
        
        # k2: Avalia a inclinação na metade do caminho (no ponto médio)
        k2 = avaliar_funcao_edo(funcao_str, x_medio, y_medio)
        
        # Passo definitivo: avança o 'h' inteiro, mas guiado pela inclinação do meio (k2)
        x_prox = x_atual + h
        y_prox = y_atual + h * k2
        
        arquivo_saida.write(f"Iteracao {i}:\n")
        arquivo_saida.write(f"  k1 (Inicio) = {k1:.4f} | k2 (Ponto Medio: x={x_medio:.4f}, y={y_medio:.4f}) = {k2:.4f}\n")
        arquivo_saida.write(f"  y_prox = {y_atual:.4f} + {h} * {k2:.4f} = {y_prox:.4f}\n")
        
        x_atual, y_atual = x_prox, y_prox
        pontos.append((x_atual, y_atual))
        
    formatar_e_gravar_resultado(arquivo_saida, pontos)
    return pontos

def metodo_ralston(funcao_str, x0, y0, h, n, arquivo_saida):
    """
    Resolve uma EDO utilizando o Método de Ralston.
    É uma variação que avalia a segunda inclinação a 3/4 do caminho, usando uma média ponderada para minimizar o erro.
    """
    gravar_cabecalho_relatorio(arquivo_saida, "Ralston", funcao_str, x0, y0, h, n)
    
    x_atual, y_atual = x0, y0
    pontos = [(x_atual, y_atual)]
    arquivo_saida.write(f"Iteracao 0: x = {x_atual:.4f}, y = {y_atual:.4f}\n")
    
    for i in range(1, n + 1):
        # k1: Avalia a inclinação inicial
        k1 = avaliar_funcao_edo(funcao_str, x_atual, y_atual)
        
        # Encontra as coordenadas parando em 3/4 (0.75) do tamanho do passo
        x_3_4 = x_atual + (0.75 * h)
        y_3_4 = y_atual + (0.75 * h) * k1
        
        # k2: Avalia a inclinação no ponto de 3/4
        k2 = avaliar_funcao_edo(funcao_str, x_3_4, y_3_4)
        
        # Fórmula de Ralston (o ponderamento): Dá o passo inteiro usando 1/3 do peso para a inclinação inicial 
        # e 2/3 do peso para a inclinação em 3/4 do caminho.
        x_prox = x_atual + h
        y_prox = y_atual + (h / 3.0) * (k1 + 2 * k2)
        
        arquivo_saida.write(f"Iteracao {i}:\n")
        arquivo_saida.write(f"  k1 = {k1:.4f} | k2 (em 3/4 do caminho) = {k2:.4f}\n")
        arquivo_saida.write(f"  y_prox = {y_atual:.4f} + ({h}/3) * ({k1:.4f} + 2*{k2:.4f}) = {y_prox:.4f}\n")
        
        x_atual, y_atual = x_prox, y_prox
        pontos.append((x_atual, y_atual))
        
    formatar_e_gravar_resultado(arquivo_saida, pontos)
    return pontos

# ==========================================
# CÓDIGO PRINCIPAL: LEITURA E MENU
# ==========================================

def main():
    caminho_entrada = 'entrada.txt'
    caminho_saida = 'saida.txt'
    
    print("====== RESOLUCAO DE EDOs ======")
    print("1 - Metodo de Euler")
    print("2 - Metodo de Euler Modificado (Ponto Medio)")
    print("3 - Metodo de Heun")
    print("4 - Metodo de Ralston")
    print("5 - Sair")
    opcao = input("Escolha o metodo desejado: ")

    if opcao == '5':
        print("Saindo...")
        return

    # Tenta ler o arquivo de entrada com as condições iniciais
    try:
        funcao_str, x0, y0, h, n = ler_arquivo_edo(caminho_entrada)
    except Exception as e:
        print(f"Erro ao ler '{caminho_entrada}'. Detalhe: {e}")
        return

    with open(caminho_saida, 'w') as file_out:
        if opcao == '1':
            pontos = metodo_euler(funcao_str, x0, y0, h, n, file_out)
        elif opcao == '2':
            pontos = metodo_euler_modificado(funcao_str, x0, y0, h, n, file_out)
        elif opcao == '3':
            pontos = metodo_heun(funcao_str, x0, y0, h, n, file_out)
        elif opcao == '4':
            pontos = metodo_ralston(funcao_str, x0, y0, h, n, file_out)
        else:
            print("Opcao invalida.")
            return
            
        if pontos:
            print(f"\nSucesso! Relatorio gravado em '{caminho_saida}'.")

if __name__ == "__main__":
    main()

