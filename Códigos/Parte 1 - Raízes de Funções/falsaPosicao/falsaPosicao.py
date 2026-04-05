import math

def metodo_falsa_posicao(f, xl, xu, es, arquivo_saida, max_iter=100):
    """
    Encontra a raiz de uma função usando o Método da Falsa Posição.
    
    Parâmetros:
    f        : A função matemática a ser avaliada.
    xl       : Limite inferior do intervalo inicial.
    xu       : Limite superior do intervalo inicial.
    es       : Tolerância de erro relativo percentual (padrão é 0.5%).
    max_iter : Número máximo de iterações permitidas.
    """
    
    # Passo 1: Verifica se a raiz realmente está no intervalo
    if f(xl) * f(xu) >= 0:
        arquivo_saida.write("Erro: A funcaoo nao muda de sinal no intervalo dado.\n")
        return None

    xr_velho = xl
    iteracao = 0
    ea = 100.0  

    arquivo_saida.write("(Iteracao) | (xl)       | (xu)       | (xr)       | (ea %)\n")
    arquivo_saida.write("-" * 65 + "\n")

    while ea > es and iteracao < max_iter:
        
        # Passo 2: Calcula o novo xr usando a fórmula da Falsa Posição
        # xr = xu - ( f(xu)*(xl - xu) ) / ( f(xl) - f(xu) )
        numerador = f(xu) * (xl - xu)
        denominador = f(xl) - f(xu)
        
        # Prevenção contra divisão por zero caso a função seja plana
        if denominador == 0:
            arquivo_saida.write("Erro: Divisao por zero encontrada.\n")
            break
            
        xr_novo = xu - (numerador / denominador)
        iteracao += 1

        # Passo 3: Calcula o erro relativo percentual aproximado (ea)
        if xr_novo != 0 and iteracao > 1:
            ea = abs((xr_novo - xr_velho) / xr_novo) * 100

        arquivo_saida.write(f"( {iteracao:02d} )      | ({xl:.6f}) | ({xu:.6f}) | ({xr_novo:.6f}) | ({ea:.4f}%)\n")

        # Passo 4: Define de qual lado a raiz está para a próxima rodada
        aux = f(xl) * f(xr_novo) # 

        if aux < 0:            # Se deu negativo f(xl) e f(xr_novo) tem sinais opostos, a linha cruzou o eixo no meio do caminho
            xu = xr_novo       # Raiz no subintervalo inferior
        elif aux > 0:          # A linha não cruzou o eixo nesse intervalo
            xl = xr_novo       # Raiz no subintervalo superior
        else:
            ea = 0             # Raiz exata encontrada

        xr_velho = xr_novo     # Para o cálculo de erro na próxima iteração, calcular o quão pouco o resultado mudou

    arquivo_saida.write("-" * 65 + "\n")
    arquivo_saida.write(f"Raiz encontrada: {xr_novo:.6f} com erro de {ea:.4f}% apos {iteracao} iteracoes.\n\n")
    return xr_novo

# ==========================================
# CÓDIGO PRINCIPAL: LEITURA E ESCRITA
# ==========================================

caminho_entrada = 'entrada.txt'
caminho_saida = 'saida.txt'

try:
    # Lendo os dados do arquivo de entrada
    with open(caminho_entrada, 'r') as file_in: # Fecha o arquivo automaticamente, com um apelido de file_in
        linhas = file_in.readlines() # Lê todas as linhas e guarda cada uma em uma posição do vetor
        
        # Extraindo os valores de cada linha
        func_str = linhas[0].strip() # Limpa todos os \n no caminho para conversão 
        xl_input = float(linhas[1].strip())
        xu_input = float(linhas[2].strip())
        es_input = float(linhas[3].strip())
        
    # Transforma o texto em uma função Python executável usando lambda e eval
    funcao_matematica = lambda x: eval(func_str, {"math": math, "x": x}) # Lê o txt e executa como código de python (mini função)
    
    # Criando o arquivo de saída e executando os métodos
    with open(caminho_saida, 'w') as file_out:
        
        file_out.write("====== RELATORIO ======\n")
        file_out.write(f"Funcao analisada: f(x) = {func_str}\n")
        file_out.write(f"Intervalo inicial: [{xl_input}, {xu_input}]\n")
        file_out.write(f"Tolerancia exigida: {es_input}%\n")
        file_out.write("=======================\n\n")

        file_out.write("METODO DA FALSA POSICAO \n")
        metodo_falsa_posicao(funcao_matematica, xl_input, xu_input, es_input, file_out)
        
    print(f"\nSucesso! Os calculos foram realizados e salvos no arquivo '{caminho_saida}'.\n")

except FileNotFoundError:
    print(f"Erro: O arquivo '{caminho_entrada}' não foi encontrado na mesma pasta.")
except Exception as e:
    print(f"Ocorreu um erro durante a execução: {e}")