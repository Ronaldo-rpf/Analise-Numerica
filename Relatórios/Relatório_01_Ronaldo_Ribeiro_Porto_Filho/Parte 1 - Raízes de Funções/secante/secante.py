import math

# Tem o risco de divergir se a reta ir para o infinito por conta da forma da funcao.
# Nao checa sinais.
# Falsa posicao verifica sempre os sinais, entao sempre converge mas e mais lento.

def metodo_secante(f, x_ant, x_atual, es, arquivo_saida, max_iter=100):
    """
    Encontra a raiz de uma função usando o Método da Secante.
    
    Parâmetros:
    f        : A função matemática original.
    x_ant    : Primeiro chute inicial (x_{i-1}).
    x_atual  : Segundo chute inicial (x_i).
    es       : Tolerância de erro relativo percentual (padrão é 0.5%).
    arquivo_saida: Objeto do arquivo de texto para escrever o relatório.
    """
    
    iteracao = 0
    ea = 100.0  

    arquivo_saida.write("(Iteracao) | (x_ant)    | (x_atual)  | (x_novo)   | (ea %)\n")
    arquivo_saida.write("-" * 65 + "\n")

    while ea > es and iteracao < max_iter:
        
        f_ant = f(x_ant)
        f_atual = f(x_atual)
        
        # Prevenção contra divisão por zero
        denominador = f_ant - f_atual
        if denominador == 0:
            arquivo_saida.write(f"Erro: O denominador zerou (f(x_ant) == f(x_atual)). A reta ficou paralela ao eixo X.\n")
            break
            
        # Fórmula da Secante: x_novo = x_atual - [ f(x_atual) * (x_ant - x_atual) ] / [ f(x_ant) - f(x_atual) ]
        numerador = f_atual * (x_ant - x_atual)
        x_novo = x_atual - (numerador / denominador)
        
        iteracao += 1

        # Calcula o erro relativo percentual aproximado (ea)
        if x_novo != 0:
            ea = abs((x_novo - x_atual) / x_novo) * 100

        arquivo_saida.write(f"( {iteracao:02d} )      | ({x_ant:.6f}) | ({x_atual:.6f}) | ({x_novo:.6f}) | ({ea:.6f}%)\n")

        # Atualiza os valores em "sequência estrita" (o atual vira antigo, o novo vira atual)
        x_ant = x_atual
        x_atual = x_novo

    arquivo_saida.write("-" * 65 + "\n")
    
    # Verificação de segurança 
    if abs(f(x_atual)) > 0.1:
        arquivo_saida.write("AVISO: O erro ficou pequeno, mas f(x) esta longe de zero. O metodo pode ter divergido!\n")

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
        
        func_str = linhas[0].strip()
        x0_input = float(linhas[1].strip())
        x1_input = float(linhas[2].strip())
        es_input = float(linhas[3].strip())
        
    funcao_matematica = lambda x: eval(func_str, {"math": math, "x": x})
    
    with open(caminho_saida, 'w') as file_out:
        
        file_out.write("====== RELATORIO DE ANALISE NUMERICA ======\n")
        file_out.write(f"Funcao analisada : f(x) = {func_str}\n")
        file_out.write(f"Chutes iniciais  : x0 = {x0_input}, x1 = {x1_input}\n")
        file_out.write(f"Tolerancia (ea)  : {es_input}%\n")
        file_out.write("===========================================\n\n")

        file_out.write("METODO DA SECANTE\n")
        metodo_secante(funcao_matematica, x0_input, x1_input, es_input, file_out)
        
    print(f"\nSucesso! Calculos da Secante salvos no arquivo '{caminho_saida}'.\n")

except FileNotFoundError:
    print(f"Erro: O arquivo '{caminho_entrada}' nao foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro durante a execucao: {e}")