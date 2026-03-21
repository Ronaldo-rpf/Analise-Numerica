import numpy as np

# ==== Métodos de interpolação ====
def lagrange(pontos):
    xs = [p[0] for p in pontos]
    ys = [p[1] for p in pontos]
    n = len(pontos)
    pol = np.zeros(n)

    for i in range(n):
        Li = np.poly1d([1.0])
        for j in range(n):
            if i != j:
                Li *= np.poly1d([1.0, -xs[j]]) / (xs[i] - xs[j])
        pol += ys[i] * Li

    termos = [f"{c:.4g}x^{i}" for i, c in enumerate(pol[::-1]) if abs(c) > 1e-10]
    return "P(x) ≈ " + " + ".join(termos)

def newton(pontos):
    n = len(pontos)
    xs = [p[0] for p in pontos]
    ys = [p[1] for p in pontos]

    coef = ys.copy()
    for i in range(1, n):
        for j in range(n - 1, i - 1, -1):
            coef[j] = (coef[j] - coef[j - 1]) / (xs[j] - xs[j - i])

    pol = np.poly1d([0.0])
    termo = np.poly1d([1.0])
    for i in range(n):
        pol += coef[i] * termo
        termo *= np.poly1d([1.0, -xs[i]])

    c = pol.coeffs
    termos = [f"{v:.4g}x^{i}" for i, v in enumerate(c[::-1]) if abs(v) > 1e-10]
    return "P(x) ≈ " + " + ".join(termos)

# ==== Entrada e saída ====
def carregar_dados(nome_arquivo="entrada.txt"):
    with open(nome_arquivo, "r") as f:
        return [linha.strip() for linha in f if linha.strip()]

def salvar_resultados(resultados, metodo):
    arquivo_saida = "saida_final.txt"
    with open(arquivo_saida, "a", encoding="utf-8") as f:
        f.write(f"\n[Método: {metodo}]\n")
        for r in resultados:
            f.write(r + "\n")
    print(f"[OK] Resultados salvos em '{arquivo_saida}'.")

def interpretar_pares(linha):
    return [tuple(map(float, p.split(','))) for p in linha.split()]

# ==== Programa principal ====
def main():
    print("Escolha o método de interpolação:")
    print("1 - Lagrange\n2 - Newton")

    opcao = input("Opção: ").strip()
    linhas = carregar_dados("entrada.txt")
    resultados = []

    if opcao == "1":
        for linha in linhas:
            pares = interpretar_pares(linha)
            resultados.append(lagrange(pares))
        salvar_resultados(resultados, "Lagrange")

    elif opcao == "2":
        for linha in linhas:
            pares = interpretar_pares(linha)
            resultados.append(newton(pares))
        salvar_resultados(resultados, "Newton")

    else:
        print("Opção inválida!")

if __name__ == "__main__":
    main()
