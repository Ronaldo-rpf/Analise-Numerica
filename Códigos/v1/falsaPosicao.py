import math

def funcao(x):
    return 0.25 * (x - 2) + 0.1 * math.sin(x)


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
        arquivo_saida.write("Erro: A função não muda de sinal no intervalo dado.\n")
        return None

    xr_velho = xl
    iteracao = 0
    ea = 100.0  

    arquivo_saida.write("(Iteração) | (xl)       | (xu)       | (xr)       | (ea %)\n")
    arquivo_saida.write("-" * 65 + "\n")

    while ea > es and iteracao < max_iter:
        
        # Passo 2: Calcula o novo xr usando a fórmula da Falsa Posição
        # xr = xu - ( f(xu)*(xl - xu) ) / ( f(xl) - f(xu) )
        numerador = f(xu) * (xl - xu)
        denominador = f(xl) - f(xu)
        
        # Prevenção contra divisão por zero caso a função seja plana
        if denominador == 0:
            arquivo_saida.write("Erro: Divisão por zero encontrada.\n")
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
    arquivo_saida.write(f"Raiz encontrada: {xr_novo:.6f} com erro de {ea:.4f}% após {iteracao} iterações.\n\n")
    return xr_novo




raiz = metodo_falsa_posicao(funcao, 1, 2)
