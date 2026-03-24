import os
import math
import matplotlib.pyplot as plt

def ler_dados():
    """
    Carrega a expressão da função f(x, y), condições iniciais (x_ini, y_ini),
    passo (h) e número de repetições (qtd) do arquivo 'entrada.txt'.
    Retorna a função g(x, y) e os parâmetros iniciais.
    """
    arquivo = os.path.join(os.path.dirname(__file__), "entrada.txt")

    try:
        with open(arquivo, "r") as arq:
            linhas = [linha.strip() for linha in arq.readlines()]
            expressao = linhas[0]
            x_ini = float(linhas[1])
            y_ini = float(linhas[2])
            passo = float(linhas[3])
            qtd = int(linhas[4])
    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo}' não foi encontrado.")
        return None, None, None, None, None
    except IndexError:
        print("Erro: O arquivo 'entrada.txt' não contém as 5 linhas de dados esperadas.")
        return None, None, None, None, None
    except ValueError as e:
        print(f"Erro ao converter dados numéricos em 'entrada.txt': {e}")
        return None, None, None, None, None

    def g(x, y):

        return eval(expressao, {
            "x": x,
            "y": y,
            "math": math,
            "e": math.e,
            "exp": math.exp,
            "sin": math.sin,
            "cos": math.cos
        })

    return g, x_ini, y_ini, passo, qtd


def escrever_saida(lista_x, lista_y, metodo):
    """
    Grava os resultados calculados (pares x, y) no arquivo 'saida.txt'.
    """
    caminho_out = os.path.join(os.path.dirname(__file__), "saida.txt")

    with open(caminho_out, "w") as arq:
        arq.write(f"Metodo: {metodo}\n")
        for a, b in zip(lista_x, lista_y):
            arq.write(f"x = {a:.6f}, y = {b:.6f}\n")


def plotar_solucao(lista_x, lista_y, nome_metodo):
    """
    Gera um gráfico da solução numérica (y em função de x) e salva como arquivo PNG.
    Retorna o nome do arquivo gerado.
    """
    plt.figure(figsize=(10, 6))
    
    plt.plot(lista_x, lista_y, marker='o', linestyle='-', color='blue', 
             label=f'Solução - {nome_metodo}')
    
    plt.title(f'Evolução da Solução pelo Método de {nome_metodo}', fontsize=14)
    plt.xlabel('Variável Independente (x)', fontsize=12)
    plt.ylabel('Variável Dependente (y)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc='best')
    
    nome_limpo = nome_metodo.replace(' ', '_').replace('ª', '')
    nome_arquivo = f"solucao_{nome_limpo}.png"
    caminho_grafico = os.path.join(os.path.dirname(__file__), nome_arquivo)
    
    plt.savefig(caminho_grafico)
    
    plt.close() 
    
    return nome_arquivo 

def metodo_rk3(fun, x_atual, y_atual, h, vezes):
    """
    Implementa o método de Runge-Kutta de 3ª Ordem.
    """
    xs = [x_atual]
    ys = [y_atual]

    for _ in range(vezes):
    
        k1 = fun(x_atual, y_atual)
        k2 = fun(x_atual + h/2, y_atual + h*k1/2)
        k3 = fun(x_atual + h, y_atual - h*k1 + 2*h*k2)

      
        y_atual += (h/6) * (k1 + 4*k2 + k3)
      
        x_atual += h

        xs.append(x_atual)
        ys.append(y_atual)

    return xs, ys


def metodo_rk4(fun, x_atual, y_atual, h, vezes):
    """
    Implementa o método de Runge-Kutta de 4ª Ordem.
    """
    xs = [x_atual]
    ys = [y_atual]

    for _ in range(vezes):
      
        k1 = fun(x_atual, y_atual)
        k2 = fun(x_atual + h/2, y_atual + h*k1/2)
        k3 = fun(x_atual + h/2, y_atual + h*k2/2)
        k4 = fun(x_atual + h, y_atual + h*k3)

       
        y_atual += (h/6) * (k1 + 2*k2 + 2*k3 + k4)
     
        x_atual += h

        xs.append(x_atual)
        ys.append(y_atual)

    return xs, ys


def principal():
    fun, xi, yi, h, n = ler_dados()
    
    if fun is None:
        return

    print("Escolha o metodo:")
    print("1 - Runge-Kutta 3ª Ordem")
    print("2 - Runge-Kutta 4ª Ordem")
    op = input("Digite o numero do metodo: ").strip()

    if op == "1":
        xs, ys = metodo_rk3(fun, xi, yi, h, n)
        nome = "Runge-Kutta 3ª Ordem"

    elif op == "2":
        xs, ys = metodo_rk4(fun, xi, yi, h, n)
        nome = "Runge-Kutta 4ª Ordem"

    else:
        print("Opção inválida.")
        return

    escrever_saida(xs, ys, nome)
    print(f"Resultados gravados em saida.txt usando o {nome}.")
    
    nome_arquivo_grafico = plotar_solucao(xs, ys, nome)
    print(f"Gráfico da solução salvo em '{nome_arquivo_grafico}'.")


if __name__ == "__main__":
    principal()