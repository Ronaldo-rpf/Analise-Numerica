import numpy as np
import time

# =========================================
# MÉTODOS DIRETOS E ITERATIVOS
# =========================================
def eliminacao_gauss(matriz, vetor):
    dim = len(vetor)
    matriz = matriz.astype(float)
    vetor = vetor.astype(float)

    # Eliminação progressiva
    for k in range(dim):
        if matriz[k, k] == 0:
            raise ZeroDivisionError("Pivô nulo durante eliminação de Gauss.")
        for i in range(k+1, dim):
            fator = matriz[i, k] / matriz[k, k]
            matriz[i, k:] -= fator * matriz[k, k:]
            vetor[i] -= fator * vetor[k]

    # Substituição regressiva
    solucao = np.zeros(dim)
    for i in range(dim-1, -1, -1):
        solucao[i] = (vetor[i] - np.dot(matriz[i, i+1:], solucao[i+1:])) / matriz[i, i]

    return solucao, None


def fatoracao_LU(matriz, vetor):
    dim = len(matriz)
    L = np.zeros_like(matriz)
    U = np.zeros_like(matriz)

    for i in range(dim):
        L[i, i] = 1
        for j in range(i, dim):
            U[i, j] = matriz[i, j] - np.dot(L[i, :i], U[:i, j])
        for j in range(i+1, dim):
            L[j, i] = (matriz[j, i] - np.dot(L[j, :i], U[:i, i])) / U[i, i]

    # resolve Ly = b
    vetor_y = np.zeros_like(vetor)
    for i in range(dim):
        vetor_y[i] = vetor[i] - np.dot(L[i, :i], vetor_y[:i])

    # resolve Ux = y
    solucao = np.zeros_like(vetor)
    for i in range(dim-1, -1, -1):
        solucao[i] = (vetor_y[i] - np.dot(U[i, i+1:], solucao[i+1:])) / U[i, i]

    return solucao, None


def metodo_jacobi(matriz, vetor, tol=1e-10, max_iter=1000):
    dim = len(vetor)
    solucao = np.zeros(dim)
    for k in range(max_iter):
        prox_solucao = np.zeros_like(solucao)
        for i in range(dim):
            soma = sum(matriz[i][j] * solucao[j] for j in range(dim) if j != i)
            if matriz[i][i] == 0:
                raise ZeroDivisionError(f"Pivô zero em matriz[{i},{i}]")
            prox_solucao[i] = (vetor[i] - soma) / matriz[i][i]
        if np.linalg.norm(prox_solucao - solucao, np.inf) < tol:
            return prox_solucao, k + 1
        solucao = prox_solucao
    return solucao, max_iter


def metodo_gauss_seidel(matriz, vetor, tol=1e-10, max_iter=1000):
    dim = len(vetor)
    solucao = np.zeros(dim)
    for k in range(max_iter):
        prox_solucao = np.copy(solucao)
        for i in range(dim):
            soma1 = sum(matriz[i][j] * prox_solucao[j] for j in range(i))
            soma2 = sum(matriz[i][j] * solucao[j] for j in range(i+1, dim))
            if matriz[i][i] == 0:
                raise ZeroDivisionError(f"Pivô zero em matriz[{i},{i}]")
            prox_solucao[i] = (vetor[i] - soma1 - soma2) / matriz[i][i]
        if np.linalg.norm(prox_solucao - solucao, np.inf) < tol:
            return prox_solucao, k + 1
        solucao = prox_solucao
    return solucao, max_iter


# =========================================
# LEITURA DE DADOS
# =========================================
def ler_entrada(arquivo):
    with open(arquivo, 'r') as f:
        dim = int(f.readline().strip())
        matriz, vetor = [], []
        for _ in range(dim):
            linha = list(map(float, f.readline().strip().split()))
            matriz.append(linha[:-1])
            vetor.append(linha[-1])
    return np.array(matriz), np.array(vetor)


# =========================================
# PRINCIPAL
# =========================================
def main(arquivo_entrada, metodo="gauss"):
    matriz, vetor = ler_entrada(arquivo_entrada)

    start = time.time()

    if metodo == "gauss":
        solucao, it = eliminacao_gauss(matriz, vetor)
    elif metodo == "lu":
        solucao, it = fatoracao_LU(matriz, vetor)
    elif metodo == "jacobi":
        solucao, it = metodo_jacobi(matriz, vetor)
    elif metodo == "gauss_seidel":
        solucao, it = metodo_gauss_seidel(matriz, vetor)
    else:
        raise ValueError("Método inválido.")

    duracao = time.time() - start

    print(f"\n>> Método escolhido: {metodo}")
    if solucao is None:
        print("O método não convergiu.")
    else:
        print(f"Solução: {[round(float(val), 6) for val in solucao]}")
        if it is not None:
            print(f"Iterações: {it}")
        print(f"Tempo de execução: {duracao:.6f} s")

    with open("saida.txt", "w") as fout:
        if solucao is None:
            fout.write("Não foi possível encontrar solução (divergência).\n")
        else:
            fout.write(f"Solução: {[round(float(val), 6) for val in solucao]}\n")
            if it is not None:
                fout.write(f"Iterações: {it}\n")
            fout.write(f"Tempo: {duracao:.6f} s\n")


if __name__ == "__main__":
    arquivo = "entrada.txt"
    metodo = input("Escolha o método (gauss, lu, jacobi, gauss_seidel): ").strip()
    main(arquivo, metodo)   
