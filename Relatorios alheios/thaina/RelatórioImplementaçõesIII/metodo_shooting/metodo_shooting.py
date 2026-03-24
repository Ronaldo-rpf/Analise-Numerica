import os
import math
import matplotlib.pyplot as plt 

BASE = os.path.dirname(os.path.abspath(__file__))

def ler_entrada():
    """
    Carrega a função de segunda ordem f(x, y, dy), condições de contorno (a, b, ya, yb),
    chutes iniciais para a inclinação (s0, s1) e o passo (h) do arquivo 'entrada.txt'.
    """
    caminho_entrada = os.path.join(BASE, "entrada.txt")

    try:
        with open(caminho_entrada, "r") as f:
            linhas = [linha.strip() for linha in f.readlines()]

            fx_line = linhas[0]
            a = float(linhas[1])
            b = float(linhas[2])
            ya = float(linhas[3])
            yb = float(linhas[4])
            s0 = float(linhas[5])
            s1 = float(linhas[6])
            h = float(linhas[7])

    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_entrada}' não foi encontrado.")
        return None, None, None, None, None, None, None, None
    except IndexError:
        print("Erro: O arquivo 'entrada.txt' não contém as 8 linhas de dados esperadas.")
        return None, None, None, None, None, None, None, None
    except ValueError as e:
        print(f"Erro ao converter dados numéricos em 'entrada.txt': {e}")
        return None, None, None, None, None, None, None, None


    def f(x, y, dy):
        """Função que representa a EDO de segunda ordem: y'' = f(x, y, dy)"""
        return eval(fx_line, {
            "x": x,
            "y": y,
            "dy": dy, 
            "math": math,
            "e": math.e,
            "exp": math.exp,
            "sin": math.sin,
            "cos": math.cos
        })

    return f, a, b, ya, yb, s0, s1, h


def salvar_saida(xs, ys, metodo_nome):
    """
    Grava os resultados calculados (pares x, y) no arquivo 'saida.txt'.
    """
    caminho_saida = os.path.join(BASE, "saida.txt")

    with open(caminho_saida, "w") as f:
        
        for x, y in zip(xs, ys):
            f.write(f"x = {x:.6f}, y = {y:.6f}\n")


def plotar_solucao(lista_x, lista_y, nome_metodo):
    """
    Gera um gráfico da solução final (y em função de x) e salva como arquivo PNG.
    Retorna o nome do arquivo gerado.
    """
    plt.figure(figsize=(10, 6))
    
    plt.plot(lista_x, lista_y, marker='o', linestyle='-', color='purple', 
             label=f'Solução Final - {nome_metodo}')
    
    plt.title(f'Solução de PVI pelo Método de {nome_metodo}', fontsize=14)
    plt.xlabel('Variável Independente (x)', fontsize=12)
    plt.ylabel('Variável Dependente (y)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc='best')
    
    nome_limpo = nome_metodo.replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '')
    nome_arquivo = f"solucao_{nome_limpo}.png"
    caminho_grafico = os.path.join(BASE, nome_arquivo)
    
    plt.savefig(caminho_grafico)
    
    plt.close() 
    
    return nome_arquivo 


def runge_kutta_4_ordem_edo2(f, x0, y0, dy0, h, n):
    """
    Aplica o método de Runge-Kutta de 4ª Ordem para resolver um sistema 
    de EDOs de 1ª ordem (equivalente a uma EDO de 2ª ordem).
    A EDO de 2ª ordem y'' = f(x, y, y') é convertida no sistema:
    1: y' = dy
    2: dy' = f(x, y, dy)
    """
    xs = [x0]
    ys = [y0]
    dy = dy0

    for _ in range(n):
        
        k1 = h * dy
        l1 = h * f(x0, y0, dy)

        k2 = h * (dy + l1 / 2)
        l2 = h * f(x0 + h / 2, y0 + k1 / 2, dy + l1 / 2)

        k3 = h * (dy + l2 / 2)
        l3 = h * f(x0 + h / 2, y0 + k2 / 2, dy + l2 / 2)

        k4 = h * (dy + l3)
        l4 = h * f(x0 + h, y0 + k3, dy + l3)

        y0 += (k1 + 2*k2 + 2*k3 + k4) / 6
        dy += (l1 + 2*l2 + 2*l3 + l4) / 6
        x0 += h

        xs.append(x0)
        ys.append(y0)

    return xs, ys


def shooting(f, a, b, ya, yb, s0, s1, h, tol=1e-5, max_iter=100):
    """
    Implementa o Método do Tiro (Shooting Method) usando o Método da Secante
    para encontrar a inclinação inicial correta (y'(a)).
    """
    n = int(round((b - a) / h))

    _, ys0 = runge_kutta_4_ordem_edo2(f, a, ya, s0, h, n)
    f0 = ys0[-1] - yb 

    _, ys1 = runge_kutta_4_ordem_edo2(f, a, ya, s1, h, n)
    f1 = ys1[-1] - yb 

    iter_count = 0
    s_final = s1

    print(f"Iteração 0: s = {s0:.6f}, Erro (f(s)) = {f0:.6f}")
    print(f"Iteração 1: s = {s1:.6f}, Erro (f(s)) = {f1:.6f}")


    while abs(f1) > tol and iter_count < max_iter:
        try:
            s = s1 - f1 * (s1 - s0) / (f1 - f0)
        except ZeroDivisionError:
            print("Erro: Divisão por zero no Método da Secante. Ajuste os chutes s0 e s1.")
            return None, None

        xs, ys = runge_kutta_4_ordem_edo2(f, a, ya, s, h, n)
        fs = ys[-1] - yb 

        s0, f0 = s1, f1
        s1, f1 = s, fs
        s_final = s1
        iter_count += 1
        
        print(f"Iteração {iter_count + 1}: s = {s_final:.6f}, Erro (f(s)) = {f1:.6f}")


    if iter_count >= max_iter:
        print(f"Aviso: O método não convergiu após {max_iter} iterações. Resultado final pode ser impreciso.")
        
    print(f"\nConvergência alcançada em {iter_count + 1} iterações. Inclinação inicial ideal y'(a) ≈ {s_final:.6f}")
    return xs, ys


def main():
    f, a, b, ya, yb, s0, s1, h = ler_entrada()
    
    if f is None:
        return

    print("Iniciando Método do Tiro (Shooting Method) com RK4...")
    
    xs, ys = shooting(f, a, b, ya, yb, s0, s1, h)
    nome = "Shooting Method (Tiro)"
    
    if xs is None:
        print("Falha na execução do Método do Tiro.")
        return

    salvar_saida(xs, ys, nome)
    print(f"\nProcesso concluído. Resultados salvos em saida.txt usando o {nome}.")

    nome_arquivo_grafico = plotar_solucao(xs, ys, nome)
    print(f"Gráfico da solução final salvo em '{nome_arquivo_grafico}'.")


if __name__ == "__main__":
    main()