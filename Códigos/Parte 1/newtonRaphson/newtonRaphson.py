import math

# Se o primeiro chute cair onde a tangente é 100% horizontal (pico ou vale) ela nunca cruzara o eixo x - divisao por zero - se a inclinacao for proxima de 0 e ruim tambem.
# A reta tangente pode ficar jogando o valor de um lado para o outro infinitamente.

def metodo_newton_raphson(f, df, x0, es, arquivo_saida, max_iter=100):
    """
    Encontra a raiz de uma função usando o Método de Newton-Raphson.
    
    Parâmetros:
    f        : A função matemática original.
    df       : A primeira derivada da função f'(x).
    x0       : Chute inicial.
    es       : Tolerância de erro relativo percentual (padrão é 0.5%).
    arquivo_saida: Objeto do arquivo de texto para escrever o relatório.
    """
    
    iteracao = 0
    ea = 100.0  
    x_atual = x0

    arquivo_saida.write("(Iteracao) | (x_atual)  | (f(x))     | (df(x))    | (ea %)\n")
    arquivo_saida.write("-" * 65 + "\n")

    while ea > es and iteracao < max_iter:
        
        fx = f(x_atual)
        dfx = df(x_atual)
        
        # Prevenção contra inclinação nula (divisão por zero)
        if dfx == 0:
            arquivo_saida.write(f"Erro Crítico: A derivada zerou em x = {x_atual}. O metodo falhou.\n")
            break
            
        # Fórmula de Newton-Raphson: x_novo = x_antigo - f(x)/f'(x)
        x_novo = x_atual - (fx / dfx)
        iteracao += 1

        # Calcula o erro relativo percentual aproximado (ea)
        if x_novo != 0:
            ea = abs((x_novo - x_atual) / x_novo) * 100

        arquivo_saida.write(f"( {iteracao:02d} )      | ({x_atual:.6f}) | ({fx:.6f}) | ({dfx:.6f}) | ({ea:.6f}%)\n")

        # Atualiza para o próximo loop
        x_atual = x_novo

    # Escreve a iteração final
    arquivo_saida.write(f"( {(iteracao+1):02d} )      | ({x_atual:.6f}) | ({f(x_atual):.6f}) | ({df(x_atual):.6f}) | ({ea:.6f}%)\n")
    arquivo_saida.write("-" * 65 + "\n")
    
    # Verificação final - verifica se a função f(x) realmente chegou perto de zero
    if abs(f(x_atual)) > 0.1:
        arquivo_saida.write("AVISO: O erro 'ea' ficou pequeno, mas f(x) ainda esta longe de zero. Possivel divergencia!\n")

    arquivo_saida.write(f"Raiz encontrada: {x_atual:.8f} com erro de {ea:.6f}% apos {iteracao} iteracoes.\n\n")
    return x_atual

# ==========================================
# CÓDIGO PRINCIPAL: LEITURA E ESCRITA
# ==========================================

caminho_entrada = 'entrada.txt'
caminho_saida = 'saida.txt'

try:
    with open(caminho_entrada, 'r') as file_in:
        linhas = file_in.readlines()
        
        # Extraindo os valores do novo formato do TXT
        func_str = linhas[0].strip()
        dfunc_str = linhas[1].strip() 
        x0_input = float(linhas[2].strip()) # Chute inicial 
        es_input = float(linhas[3].strip())
        
    # Transforma texto em funções Python
    funcao_f = lambda x: eval(func_str, {"math": math, "x": x})
    funcao_df = lambda x: eval(dfunc_str, {"math": math, "x": x})
    
    with open(caminho_saida, 'w') as file_out:
        
        file_out.write("====== RELATORIO DE ANALISE NUMERICA ======\n")
        file_out.write(f"Funcao original : f(x)  = {func_str}\n")
        file_out.write(f"Derivada        : f'(x) = {dfunc_str}\n")
        file_out.write(f"Chute inicial   : x0 = {x0_input}\n")
        file_out.write(f"Tolerancia (ea) : {es_input}%\n")
        file_out.write("===========================================\n\n")

        file_out.write("METODO DE NEWTON-RAPHSON\n")
        metodo_newton_raphson(funcao_f, funcao_df, x0_input, es_input, file_out)
        
    print(f"\nSucesso! Calculos do Newton-Raphson salvos em '{caminho_saida}'.\n")

except FileNotFoundError:
    print(f"Erro: O arquivo '{caminho_entrada}' nao foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro durante a execucao: {e}")