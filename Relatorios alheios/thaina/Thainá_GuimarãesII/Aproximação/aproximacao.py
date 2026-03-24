import numpy as np
from sympy import Symbol, sympify, integrate, zeros, Matrix
import os
from datetime import datetime

def regressao_linear(valores_x, valores_y):
    soma_x = sum(valores_x)
    soma_y = sum(valores_y)
    soma_xy = sum(x * y for x, y in zip(valores_x, valores_y))
    soma_x2 = sum(x**2 for x in valores_x)
    n = len(valores_x)

    if n < 2:
        raise ValueError("Regressão Linear precisa de pelo menos 2 pontos.")

    b = (n * soma_xy - soma_x * soma_y) / (n * soma_x2 - soma_x**2)
    a = (soma_y - b * soma_x) / n

    polinomio_str = f"{b:.5f}*x + {a:.5f}"
    return polinomio_str

def mmq_discreto(valores_x, valores_y):
    if len(valores_x) < 3:
        raise ValueError(f"MMQ Discreto (grau 2) precisa de pelo menos 3 pontos, mas recebeu {len(valores_x)}.")

    x = Symbol("x")
    funcoes_base = [x**0, x**1, x**2]
    n_funcoes = len(funcoes_base)

    matriz_U = [[func.subs(x, val) for val in valores_x] for func in funcoes_base]

    vetor_F = np.zeros((n_funcoes, 1))
    matriz_M = np.zeros((n_funcoes, n_funcoes))
    for i in range(n_funcoes):
        for j in range(n_funcoes):
            matriz_M[i, j] = sum(np.multiply(matriz_U[i], matriz_U[j]))
        vetor_F[i, 0] = sum(np.multiply(valores_y, matriz_U[i]))

    coeficientes = np.linalg.solve(matriz_M, vetor_F)

    termos = []
    for i in reversed(range(n_funcoes)):
        coef = coeficientes[i, 0]
        if abs(coef) < 1e-12:
            continue
        if i == 0:
            termos.append(f"{coef:.5f}")
        elif i == 1:
            termos.append(f"{coef:.5f}*x")
        else:
            termos.append(f"{coef:.5f}*x**{i}")
    polinomio_str = " - ".join(termos).replace("- -", "+ ")
    return polinomio_str

def mmq_continuo(funcao_str, intervalo):
    x = Symbol("x")
    funcoes_base = [x**i for i in range(4)]
    n_base = len(funcoes_base)

    locais = {
        'x': x, 'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
        'exp': np.exp, 'log': np.log, 'sqrt': np.sqrt,
        'pi': np.pi, 'e': np.e, 'abs': abs, 'pow': pow
    }
    funcao_str = funcao_str.replace('^', '**').replace('math.e', 'e')
    func = sympify(funcao_str, locals=locais)

    matriz_M = zeros(n_base)
    vetor_F = zeros(n_base, 1)
    for i in range(n_base):
        for j in range(n_base):
            matriz_M[i, j] = integrate(funcoes_base[i] * funcoes_base[j], (x, intervalo[0], intervalo[1]))
        vetor_F[i, 0] = integrate(funcoes_base[i] * func, (x, intervalo[0], intervalo[1]))

    coeficientes = Matrix(matriz_M).pinv() * vetor_F

    termos = []
    for i in reversed(range(n_base)):
        coef = float(coeficientes[i, 0])
        if abs(coef) < 1e-12:
            continue
        if i == 0:
            termos.append(f"{coef:.5f}")
        elif i == 1:
            termos.append(f"{coef:.5f}*x")
        else:
            termos.append(f"{coef:.5f}*x**{i}")
    polinomio_str = " - ".join(termos).replace("- -", "+ ")
    return polinomio_str

def ler_entrada(nome_arquivo):
    caminho = os.path.abspath(nome_arquivo)
    if not os.path.exists(caminho):
        print(f"Arquivo '{caminho}' não encontrado.")
        return []
    with open(caminho, "r", encoding="utf-8") as f:
        return [linha.strip() for linha in f if linha.strip()]

def escrever_saida(metodo, resultados, nome_saida="saida_final.txt"):
    caminho = os.path.abspath(nome_saida)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(f"Resultados gerados em: {timestamp}\n")
        f.write(f"Método: {metodo}\n\n")
        if resultados:
            for r in resultados:
                f.write(str(r) + "\n")
        else:
            f.write("Nenhum resultado gerado.\n")
    print(f"Resultados salvos em {caminho}")

def processar_pares(linha):
    try:
        return [tuple(map(float, p.split(','))) for p in linha.split()]
    except Exception:
        raise ValueError(f"Linha inválida: {linha}")

def main():
    print("Escolha o método:")
    print("1 - Regressão Linear")
    print("2 - MMQ Discreto (Grau 2)")
    print("3 - MMQ Contínuo (Grau 3)")
    opcao = input("Opção: ").strip()

    if opcao == "3":
        linhas = ler_entrada("entrada2.txt")
    else:
        linhas = ler_entrada("entrada1.txt")

    if not linhas:
        print("Nenhum dado encontrado.")
        escrever_saida("Nenhum método", [])
        return

    resultados = []

    if opcao == "1":
        for linha in linhas:
            try:
                pares = processar_pares(linha)
                xs, ys = zip(*pares)
                resultados.append(regressao_linear(xs, ys))
            except Exception as e:
                resultados.append(f"Erro na linha '{linha}': {e}")
        escrever_saida("Regressão Linear", resultados)

    elif opcao == "2":
        for linha in linhas:
            try:
                pares = processar_pares(linha)
                xs, ys = zip(*pares)
                resultados.append(mmq_discreto(xs, ys))
            except Exception as e:
                resultados.append(f"Erro na linha '{linha}': {e}")
        escrever_saida("MMQ Discreto (Grau 2)", resultados)

    elif opcao == "3":
        for linha in linhas:
            try:
                if ';' not in linha:
                    resultados.append(f"Linha inválida: {linha}")
                    continue
                func_str, intervalo_str = linha.split(';')
                intervalo = tuple(map(float, intervalo_str.split(',')))
                resultados.append(mmq_continuo(func_str.strip(), intervalo))
            except Exception as e:
                resultados.append(f"Erro na linha '{linha}': {e}")
        escrever_saida("MMQ Contínuo (Grau 3)", resultados)

    else:
        print("Opção inválida!")
        escrever_saida("Opção inválida", [])

if __name__ == "__main__":
    main()
