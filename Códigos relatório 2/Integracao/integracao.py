import math

# ==========================================
# FUNÇÕES MATEMÁTICAS E AMBIENTE SEGURO
# ==========================================

def avaliar_funcao(expressao, x_val):
    """Avalia uma função matemática em formato de string de forma segura."""
    ambiente_seguro = {"x": x_val, "math": math}
    for func in ['sin', 'cos', 'tan', 'exp', 'log', 'sqrt', 'pi', 'e']:
        ambiente_seguro[func] = getattr(math, func)
    return eval(expressao, {"__builtins__": None}, ambiente_seguro)

def formatar_tupla(lista):
    """Formata uma lista de pontos numéricos com parênteses (estilo Ronaldo)."""
    return "(" + ", ".join([f"{v:.6f}" for v in lista]) + ")"

# Função interna para calcular a regra do trapézio composto sem gerar logs.
# Essencial para alimentar o método de Richardson sem poluir o arquivo de saída.
def _trapezio_silencioso(funcao_str, a, b, n):
    h = (b - a) / n
    soma = avaliar_funcao(funcao_str, a) + avaliar_funcao(funcao_str, b)
    for i in range(1, n):
        soma += 2 * avaliar_funcao(funcao_str, a + i * h)
    return (h / 2) * soma

# ==========================================
# MÉTODOS DE INTEGRAÇÃO (NEWTON-COTES)
# ==========================================

def integracao_trapezio(funcao_str, a, b, n, arquivo_saida):
    """Aplica a Regra dos Trapézios (Simples se n=1, Múltipla se n>1)."""
    h = (b - a) / n
    arquivo_saida.write(f"Metodo: Regra dos Trapezios | Subintervalos (n) = {n}\n")
    arquivo_saida.write(f"Passo (h) = {h:.6f}\n\n")

    arquivo_saida.write("--- FASE 1: AVALIACAO DOS PONTOS ---\n")
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

def integracao_simpson_13(funcao_str, a, b, n, arquivo_saida):
    """Aplica a Regra de Simpson 1/3 Múltipla (Exige n par)."""
    if n % 2 != 0:
        arquivo_saida.write(f"ERRO FATAL: Simpson 1/3 exige um numero PAR de subintervalos. n = {n} fornecido.\n")
        return None

    h = (b - a) / n
    arquivo_saida.write(f"Metodo: Regra de Simpson 1/3 | Subintervalos (n) = {n}\n")
    arquivo_saida.write(f"Passo (h) = {h:.6f}\n\n")

    arquivo_saida.write("--- FASE 1: AVALIACAO DOS PONTOS ---\n")
    pontos_x = [a + i * h for i in range(n + 1)]
    valores_y = [avaliar_funcao(funcao_str, x) for x in pontos_x]
    
    arquivo_saida.write(f"Vetor de pontos x = {formatar_tupla(pontos_x)}\n")
    arquivo_saida.write(f"Vetor de f(x)     = {formatar_tupla(valores_y)}\n\n")

    arquivo_saida.write("--- FASE 2: APLICACAO DA FORMULA ---\n")
    arquivo_saida.write("Formula: I = (h / 3) * (f(x0) + 4*soma(impares) + 2*soma(pares) + f(xn))\n")
    
    soma_impares = sum(valores_y[i] for i in range(1, n, 2))
    soma_pares = sum(valores_y[i] for i in range(2, n, 2))
    
    arquivo_saida.write(f"Soma indices impares (Peso 4) = {soma_impares:.6f}\n")
    arquivo_saida.write(f"Soma indices pares   (Peso 2) = {soma_pares:.6f}\n")
    
    soma_total = valores_y[0] + 4 * soma_impares + 2 * soma_pares + valores_y[-1]
    integral = (h / 3) * soma_total
    arquivo_saida.write(f"Calculo executado: ({h:.6f} / 3) * [{soma_total:.6f}]\n")
    return integral

def integracao_simpson_38(funcao_str, a, b, n, arquivo_saida):
    """Aplica a Regra de Simpson 3/8 Múltipla (Exige n múltiplo de 3)."""
    if n % 3 != 0:
        arquivo_saida.write(f"ERRO FATAL: Simpson 3/8 exige n multiplo de 3. n = {n} fornecido.\n")
        return None

    h = (b - a) / n
    arquivo_saida.write(f"Metodo: Regra de Simpson 3/8 | Subintervalos (n) = {n}\n")
    arquivo_saida.write(f"Passo (h) = {h:.6f}\n\n")

    arquivo_saida.write("--- FASE 1: AVALIACAO DOS PONTOS ---\n")
    pontos_x = [a + i * h for i in range(n + 1)]
    valores_y = [avaliar_funcao(funcao_str, x) for x in pontos_x]

    arquivo_saida.write(f"Vetor de pontos x = {formatar_tupla(pontos_x)}\n")
    arquivo_saida.write(f"Vetor de f(x)     = {formatar_tupla(valores_y)}\n\n")

    arquivo_saida.write("--- FASE 2: APLICACAO DA FORMULA ---\n")
    arquivo_saida.write("Formula: I = (3h / 8) * (f(x0) + 3*soma(nao_mult_3) + 2*soma(mult_3) + f(xn))\n")

    soma_nao_mult_3 = sum(valores_y[i] for i in range(1, n) if i % 3 != 0)
    soma_mult_3 = sum(valores_y[i] for i in range(1, n) if i % 3 == 0)

    arquivo_saida.write(f"Soma indices nao multiplos de 3 (Peso 3) = {soma_nao_mult_3:.6f}\n")
    arquivo_saida.write(f"Soma indices multiplos de 3     (Peso 2) = {soma_mult_3:.6f}\n")

    soma_total = valores_y[0] + 3 * soma_nao_mult_3 + 2 * soma_mult_3 + valores_y[-1]
    integral = (3 * h / 8) * soma_total
    arquivo_saida.write(f"Calculo executado: (3 * {h:.6f} / 8) * [{soma_total:.6f}]\n")
    return integral

# ==========================================
# MÉTODOS AVANÇADOS DE INTEGRAÇÃO
# ==========================================

def extrapolacao_richardson(funcao_str, a, b, n1, arquivo_saida):
    """Aplica a Extrapolação de Richardson duplicando a malha do Trapézio."""
    n2 = n1 * 2
    arquivo_saida.write(f"Metodo: Extrapolacao de Richardson\n")
    arquivo_saida.write(f"Estrategia: Combinar duas malhas de Trapezio (n1={n1} e n2={n2})\n\n")

    arquivo_saida.write("--- FASE 1: OBTENCAO DOS CALCULOS BASE ---\n")
    I1 = _trapezio_silencioso(funcao_str, a, b, n1)
    I2 = _trapezio_silencioso(funcao_str, a, b, n2)
    
    arquivo_saida.write(f"I(h1) [Integral obtida com n={n1}] = {I1:.6f}\n")
    arquivo_saida.write(f"I(h2) [Integral obtida com n={n2}] = {I2:.6f}\n")
    
    arquivo_saida.write("\n--- FASE 2: EXTRAPOLACAO ALGEBRICA ---\n")
    arquivo_saida.write("Formula: R = I(h2) + [I(h2) - I(h1)] / 3\n")
    
    termo_correcao = (I2 - I1) / 3
    resultado = I2 + termo_correcao
    
    arquivo_saida.write(f"Termo de correcao estimado = {termo_correcao:.6f}\n")
    arquivo_saida.write(f"Calculo final: {I2:.6f} + ({I2:.6f} - {I1:.6f}) / 3\n")
    return resultado

def quadratura_gauss(funcao_str, a, b, pontos_n, arquivo_saida):
    """Aplica a Quadratura de Gauss-Legendre (Suporta n = 2, 3 ou 4)."""
    tabela_gauss = {
        2: {'t': [-0.5773502692, 0.5773502692], 
            'w': [1.0, 1.0]},
        3: {'t': [-0.7745966692, 0.0, 0.7745966692], 
            'w': [0.5555555556, 0.8888888889, 0.5555555556]},
        4: {'t': [-0.8611363116, -0.3399810436, 0.3399810436, 0.8611363116], 
            'w': [0.3478548451, 0.6521451549, 0.6521451549, 0.3478548451]}
    }

    if pontos_n not in tabela_gauss:
        arquivo_saida.write(f"ERRO FATAL: Quadratura implementada para n=2, 3 ou 4. Recebido n={pontos_n}.\n")
        return None

    arquivo_saida.write(f"Metodo: Quadratura de Gauss-Legendre | Pontos (n) = {pontos_n}\n\n")
    
    arquivo_saida.write("--- FASE 1: MUDANCA DE VARIAVEL (Mapeamento para [-1, 1]) ---\n")
    fator_dx = (b - a) / 2
    termo_soma = (b + a) / 2
    
    arquivo_saida.write(f"Mapeamento: x(t) = {fator_dx}*t + {termo_soma}\n")
    arquivo_saida.write(f"Diferencial: dx = {fator_dx} dt\n\n")

    arquivo_saida.write("--- FASE 2: AVALIACAO NOS PONTOS DE LEGENDRE ---\n")
    raizes = tabela_gauss[pontos_n]['t']
    pesos = tabela_gauss[pontos_n]['w']
    soma_ponderada = 0.0
    
    for i in range(pontos_n):
        t_i = raizes[i]
        w_i = pesos[i]
        x_i = fator_dx * t_i + termo_soma
        f_xi = avaliar_funcao(funcao_str, x_i)
        
        parcela = w_i * f_xi
        soma_ponderada += parcela
        
        arquivo_saida.write(f"Ponto {i+1}: t = {t_i:11.8f} | w = {w_i:11.8f} -> x real = {x_i:.6f} -> w*f(x) = {parcela:.6f}\n")

    arquivo_saida.write("\n--- FASE 3: CALCULO DO PRODUTO ESCALAR ---\n")
    integral = fator_dx * soma_ponderada
    arquivo_saida.write(f"Calculo final: {fator_dx} * {soma_ponderada:.6f}\n")
    return integral

# ==========================================
# CÓDIGO PRINCIPAL: GERENCIADOR E MENU
# ==========================================

def ler_arquivo_entradas(caminho):
    """Lê o arquivo estruturado no padrão unificado: funcao ; a,b ; parametro"""
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
    
    print("====== INTEGRACAO NUMERICA UNIFICADA ======")
    print("1 - Regra dos Trapezios")
    print("2 - Regra de Simpson 1/3 (n deve ser par)")
    print("3 - Regra de Simpson 3/8 (n deve ser mult de 3)")
    print("4 - Extrapolacao de Richardson")
    print("5 - Quadratura de Gauss (n deve ser 2, 3 ou 4)")
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
        file_out.write("====== RELATORIO DE PROCESSAMENTO EM LOTE ======\n\n")
        
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
    