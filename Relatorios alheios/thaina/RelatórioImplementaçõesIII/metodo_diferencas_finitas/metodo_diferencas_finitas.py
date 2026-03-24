import os
import numpy as np
import math
import matplotlib.pyplot as plt 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def carregar_dados():
    """
    Carrega a função f(x, y), condições de contorno (x_ini, x_fim, y_ini, y_fim) 
    e o número de divisões (num_div) do arquivo 'entrada.txt'.
    """
    caminho_entrada = os.path.join(BASE_DIR, "entrada.txt")

    try:
        with open(caminho_entrada, "r") as arquivo:
            linhas = [l.strip() for l in arquivo.readlines()]

        expressao_f = linhas[0]
        x_ini = float(linhas[1])
        x_fim = float(linhas[2])
        y_ini = float(linhas[3])
        y_fim = float(linhas[4])
        num_div = int(linhas[5])
        
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_entrada}' não foi encontrado.")
        return None, None, None, None, None, None
    except IndexError:
        print("Erro: O arquivo 'entrada.txt' não contém as 6 linhas de dados esperadas.")
        return None, None, None, None, None, None
    except ValueError as e:
        print(f"Erro ao converter dados numéricos em 'entrada.txt': {e}")
        return None, None, None, None, None, None

    def funcao(x, y):
        """Função que representa a EDO de segunda ordem: y'' = f(x, y)"""
        contexto = {
            "x": x,
            "y": y,
            "math": math,
            "e": math.e,
            "exp": math.exp,
            "sin": math.sin,
            "cos": math.cos
        }
        return eval(expressao_f, contexto)

    return funcao, x_ini, x_fim, y_ini, y_fim, num_div


def escrever_resultado(xs, ys, metodo):
    """
    Grava os resultados calculados (pares x, y) no arquivo 'saida.txt'.
    """
    caminho_saida = os.path.join(BASE_DIR, "saida.txt")

    with open(caminho_saida, "w") as arq:

        for x_val, y_val in zip(xs, ys):
            arq.write(f"x = {x_val:.6f}, y = {y_val:.6f}\n")


def plotar_solucao(lista_x, lista_y, nome_metodo):
    """
    Gera um gráfico da solução (y em função de x) e salva como arquivo PNG.
    Retorna o nome do arquivo gerado.
    """
    plt.figure(figsize=(10, 6))
    
    plt.plot(lista_x, lista_y, marker='o', linestyle='-', color='teal', 
             label=f'Solução - {nome_metodo}')
    
    plt.plot([lista_x[0], lista_x[-1]], [lista_y[0], lista_y[-1]], 
             'ro', markersize=8, label='Condições de Contorno')
   
    plt.title(f'Solução de PVI pelo Método de {nome_metodo}', fontsize=14)
    plt.xlabel('Variável Independente (x)', fontsize=12)
    plt.ylabel('Variável Dependente (y)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc='best')
   
    nome_limpo = nome_metodo.replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '')
    nome_arquivo = f"solucao_{nome_limpo}.png"
    caminho_grafico = os.path.join(BASE_DIR, nome_arquivo)
   
    plt.savefig(caminho_grafico)
   
    plt.close() 
    
    return nome_arquivo


def metodo_dif_finitas(f, x0, xf, y0, yf, n):
    """
    Implementa o Método das Diferenças Finitas para resolver um Problema 
    de Valor de Contorno (PVC) da forma y'' = f(x, y).
    """
    h = (xf - x0) / n
    xs = np.linspace(x0, xf, n + 1)

    M = np.zeros((n - 1, n - 1))
    vet_b = np.zeros(n - 1)

    for k in range(n - 1):
        xk = xs[k + 1]
        yk_chute = y0 + (k + 1) * (yf - y0) / n  

        M[k, k] = -2
        if k > 0:
            M[k, k - 1] = 1 
        if k < n - 2:
            M[k, k + 1] = 1 

        vet_b[k] = (h ** 2) * f(xk, yk_chute) 

 
    vet_b[0] -= y0  
    vet_b[-1] -= yf  
  
    y_int = np.linalg.solve(M, vet_b)
    
    ys = [y0] + list(y_int) + [yf]

    return xs, ys


def executar():
    """Função principal de execução."""
    f, a, b, ya, yb, n = carregar_dados()
    
    if f is None:
        return

    print("Iniciando Método das Diferenças Finitas...")
  
    xs, ys = metodo_dif_finitas(f, a, b, ya, yb, n)
    nome = "Diferenças Finitas"
    
    escrever_resultado(xs, ys, nome)
    print(f"Arquivo 'saida.txt' gerado com sucesso para o método {nome}.")
    
    nome_arquivo_grafico = plotar_solucao(xs, ys, nome)
    print(f"Gráfico da solução salvo em '{nome_arquivo_grafico}'.")


if __name__ == "__main__":
    executar()