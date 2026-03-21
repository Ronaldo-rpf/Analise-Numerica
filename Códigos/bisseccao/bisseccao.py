import math
import os

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

# ==========================================
# CÓDIGO PRINCIPAL: LEITURA E ESCRITA
# ==========================================

# Define os caminhos dos arquivos (na mesma pasta do script)
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

        file_out.write("METODO DA BISSECCAO \n")
        metodo_bisseccao(funcao_matematica, xl_input, xu_input, es_input, file_out)

    print(f"\nSucesso! Os calculos foram realizados e salvos no arquivo '{caminho_saida}'.\n")

except FileNotFoundError:
    print(f"Erro: O arquivo '{caminho_entrada}' não foi encontrado na mesma pasta.")
except Exception as e:
    print(f"Ocorreu um erro durante a execução: {e}")