import math

# ==========================================
# FUNÇÕES DE APOIO 
# ==========================================

def avaliar_funcao(expressao, x_val):
    """
    Avalia uma função matemática em formato de string de forma segura, permitindo o uso de atalhos.
    
    Parâmetros:
    expressao : A string contendo a função matemática.
    x_val     : O valor numérico que substituirá a variável 'x' na expressão.
    """
    ambiente_seguro = {"x": x_val, "math": math}
    for func in ['sin', 'cos', 'tan', 'exp', 'log', 'sqrt', 'pi', 'e']:
        ambiente_seguro[func] = getattr(math, func)
    return eval(expressao, {"__builtins__": None}, ambiente_seguro)

def formatar_tupla(lista):
    """
    Formata uma lista de valores numéricos em uma string com parênteses e 6 casas decimais.
    
    Parâmetros:
    lista : Lista de números (floats) a serem formatados.
    """
    return "(" + ", ".join([f"{v:.6f}" for v in lista]) + ")"

def _trapezio_silencioso(funcao_str, a, b, n): # para o método de Richardson
    """
    Calcula a integral definida usando a Regra dos Trapézios de forma silenciosa, sem escrever nada na saida.txt.
    
    Parâmetros:
    funcao_str : A string contendo a função matemática.
    a          : Limite inferior de integração.
    b          : Limite superior de integração.
    n          : Número de subintervalos.
    """
    h = (b - a) / n # largura de cada trapézio 
    soma = avaliar_funcao(funcao_str, a) + avaliar_funcao(funcao_str, b)
    for i in range(1, n): # calcula a área de cada um
        soma += 2 * avaliar_funcao(funcao_str, a + i * h)
    return (h / 2) * soma

# ==========================================
# MÉTODOS DE INTEGRAÇÃO 
# ==========================================

def integracao_trapezio(funcao_str, a, b, n, arquivo_saida):
    """
    Calcula a integral definida de uma função usando a Regra dos Trapézios.
    
    Parâmetros:
    funcao_str    : A string contendo a função matemática.
    a             : Limite inferior do intervalo de integração.
    b             : Limite superior do intervalo de integração.
    n             : Número de subintervalos (n=1 para regra simples, n>1 para múltipla).
    arquivo_saida : Objeto do arquivo de texto para escrever o relatório passo a passo.
    """
    h = (b - a) / n # largura de cada trapézio 
    arquivo_saida.write(f"Metodo: Regra dos Trapezios | Subintervalos (n) = {n}\n")
    arquivo_saida.write(f"Passo (h) = {h:.6f}\n\n")

    arquivo_saida.write("--- FASE 1: AVALIACAO DOS PONTOS ---\n") # printa todos os pontos
    pontos_x = [a + i * h for i in range(n + 1)]
    valores_y = [avaliar_funcao(funcao_str, x) for x in pontos_x]
    
    arquivo_saida.write(f"Vetor de pontos x = {formatar_tupla(pontos_x)}\n")
    arquivo_saida.write(f"Vetor de f(x)     = {formatar_tupla(valores_y)}\n\n")

    arquivo_saida.write("--- FASE 2: APLICACAO DA FORMULA ---\n")
    if n == 1:
        arquivo_saida.write("Formula Simples: I = (h / 2) * (f(x0) + f(x1))\n")
        soma = valores_y[0] + valores_y[1]
    else:
        arquivo_saida.write("Formula Multipla: I = (h / 2) * (f(x0) + 2*soma(internos) + f(xn))\n") 
        soma_internos = sum(valores_y[1:-1])
        arquivo_saida.write(f"Soma dos termos internos = {soma_internos:.6f}\n")
        soma = valores_y[0] + 2 * soma_internos + valores_y[-1]

    integral = (h / 2) * soma 
    arquivo_saida.write(f"Calculo executado: ({h:.6f} / 2) * [{soma:.6f}]\n")
    return integral

def integracao_simpson_13(funcao_str, a, b, n, arquivo_saida): # desenha polinômios de 2º grau de 3 em 3 pontos, parábola e é muito mais preciso.
    """
    Calcula a integral definida de uma função usando a Regra de Simpson 1/3 múltipla.
    
    Parâmetros:
    funcao_str    : A string contendo a função matemática. 
    a             : Limite inferior do intervalo de integração.
    b             : Limite superior do intervalo de integração.
    n             : Número de subintervalos (obrigatoriamente PAR).
    arquivo_saida : Objeto do arquivo de texto para escrever o relatório passo a passo.
    """
    if n % 2 != 0:
        arquivo_saida.write(f"ERRO FATAL: Simpson 1/3 exige um numero PAR de subintervalos. n = {n} fornecido.\n")
        return None

    h = (b - a) / n # distância horizontal entre os pontos (passo), quanto menor mais precisa a integral.
    arquivo_saida.write(f"Metodo: Regra de Simpson 1/3 | Subintervalos (n) = {n}\n")
    arquivo_saida.write(f"Passo (h) = {h:.6f}\n\n")

    arquivo_saida.write("--- FASE 1: AVALIACAO DOS PONTOS ---\n") # printa os pontos
    pontos_x = [a + i * h for i in range(n + 1)]
    valores_y = [avaliar_funcao(funcao_str, x) for x in pontos_x]
    
    arquivo_saida.write(f"Vetor de pontos x = {formatar_tupla(pontos_x)}\n")
    arquivo_saida.write(f"Vetor de f(x)     = {formatar_tupla(valores_y)}\n\n")

    arquivo_saida.write("--- FASE 2: APLICACAO DA FORMULA ---\n")
    arquivo_saida.write("Formula: I = (h / 3) * (f(x0) + 4*soma(impares) + 2*soma(pares) + f(xn))\n") # multiplicação alternada dependendo da posição do ponto, ímpar ou par
    
    soma_impares = sum(valores_y[i] for i in range(1, n, 2))
    soma_pares = sum(valores_y[i] for i in range(2, n, 2))
    
    arquivo_saida.write(f"Soma indices impares (Peso 4) = {soma_impares:.6f}\n")
    arquivo_saida.write(f"Soma indices pares   (Peso 2) = {soma_pares:.6f}\n")
    
    soma_total = valores_y[0] + 4 * soma_impares + 2 * soma_pares + valores_y[-1]
    integral = (h / 3) * soma_total # divide pela constante geométrica das parábolas, por isso Simpson 1/3
    arquivo_saida.write(f"Calculo executado: ({h:.6f} / 3) * [{soma_total:.6f}]\n")
    return integral

def integracao_simpson_38(funcao_str, a, b, n, arquivo_saida): # usa polinômios cúbicos ligando 4 pontos por vez.
    """
    Calcula a integral definida de uma função usando a Regra de Simpson 3/8 múltipla.
    
    Parâmetros:
    funcao_str    : A string contendo a função matemática.
    a             : Limite inferior do intervalo de integração.
    b             : Limite superior do intervalo de integração.
    n             : Número de subintervalos (obrigatoriamente múltiplo de 3).
    arquivo_saida : Objeto do arquivo de texto para escrever o relatório passo a passo.
    """
    if n % 3 != 0:
        arquivo_saida.write(f"ERRO FATAL: Simpson 3/8 exige n multiplo de 3. n = {n} fornecido.\n")
        return None

    h = (b - a) / n # distância horizontal entre os pontos (passo), quanto menor mais precisa a integral.
    arquivo_saida.write(f"Metodo: Regra de Simpson 3/8 | Subintervalos (n) = {n}\n")
    arquivo_saida.write(f"Passo (h) = {h:.6f}\n\n")

    arquivo_saida.write("--- FASE 1: AVALIACAO DOS PONTOS ---\n") # printa os pontos
    pontos_x = [a + i * h for i in range(n + 1)]
    valores_y = [avaliar_funcao(funcao_str, x) for x in pontos_x]

    arquivo_saida.write(f"Vetor de pontos x = {formatar_tupla(pontos_x)}\n")
    arquivo_saida.write(f"Vetor de f(x)     = {formatar_tupla(valores_y)}\n\n")

    arquivo_saida.write("--- FASE 2: APLICACAO DA FORMULA ---\n")
    arquivo_saida.write("Formula: I = (3h / 8) * (f(x0) + 3*soma(nao_mult_3) + 2*soma(mult_3) + f(xn))\n") # multiplica por 3 os pontos nao múltiplos de 3, e por 2 os múltiplos de 3. 

    soma_nao_mult_3 = sum(valores_y[i] for i in range(1, n) if i % 3 != 0)
    soma_mult_3 = sum(valores_y[i] for i in range(1, n) if i % 3 == 0)

    arquivo_saida.write(f"Soma indices nao multiplos de 3 (Peso 3) = {soma_nao_mult_3:.6f}\n")
    arquivo_saida.write(f"Soma indices multiplos de 3     (Peso 2) = {soma_mult_3:.6f}\n")

    soma_total = valores_y[0] + 3 * soma_nao_mult_3 + 2 * soma_mult_3 + valores_y[-1]
    integral = (3 * h / 8) * soma_total # multiplica pela constante geométrica, por isso o nome 3/8.
    arquivo_saida.write(f"Calculo executado: (3 * {h:.6f} / 8) * [{soma_total:.6f}]\n")
    return integral

# ==========================================
# MÉTODOS AVANÇADOS DE INTEGRAÇÃO
# ==========================================

def extrapolacao_richardson(funcao_str, a, b, n1, arquivo_saida): # Subtrai as malhas para ver o padrão de erro e corrige o mesmo.
    """
    Melhora a precisão da integral usando a Extrapolação de Richardson sobre a Regra dos Trapézios.
    
    Parâmetros:
    funcao_str    : A string contendo a função matemática.
    a             : Limite inferior de integração.
    b             : Limite superior de integração.
    n1            : Número inicial de subintervalos (que será duplicado na extrapolação).
    arquivo_saida : Objeto do arquivo de texto para escrever o relatório.
    """
    n2 = n1 * 2
    arquivo_saida.write(f"Metodo: Extrapolacao de Richardson\n")
    arquivo_saida.write(f"Estrategia: Combinar duas malhas de Trapezio (n1={n1} e n2={n2})\n\n")

    arquivo_saida.write("--- FASE 1: OBTENCAO DOS CALCULOS BASE ---\n")
    I1 = _trapezio_silencioso(funcao_str, a, b, n1) # calcula a regra dos trapézios duas vezes - malha menos precisa
    I2 = _trapezio_silencioso(funcao_str, a, b, n2) # malha mais precisa
    
    arquivo_saida.write(f"I(h1) [Integral obtida com n={n1}] = {I1:.6f}\n")
    arquivo_saida.write(f"I(h2) [Integral obtida com n={n2}] = {I2:.6f}\n")
    
    arquivo_saida.write("\n--- FASE 2: EXTRAPOLACAO ALGEBRICA ---\n")
    arquivo_saida.write("Formula: R = I(h2) + [I(h2) - I(h1)] / 3\n")
    
    termo_correcao = (I2 - I1) / 3 
    resultado = I2 + termo_correcao # assim o erro/imprecisão gerado pelos trapézios desaparece. 
    
    arquivo_saida.write(f"Termo de correcao estimado = {termo_correcao:.6f}\n")
    arquivo_saida.write(f"Calculo final: {I2:.6f} + ({I2:.6f} - {I1:.6f}) / 3\n")
    return resultado

def quadratura_gauss(funcao_str, a, b, pontos_n, arquivo_saida):
    """
    Calcula a integral definida usando a Quadratura de Gauss-Legendre para alta precisão.
    
    Parâmetros:
    funcao_str    : A string contendo a função matemática.
    a             : Limite inferior de integração.
    b             : Limite superior de integração.
    pontos_n      : Número de pontos de Gauss a serem usados (suporta 2, 3 ou 4).
    arquivo_saida : Objeto do arquivo de texto para escrever o relatório passo a passo.
    """
    tabela_gauss = { # raízes dos Polinômios de Legendre e seus respectivos pesos.
        2: {'t': [-0.5773502692, 0.5773502692], 
            'w': [1.0, 1.0]},
        3: {'t': [-0.7745966692, 0.0, 0.7745966692], 
            'w': [0.5555555556, 0.8888888889, 0.5555555556]},
        4: {'t': [-0.8611363116, -0.3399810436, 0.3399810436, 0.8611363116], 
            'w': [0.3478548451, 0.6521451549, 0.6521451549, 0.3478548451]}
    } # para não perder tempo calculando esses valores.

    if pontos_n not in tabela_gauss: # só permite 2, 3 ou 4
        arquivo_saida.write(f"ERRO FATAL: Quadratura implementada para n=2, 3 ou 4. Recebido n={pontos_n}.\n")
        return None

    arquivo_saida.write(f"Metodo: Quadratura de Gauss-Legendre | Pontos (n) = {pontos_n}\n\n")
    
    arquivo_saida.write("--- FASE 1: MUDANCA DE VARIAVEL (Mapeamento para [-1, 1]) ---\n") # para corverter qualquer intervalo [a,b] em [-1,1], porque os valores da tabela só funcionam nesse intervalo.
    fator_dx = (b - a) / 2 # metade da largura do intervalo
    termo_soma = (b + a) / 2 # ponto médio
    
    arquivo_saida.write(f"Mapeamento: x(t) = {fator_dx}*t + {termo_soma}\n")
    arquivo_saida.write(f"Diferencial: dx = {fator_dx} dt\n\n")

    arquivo_saida.write("--- FASE 2: AVALIACAO NOS PONTOS DE LEGENDRE ---\n")
    raizes = tabela_gauss[pontos_n]['t'] # pega da tabela
    pesos = tabela_gauss[pontos_n]['w'] # pega da tabela
    soma_ponderada = 0.0
    
    for i in range(pontos_n):
        t_i = raizes[i]
        w_i = pesos[i]
        x_i = fator_dx * t_i + termo_soma # está no intervalo [-1,1], ele descobre qual é a coordenada equivalente dentro do intervalo do usuário. 
        f_xi = avaliar_funcao(funcao_str, x_i)
        
        parcela = w_i * f_xi # calcula a altura com o peso específico.
        soma_ponderada += parcela
        
        arquivo_saida.write(f"Ponto {i+1}: t = {t_i:11.8f} | w = {w_i:11.8f} -> x real = {x_i:.6f} -> w*f(x) = {parcela:.6f}\n")

    arquivo_saida.write("\n--- FASE 3: CALCULO DO PRODUTO ESCALAR ---\n")
    integral = fator_dx * soma_ponderada # Volta para a proporção original, antes de converter tudo para [-1,1]. 
    arquivo_saida.write(f"Calculo final: {fator_dx} * {soma_ponderada:.6f}\n")
    return integral

# ==========================================
# CÓDIGO PRINCIPAL: LEITURA E MENU
# ==========================================

def ler_arquivo_entradas(caminho):
    """
    Lê um arquivo de texto contendo os parâmetros para integração numérica.
    
    Parâmetros:
    caminho : Caminho (string) para o arquivo de texto.
    
    Retorno:
    Lista de tuplas empacotadas no formato (funcao_str, limite_a, limite_b, parametro_n).
    """
    dados = []
    with open(caminho, 'r') as file_in:
        for linha in file_in:
            if linha.strip() and ';' in linha:
                partes = linha.split(';')
                func_str = partes[0].strip()
                a_str, b_str = partes[1].split(',')
                param_n = int(partes[2].strip())
                dados.append((func_str, float(a_str.strip()), float(b_str.strip()), param_n))
    return dados

def main():
    caminho_entrada = 'entrada.txt'
    caminho_saida = 'saida.txt'
    
    print("====== INTEGRACAO NUMERICA ======")
    print("1 - Regra dos Trapezios")
    print("2 - Regra de Simpson 1/3 (numero de subintervalos nao deve ser par)")
    print("3 - Regra de Simpson 3/8 (numero de subintervalos nao deve ser multiplo de 3)")
    print("4 - Extrapolacao de Richardson")
    print("5 - Quadratura de Gauss (numero de subintervalos deve ser 2, 3 ou 4)")
    print("6 - Sair")
    opcao = input("Escolha o metodo para processar o arquivo: ")

    if opcao == '6':
        print("Saindo...")
        return

    if opcao not in ['1', '2', '3', '4', '5']:
        print("Opcao invalida!")
        return

    try:
        dados = ler_arquivo_entradas(caminho_entrada)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_entrada}' nao foi encontrado.")
        return
    except Exception as e:
        print(f"Erro na triagem do arquivo de entrada: {e}")
        return

    with open(caminho_saida, 'w') as file_out:
        file_out.write("====== RELATORIO DE PROCESSAMENTO ======\n\n")
        
        for idx, (funcao, a, b, param) in enumerate(dados):
            file_out.write("==================================================\n")
            file_out.write(f"EQUACAO ANALISADA {idx + 1}: f(x) = {funcao}\n")
            file_out.write(f"Intervalo de integracao: [{a}, {b}]\n")
            file_out.write("==================================================\n\n")

            if opcao == '1':
                resultado = integracao_trapezio(funcao, a, b, param, file_out)
            elif opcao == '2':
                resultado = integracao_simpson_13(funcao, a, b, param, file_out)
            elif opcao == '3':
                resultado = integracao_simpson_38(funcao, a, b, param, file_out)
            elif opcao == '4':
                resultado = extrapolacao_richardson(funcao, a, b, param, file_out)
            elif opcao == '5':
                resultado = quadratura_gauss(funcao, a, b, param, file_out)

            if resultado is not None:
                file_out.write("\n" + "-" * 50 + "\n")
                file_out.write(f"VALOR DA INTEGRAL ENCONTRADO: I = {resultado:.6f}\n")
                file_out.write("-" * 50 + "\n\n")
            else:
                file_out.write("\n[ALERTA DE SISTEMA] O metodo falhou devido aos erros listados acima.\n\n")

    print(f"\nSucesso! Todas as equacoes foram resolvidas e documentadas em '{caminho_saida}'.")

if __name__ == "__main__":
    main()
    