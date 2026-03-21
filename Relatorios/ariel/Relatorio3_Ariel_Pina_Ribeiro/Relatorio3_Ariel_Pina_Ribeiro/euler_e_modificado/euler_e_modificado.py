"""
Implementação dos métodos de Euler e Euler Modificado para resolução de EDOs
"""

import math

class ResolvedorEDO:
    """Classe para resolução de Equações Diferenciais Ordinárias"""
    
    @staticmethod
    def configurar_problema(arquivo_entrada="entrada.txt"):
        """
        Lê os parâmetros do problema a partir do arquivo de entrada
        
        Formato do arquivo:
        linha 1: expressão da EDO (dy/dx = f(x, y))
        linha 2: valor inicial de x (x0)
        linha 3: valor inicial de y (y0)
        linha 4: tamanho do passo (h)
        linha 5: número de iterações (n)
        """
        with open(arquivo_entrada, 'r') as arquivo:
            dados = arquivo.readlines()
        
        # Processa cada linha do arquivo
        expressao_edo = dados[0].strip()
        ponto_inicial_x = float(dados[1].strip())
        ponto_inicial_y = float(dados[2].strip())
        tamanho_passo = float(dados[3].strip())
        iteracoes = int(dados[4].strip())
        
        # Cria a função f(x, y) a partir da expressão
        def funcao_edo(x, y):
            return eval(expressao_edo, {
                "x": x, 
                "y": y, 
                "math": math, 
                "e": math.e, 
                "exp": math.exp, 
                "sin": math.sin, 
                "cos": math.cos,
                "log": math.log,
                "sqrt": math.sqrt
            })
        
        return funcao_edo, ponto_inicial_x, ponto_inicial_y, tamanho_passo, iteracoes
    
    @staticmethod
    def registrar_resultados(pontos_x, pontos_y, metodo, arquivo_saida="saida.txt"):
        """
        Registra os resultados da simulação no arquivo de saída
        """
        with open(arquivo_saida, 'w') as arquivo:
            arquivo.write(f"Método: {metodo}\n")
            for x, y in zip(pontos_x, pontos_y):
                arquivo.write(f"x = {x:.6f}, y = {y:.6f}\n")
        print(f"Resultados salvos em '{arquivo_saida}'")


class MetodoEuler:
    """Implementação do método de Euler para EDOs"""
    
    def __init__(self, funcao, x_inicial, y_inicial, passo, iteracoes):
        self.f = funcao
        self.x_atual = x_inicial
        self.y_atual = y_inicial
        self.h = passo
        self.n = iteracoes
        self.pontos_x = []
        self.pontos_y = []
    
    def executar(self):
        """Executa o método de Euler"""
        # Registra o ponto inicial
        self.pontos_x.append(self.x_atual)
        self.pontos_y.append(self.y_atual)
        
        # Executa as iterações
        for _ in range(self.n):
            # Calcula o próximo valor usando a fórmula de Euler
            inclinacao = self.f(self.x_atual, self.y_atual)
            self.y_atual += self.h * inclinacao
            self.x_atual += self.h
            
            # Armazena os resultados
            self.pontos_x.append(self.x_atual)
            self.pontos_y.append(self.y_atual)
        
        return self.pontos_x, self.pontos_y


class MetodoEulerModificado:
    """Implementação do método de Euler Modificado"""
    
    def __init__(self, funcao, x_inicial, y_inicial, passo, iteracoes):
        self.f = funcao
        self.x_atual = x_inicial
        self.y_atual = y_inicial
        self.h = passo
        self.n = iteracoes
        self.pontos_x = []
        self.pontos_y = []
    
    def executar(self):
        """Executa o método de Euler Modificado"""
        # Registra o ponto inicial
        self.pontos_x.append(self.x_atual)
        self.pontos_y.append(self.y_atual)
        
        # Executa as iterações
        for _ in range(self.n):
            # Primeiro estágio: previsão com Euler simples
            inclinacao_inicial = self.f(self.x_atual, self.y_atual)
            y_previsao = self.y_atual + self.h * inclinacao_inicial
            x_proximo = self.x_atual + self.h
            
            # Segundo estágio: correção usando a inclinação no ponto previsto
            inclinacao_final = self.f(x_proximo, y_previsao)
            inclinacao_media = (inclinacao_inicial + inclinacao_final) / 2
            
            # Atualiza os valores
            self.y_atual += self.h * inclinacao_media
            self.x_atual = x_proximo
            
            # Armazena os resultados
            self.pontos_x.append(self.x_atual)
            self.pontos_y.append(self.y_atual)
        
        return self.pontos_x, self.pontos_y


def apresentar_menu():
    """Apresenta o menu de escolha de métodos"""
    print("\n" + "="*50)
    print("RESOLUÇÃO DE EQUAÇÕES DIFERENCIAIS ORDINÁRIAS")
    print("="*50)
    print("\nEscolha o método numérico para resolução:")
    print("1. Método de Euler")
    print("2. Método de Euler Modificado")
    print("="*50)
    
    while True:
        escolha = input("\nDigite o número do método desejado (1 ou 2): ").strip()
        if escolha in ["1", "2"]:
            return escolha
        else:
            print("Opção inválida! Por favor, digite 1 ou 2.")


def main():
    """Função principal do programa"""
    try:
        # Carrega a configuração do problema
        print("Carregando configuração do arquivo 'entrada.txt'...")
        funcao_edo, x0, y0, h, n = ResolvedorEDO.configurar_problema()
        
        # Apresenta os parâmetros carregados
        print(f"\nParâmetros do problema:")
        print(f"  x0 = {x0}")
        print(f"  y0 = {y0}")
        print(f"  h  = {h}")
        print(f"  n  = {n}")
        
        # Solicita a escolha do método
        opcao = apresentar_menu()
        
        # Executa o método selecionado
        if opcao == "1":
            print("\nExecutando o Método de Euler...")
            resolvedor = MetodoEuler(funcao_edo, x0, y0, h, n)
            pontos_x, pontos_y = resolvedor.executar()
            nome_metodo = "Euler"
        else:
            print("\nExecutando o Método de Euler Modificado...")
            resolvedor = MetodoEulerModificado(funcao_edo, x0, y0, h, n)
            pontos_x, pontos_y = resolvedor.executar()
            nome_metodo = "Euler Modificado"
        
        # Exibe um resumo dos resultados
        print(f"\nSimulação concluída com sucesso!")
        print(f"  Primeiro ponto: x = {pontos_x[0]:.6f}, y = {pontos_y[0]:.6f}")
        print(f"  Último ponto:   x = {pontos_x[-1]:.6f}, y = {pontos_y[-1]:.6f}")
        
        # Salva os resultados
        ResolvedorEDO.registrar_resultados(pontos_x, pontos_y, nome_metodo)
        
        # Oferece opção para visualizar alguns pontos
        visualizar = input("\nDeseja visualizar os primeiros 5 pontos? (s/n): ").strip().lower()
        if visualizar == 's':
            print("\nPrimeiros 5 pontos da simulação:")
            for i in range(min(5, len(pontos_x))):
                print(f"  x = {pontos_x[i]:.6f}, y = {pontos_y[i]:.6f}")
        
        print("\nProcesso finalizado!")
        
    except FileNotFoundError:
        print("Erro: Arquivo 'entrada.txt' não encontrado!")
        print("Certifique-se de que o arquivo existe no diretório atual.")
    except Exception as e:
        print(f"Ocorreu um erro durante a execução: {e}")


if __name__ == "__main__":
    main()
