import math

# ==========================================
# FUNÇÕES MATEMÁTICAS E AMBIENTE SEGURO
# ==========================================

def avaliar_funcao(expressao, x_val):
    """
    Avalia uma função matemática em formato de string de forma segura.
    Inclui atalhos para facilitar a digitação no txt (ex: 'sin(x)' em vez de 'math.sin(x)').
    """
    ambiente_seguro = {"x": x_val, "math": math}
    # Carrega atalhos úteis da biblioteca math
    for func in ['sin', 'cos', 'tan', 'exp', 'log', 'sqrt', 'pi', 'e']:
        ambiente_seguro[func] = getattr(math, func)
        
    return eval(expressao, {"__builtins__": None}, ambiente_seguro)

# ==========================================
# MÉTODOS DE DERIVAÇÃO (DIFERENÇAS CENTRAIS)
# ==========================================

def derivada_primeira_ordem(funcao_str, x0, arquivo_saida, h=1e-5):
    """Calcula a 1ª Derivada f'(x) usando Diferenças Finitas Centrais."""
    arquivo_saida.write(f"\n--- FASE 1: AVALIACAO DOS PONTOS VIZINHOS ---\n")
    arquivo_saida.write(f"Metodo: Diferencas Finitas Centrais (passo h = {h})\n")
    
    # Avaliando os pontos levemente deslocados
    f_mais = avaliar_funcao(funcao_str, x0 + h)
    f_menos = avaliar_funcao(funcao_str, x0 - h)
    
    arquivo_saida.write(f"f(x0 + h) = f({x0 + h:.6f}) = {f_mais:.6f}\n")
    arquivo_saida.write(f"f(x0 - h) = f({x0 - h:.6f}) = {f_menos:.6f}\n")
    
    arquivo_saida.write("\n--- FASE 2: APLICACAO DA FORMULA ---\n")
    arquivo_saida.write("Formula: f'(x) = [f(x0 + h) - f(x0 - h)] / (2h)\n")
    
    # Cálculo final
    derivada = (f_mais - f_menos) / (2 * h)
    arquivo_saida.write(f"Calculo executado: [{f_mais:.6f} - {f_menos:.6f}] / {2 * h}\n")
    
    return derivada

def derivada_segunda_ordem(funcao_str, x0, arquivo_saida, h=1e-5):
    """Calcula a 2ª Derivada f''(x) usando Diferenças Finitas Centrais."""
    arquivo_saida.write(f"\n--- FASE 1: AVALIACAO DOS PONTOS VIZINHOS E CENTRAL ---\n")
    arquivo_saida.write(f"Metodo: Diferencas Finitas Centrais (passo h = {h})\n")
    
    # Avaliando os três pontos necessários para a concavidade
    f_mais = avaliar_funcao(funcao_str, x0 + h)
    f_central = avaliar_funcao(funcao_str, x0)
    f_menos = avaliar_funcao(funcao_str, x0 - h)
    
    arquivo_saida.write(f"f(x0 + h) = f({x0 + h:.6f}) = {f_mais:.6f}\n")
    arquivo_saida.write(f"f(x0)     = f({x0:.6f}) = {f_central:.6f}\n")
    arquivo_saida.write(f"f(x0 - h) = f({x0 - h:.6f}) = {f_menos:.6f}\n")
    
    arquivo_saida.write("\n--- FASE 2: APLICACAO DA FORMULA ---\n")
    arquivo_saida.write("Formula: f''(x) = [f(x0 + h) - 2f(x0) + f(x0 - h)] / (h^2)\n")
    
    # Cálculo final
    derivada = (f_mais - 2 * f_central + f_menos) / (h ** 2)
    # Exibindo h^2 em notação científica no txt para não poluir
    arquivo_saida.write(f"Calculo executado: [{f_mais:.6f} - 2*({f_central:.6f}) + {f_menos:.6f}] / {h**2:.1e}\n")
    
    return derivada

# ==========================================
# CÓDIGO PRINCIPAL: LEITURA E MENU
# ==========================================

def ler_arquivo(caminho):
    """Lê o arquivo esperando o formato: função ; ponto_x"""
    dados = []
    with open(caminho, 'r') as file_in:
        for linha in file_in:
            if linha.strip():
                if ';' in linha:
                    func_str, x0_str = linha.split(';')
                    dados.append((func_str.strip(), float(x0_str.strip())))
                else:
                    raise ValueError(f"A linha '{linha.strip()}' nao contem o separador ';'.")
    return dados

def main():
    caminho_entrada = 'entrada.txt'
    caminho_saida = 'saida.txt'
    
    print("====== MENU DE DERIVACAO NUMERICA ======")
    print("1 - Derivada de Primeira Ordem f'(x)")
    print("2 - Derivada de Segunda Ordem f''(x)")
    print("3 - Sair")
    opcao = input("Escolha o metodo desejado: ")

    if opcao == '3':
        print("Saindo...")
        return

    try:
        dados = ler_arquivo(caminho_entrada)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_entrada}' nao foi encontrado.")
        return
    except Exception as e:
        print(f"Erro na leitura dos dados: {e}")
        return

    with open(caminho_saida, 'w') as file_out:
        
        for i, (funcao, x0) in enumerate(dados):
            file_out.write("==================================================\n")
            if opcao == '1':
                file_out.write(f"RELATORIO: DERIVADA 1a ORDEM | FUNCAO {i+1}\n")
                file_out.write(f"Alvo: f(x) = {funcao} no ponto x0 = {x0}\n")
                resultado = derivada_primeira_ordem(funcao, x0, file_out)
                
            elif opcao == '2':
                file_out.write(f"RELATORIO: DERIVADA 2a ORDEM | FUNCAO {i+1}\n")
                file_out.write(f"Alvo: f(x) = {funcao} no ponto x0 = {x0}\n")
                resultado = derivada_segunda_ordem(funcao, x0, file_out)
                
            else:
                print("Opcao invalida.")
                return

            if resultado is not None:
                file_out.write("\n" + "-" * 45 + "\n")
                file_out.write("RESULTADO FINAL:\n")
                if opcao == '1':
                    file_out.write(f"f'({x0}) ~= {resultado:.6f}\n")
                else:
                    file_out.write(f"f''({x0}) ~= {resultado:.6f}\n")
                file_out.write("-" * 45 + "\n\n")

    print(f"\nSucesso! Os calculos de derivacao foram gravados em '{caminho_saida}'.\n")

if __name__ == "__main__":
    main()
    