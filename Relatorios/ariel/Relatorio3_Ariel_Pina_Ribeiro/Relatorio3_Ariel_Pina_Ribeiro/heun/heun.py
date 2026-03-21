"""
Implementação do método de Heun para resolução de equações diferenciais
"""

import math
import sys

def carregar_configuracao(caminho_entrada="entrada.txt"):
    """
    Carrega os parâmetros de configuração do arquivo de entrada.
    
    Formato esperado do arquivo:
    Linha 1: Expressão da EDO f(x, y)
    Linha 2: Valor inicial de x
    Linha 3: Valor inicial de y
    Linha 4: Tamanho do passo h
    Linha 5: Número de iterações n
    
    Retorna: função f(x, y), x0, y0, h, n
    """
    try:
        with open(caminho_entrada, 'r') as arquivo:
            dados = [linha.rstrip('\n') for linha in arquivo]
        
        if len(dados) < 5:
            raise ValueError("Arquivo de entrada incompleto")
        
        # Extrai os parâmetros
        expressao_f = dados[0]
        valor_x_inicial = float(dados[1])
        valor_y_inicial = float(dados[2])
        passo_h = float(dados[3])
        iteracoes_n = int(dados[4])
        
        # Cria a função f(x, y) a partir da expressão
        def funcao_edo(x_valor, y_valor):
            ambiente = {
                'x': x_valor,
                'y': y_valor,
                'math': math,
                'e': math.e,
                'exp': math.exp,
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'log': math.log,
                'log10': math.log10,
                'sqrt': math.sqrt,
                'pi': math.pi
            }
            return eval(expressao_f, ambiente)
        
        return funcao_edo, valor_x_inicial, valor_y_inicial, passo_h, iteracoes_n
    
    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_entrada}' não encontrado.")
        sys.exit(1)
    except ValueError as e:
        print(f"Erro no formato do arquivo: {e}")
        sys.exit(1)

def metodo_heun(funcao, x_inicio, y_inicio, passo, iteracoes):
    """
    Implementação do método de Heun para resolução de EDOs.
    
    O método utiliza uma abordagem de previsão-correção com duas estimativas
    de inclinação para melhorar a precisão em relação ao método de Euler.
    
    Parâmetros:
    - funcao: função f(x, y) da EDO dy/dx = f(x, y)
    - x_inicio: valor inicial de x
    - y_inicio: valor inicial de y
    - passo: tamanho do passo de integração
    - iteracoes: número de iterações a executar
    
    Retorna: listas com os valores de x e y calculados
    """
    # Listas para armazenar os resultados
    valores_x = [x_inicio]
    valores_y = [y_inicio]
    
    # Variáveis atuais
    x_atual = x_inicio
    y_atual = y_inicio
    
    print(f"Iniciando método de Heun com {iteracoes} iterações...")
    
    for i in range(iteracoes):
        # Estágio 1: Cálculo da inclinação inicial (previsão)
        inclinacao_inicial = funcao(x_atual, y_atual)
        y_previsao = y_atual + passo * inclinacao_inicial
        x_proximo = x_atual + passo
        
        # Estágio 2: Cálculo da inclinação no ponto previsto (correção)
        inclinacao_corrigida = funcao(x_proximo, y_previsao)
        
        # Estágio 3: Atualização usando a média das inclinações
        inclinacao_media = (inclinacao_inicial + inclinacao_corrigida) / 2
        y_atualizado = y_atual + passo * inclinacao_media
        
        # Atualiza os valores para a próxima iteração
        x_atual = x_proximo
        y_atual = y_atualizado
        
        # Armazena os resultados
        valores_x.append(x_atual)
        valores_y.append(y_atual)
        
        # Exibe progresso a cada 50 iterações
        if (i + 1) % 50 == 0 or i == iteracoes - 1:
            print(f"  Iteração {i + 1}/{iteracoes}: x = {x_atual:.6f}, y = {y_atual:.6f}")
    
    print(f"Método de Heun concluído com sucesso!")
    return valores_x, valores_y

def exportar_resultados(valores_x, valores_y, caminho_saida="saida.txt"):
    """
    Exporta os resultados para um arquivo de saída.
    
    Formato do arquivo de saída:
    Linha 1: "Método: Heun"
    Linhas seguintes: "x = {x:.6f}, y = {y:.6f}"
    """
    try:
        with open(caminho_saida, 'w') as arquivo:
            # Cabeçalho com o método utilizado
            arquivo.write("Método: Heun\n")
            
            # Escreve cada par (x, y) formatado com 6 casas decimais
            for x, y in zip(valores_x, valores_y):
                linha = f"x = {x:.6f}, y = {y:.6f}\n"
                arquivo.write(linha)
        
        print(f"Resultados exportados para '{caminho_saida}'")
        print(f"Total de {len(valores_x)} pontos calculados")
        
    except IOError as e:
        print(f"Erro ao escrever no arquivo de saída: {e}")
        sys.exit(1)

def exibir_resumo(valores_x, valores_y):
    """
    Exibe um resumo dos resultados na tela.
    """
    print("\n" + "="*50)
    print("RESUMO DOS RESULTADOS")
    print("="*50)
    
    # Mostra os primeiros 3 pontos
    print("Primeiros pontos:")
    for i in range(min(3, len(valores_x))):
        print(f"  x = {valores_x[i]:.6f}, y = {valores_y[i]:.6f}")
    
    # Mostra os últimos 3 pontos
    if len(valores_x) > 3:
        print("\nÚltimos pontos:")
        for i in range(max(0, len(valores_x)-3), len(valores_x)):
            print(f"  x = {valores_x[i]:.6f}, y = {valores_y[i]:.6f}")
    
    # Informações gerais
    print(f"\nInformações:")
    print(f"  Intervalo de x: [{valores_x[0]:.2f}, {valores_x[-1]:.2f}]")
    print(f"  Variação em y: {valores_y[-1] - valores_y[0]:.6f}")
    print(f"  Número total de pontos: {len(valores_x)}")
    print("="*50)

def main():
    """
    Função principal que orquestra a execução do método de Heun.
    """
    print("="*60)
    print("IMPLEMENTAÇÃO DO MÉTODO DE HEUN")
    print("Para resolução de equações diferenciais ordinárias")
    print("="*60)
    
    # Carrega a configuração do arquivo de entrada
    print("\n[1/4] Carregando configuração...")
    funcao_edo, x0, y0, h, n = carregar_configuracao()
    
    print(f"   Expressão da EDO: dy/dx = {open('entrada.txt').readline().strip()}")
    print(f"   Condições iniciais: x0 = {x0}, y0 = {y0}")
    print(f"   Parâmetros: passo h = {h}, iterações n = {n}")
    
    # Executa o método de Heun
    print("\n[2/4] Executando o método de Heun...")
    resultados_x, resultados_y = metodo_heun(funcao_edo, x0, y0, h, n)
    
    # Exporta os resultados
    print("\n[3/4] Exportando resultados...")
    exportar_resultados(resultados_x, resultados_y)
    
    # Exibe resumo
    print("\n[4/4] Gerando resumo...")
    exibir_resumo(resultados_x, resultados_y)
    
    # Pergunta se o usuário deseja ver mais pontos
    try:
        resposta = input("\nDeseja visualizar mais pontos? (s/n): ").strip().lower()
        if resposta == 's':
            try:
                quantidade = int(input("Quantos pontos deseja ver? (ex: 10): "))
                print(f"\nPrimeiros {min(quantidade, len(resultados_x))} pontos:")
                for i in range(min(quantidade, len(resultados_x))):
                    print(f"  x = {resultados_x[i]:.6f}, y = {resultados_y[i]:.6f}")
            except ValueError:
                print("Entrada inválida. Exibindo os primeiros 5 pontos por padrão:")
                for i in range(min(5, len(resultados_x))):
                    print(f"  x = {resultados_x[i]:.6f}, y = {resultados_y[i]:.6f}")
    except KeyboardInterrupt:
        pass
    
    print("\nExecução concluída com sucesso!")
    print("="*60)

if __name__ == "__main__":
    main()
