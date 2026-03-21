import math

def funcao(x):
    return 0.25 * (x - 2) + 0.1 * math.sin(x)

def metodo_bisseccao(f, xl, xu, es, arquivo_saida, max_iter=100):
    """
    Encontra a raiz de uma função usando o Método da Bissecção.
    
    Parâmetros:
    f        : A função matemática (definida em Python).
    xl       : Limite inferior do intervalo.
    xu       : Limite superior do intervalo.
    es       : Critério de parada / tolerância de erro em % (padrão é 0.5%) - nível de precisão exigido.
    max_iter : Número máximo de iterações por segurança.
    """
    
    # Passo 1: Verifica se a raiz realmente está no intervalo, se ela passa no eixo das abscissas
    if f(xl) * f(xu) >= 0:
        arquivo_saida.write("Erro: A funcao nao muda de sinal no intervalo dado.\n")
        return None

    xr_velho = xl  # Inicializa a variável para poder calcular o erro na primeira passada
    iteracao = 0
    ea = 100.0     # Define um erro inicial alto para garantir que entre no loop

    arquivo_saida.write("(Iteracao) | (xl)       | (xu)       | (xr)       | (ea %)\n")
    arquivo_saida.write("-" * 65 + "\n")

    # O loop continua enquanto o erro aproximado for maior que a tolerância (es)
    while ea > es and iteracao < max_iter:
        
        # Passo 2: Calcula o ponto médio
        xr_novo = (xl + xu) / 2
        iteracao += 1

        # Calcula o erro relativo percentual aproximado (ea) - o quanto o resultado está parando de mudar e chegando mais perto da raiz
        if xr_novo != 0: # Se for 0 achou a raiz
            ea = abs((xr_novo - xr_velho) / xr_novo) * 100

        # Imprime o acompanhamento da iteração atual
        arquivo_saida.write(f"( {iteracao:02d} )      | ({xl:.6f}) | ({xu:.6f}) | ({xr_novo:.6f}) | ({ea:.4f}%)\n")

        # Passo 3: Define qual será o novo intervalo
        aux = f(xl) * f(xr_novo)

        if aux < 0:
            xu = xr_novo       # A raiz está na metade inferior
        elif aux > 0:
            xl = xr_novo       # A raiz está na metade superior
        else:
            ea = 0             # A raiz exata foi encontrada 

        # Atualiza a variável para o cálculo do erro na próxima iteração
        xr_velho = xr_novo

    arquivo_saida.write("-" * 65 + "\n")
    arquivo_saida.write(f"Raiz encontrada: {xr_novo:.6f} com erro de {ea:.4f}% apos {iteracao} iteracoes.\n\n")
    return xr_novo




raiz = metodo_bisseccao(funcao, 1, 2)
