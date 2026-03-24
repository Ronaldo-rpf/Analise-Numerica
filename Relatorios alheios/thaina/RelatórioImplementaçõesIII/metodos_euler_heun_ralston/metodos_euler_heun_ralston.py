import os
import math
import matplotlib.pyplot as plt 

def ler_dados():
    """
    Carrega a expressão da função f(x, y), condições iniciais,
    passo (h) e número de repetições (qtd) do arquivo 'entrada.txt'.
    Retorna a função g(x, y) e os parâmetros iniciais.
    """
    arquivo = os.path.join(os.path.dirname(__file__), "entrada.txt")

    try:
        with open(arquivo, "r") as arq:
            linhas = [ln.strip() for ln in arq.readlines()]
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
    (Mantido o nome original 'gravar_resultado' para consistência local)
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
    
    plt.plot(lista_x, lista_y, marker='o', linestyle='-', color='red', 
             label=f'Solução - {nome_metodo}')
    
    plt.title(f'Evolução da Solução pelo Método de {nome_metodo}', fontsize=14)
    plt.xlabel('Variável Independente (x)', fontsize=12)
    plt.ylabel('Variável Dependente (y)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc='best')
    
    nome_limpo = nome_metodo.replace(' ', '_').replace('ª', '').replace('-', '_')
    nome_arquivo = f"solucao_{nome_limpo}.png"
    caminho_grafico = os.path.join(os.path.dirname(__file__), nome_arquivo)
    
    plt.savefig(caminho_grafico)
    
    plt.close() 
    
    return nome_arquivo 
def metodo_euler(fun, x_atual, y_atual, h, vezes):
    """
    Implementa o método de Euler.
    """
    xs = [x_atual]
    ys = [y_atual]

    for _ in range(vezes):
        y_atual += h * fun(x_atual, y_atual)
        x_atual += h
        xs.append(x_atual)
        ys.append(y_atual)

    return xs, ys


def metodo_euler_mod(fun, x_atual, y_atual, h, vezes):
    """
    Implementa o método de Euler Modificado.
    """
    xs = [x_atual]
    ys = [y_atual]

    for _ in range(vezes):
        k_1 = fun(x_atual, y_atual)
        k_2 = fun(x_atual + h, y_atual + h * k_1)
        y_atual += (h / 2) * (k_1 + k_2)
        x_atual += h
        xs.append(x_atual)
        ys.append(y_atual)

    return xs, ys


def metodo_heun(fun, x_atual, y_atual, h, vezes):
    """
    Implementa o método de Heun (igual ao Euler Modificado/Runge-Kutta 2ª Ordem).
    """
    xs = [x_atual]
    ys = [y_atual]

    for _ in range(vezes):
        a1 = fun(x_atual, y_atual)
        a2 = fun(x_atual + h, y_atual + h * a1)
        y_atual += (h / 2) * (a1 + a2)
        x_atual += h
        xs.append(x_atual)
        ys.append(y_atual)

    return xs, ys


def metodo_ralston(fun, x_atual, y_atual, h, vezes):
    """
    Implementa o método de Ralston (Runge-Kutta 2ª Ordem com ênfase).
    """
    xs = [x_atual]
    ys = [y_atual]

    for _ in range(vezes):
        k1 = fun(x_atual, y_atual)
        k2 = fun(x_atual + (3/4)*h, y_atual + (3/4)*h*k1)
        # O Ralston usa pesos de 1/3 e 2/3
        y_atual += (h / 3) * (k1 + 2 * k2) 
        x_atual += h
        xs.append(x_atual)
        ys.append(y_atual)

    return xs, ys


def principal():
    """
    Função principal para carregar dados, solicitar a escolha do método,
    calcular a solução, salvar os resultados e gerar o gráfico.
    """
    fun, xi, yi, h, n = ler_dados()
    
    if fun is None:
        return

    print("Escolha o método numérico:")
    print("1 - Euler")
    print("2 - Euler Modificado")
    print("3 - Heun")
    print("4 - Ralston")

    escolha = input("Digite a opção desejada: ").strip()

    if escolha == "1":
        xs, ys = metodo_euler(fun, xi, yi, h, n)
        nome = "Euler"

    elif escolha == "2":
        xs, ys = metodo_euler_mod(fun, xi, yi, h, n)
        nome = "Euler Modificado"

    elif escolha == "3":
        xs, ys = metodo_heun(fun, xi, yi, h, n)
        nome = "Heun"

    elif escolha == "4":
        xs, ys = metodo_ralston(fun, xi, yi, h, n)
        nome = "Ralston"

    else:
        print("Opção inválida.")
        return

    escrever_saida(xs, ys, nome)
    print(f"Resultados gravados em saida.txt usando o {nome}.")
    
    nome_arquivo_grafico = plotar_solucao(xs, ys, nome)
    print(f"Gráfico da solução salvo em '{nome_arquivo_grafico}'.")


if __name__ == "__main__":
    principal()