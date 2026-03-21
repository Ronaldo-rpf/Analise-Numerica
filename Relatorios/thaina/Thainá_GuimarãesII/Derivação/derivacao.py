import numpy as np

# ==== Funções de derivação ====

h = 1e-5

def avaliar(expressao, x):
    contexto = {
        'x': x,
        'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
        'exp': np.exp, 'log': np.log, 'sqrt': np.sqrt,
        'pi': np.pi, 'e': np.e, 'abs': abs, 'pow': pow
    }
    try:
        return eval(expressao, {"__builtins__": None}, contexto)
    except Exception as e:
        raise ValueError(f"Erro ao avaliar função '{expressao}' no ponto {x}: {e}")

def derivada_primeira_ordem(expressao, x):
    return (avaliar(expressao, x + h) - avaliar(expressao, x - h)) / (2 * h)

def derivada_segunda_ordem(expressao, x):
    return (avaliar(expressao, x + h) - 2 * avaliar(expressao, x) + avaliar(expressao, x - h)) / (h ** 2)

# ==== Entrada e saída ====

def carregar_dados(nome_arquivo="entrada.txt"):
    with open(nome_arquivo, "r") as f:
        linhas = [l.strip() for l in f if l.strip()]
    dados = []
    for linha in linhas:
        try:
            func, x_str = linha.split(";")
            dados.append((func.strip(), float(x_str.strip())))
        except Exception:
            raise ValueError(f"Formato inválido na linha: '{linha}'. Esperado 'função ; x'")
    return dados

def salvar_resultado(resultados, metodo):
    arquivo_saida = "saida_final.txt"
    with open(arquivo_saida, "a", encoding="utf-8") as f:
        f.write(f"\n[Método: {metodo}]\n")
        for i, res in enumerate(resultados, 1):
            f.write(f"Função {i}: {res}\n")
    print(f"[OK] Resultados salvos em '{arquivo_saida}'.")

# ==== Programa principal ====

def main():
    print("Escolha o método de derivação:")
    print("1 - Primeira Ordem")
    print("2 - Segunda Ordem")

    opcao = input("Opção: ").strip()
    dados = carregar_dados("entrada.txt")
    resultados = []

    if opcao == "1":
        for funcao, x in dados:
            try:
                valor = derivada_primeira_ordem(funcao, x)
                resultados.append(f"{valor:.6g}")
            except Exception as e:
                resultados.append(f"Erro: {e}")
        salvar_resultado(resultados, "Primeira Ordem")

    elif opcao == "2":
        for funcao, x in dados:
            try:
                valor = derivada_segunda_ordem(funcao, x)
                resultados.append(f"{valor:.6g}")
            except Exception as e:
                resultados.append(f"Erro: {e}")
        salvar_resultado(resultados, "Segunda Ordem")

    else:
        print("Opção inválida!")

if __name__ == "__main__":
    main()
