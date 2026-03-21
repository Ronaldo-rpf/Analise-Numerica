"""
Implementação dos métodos de Runge-Kutta de 3ª e 4ª ordens para resolução de EDOs
"""

import math
import sys

class SolucionadorRungeKutta:
    """Classe para implementação dos métodos de Runge-Kutta"""
    
    def __init__(self):
        self.resultados_x = []
        self.resultados_y = []
    
    def carregar_configuracao(self, arquivo="entrada.txt"):
        """
        Carrega os parâmetros do problema do arquivo de entrada
        
        Formato do arquivo:
        Linha 1: f(x, y) - expressão da EDO
        Linha 2: x0 - valor inicial de x
        Linha 3: y0 - valor inicial de y
        Linha 4: h - tamanho do passo
        Linha 5: n - número de iterações
        """
        try:
            with open(arquivo, 'r') as f:
                linhas = f.readlines()
            
            if len(linhas) < 5:
                raise ValueError("Arquivo de entrada incompleto")
            
            # Remove espaços em branco e caracteres de nova linha
            expressao_edo = linhas[0].strip()
            x_inicial = float(linhas[1].strip())
            y_inicial = float(linhas[2].strip())
            passo = float(linhas[3].strip())
            iteracoes = int(linhas[4].strip())
            
            # Cria a função f(x, y) dinamicamente
            def funcao_diferencial(x_val, y_val):
                contexto = {
                    'x': x_val, 'y': y_val,
                    'math': math, 'sin': math.sin, 'cos': math.cos,
                    'exp': math.exp, 'log': math.log, 'sqrt': math.sqrt,
                    'e': math.e, 'pi': math.pi,
                    'tan': math.tan, 'asin': math.asin, 'acos': math.acos,
                    'atan': math.atan, 'sinh': math.sinh, 'cosh': math.cosh,
                    'tanh': math.tanh
                }
                return eval(expressao_edo, contexto)
            
            return funcao_diferencial, x_inicial, y_inicial, passo, iteracoes
            
        except FileNotFoundError:
            print(f"Erro: Arquivo '{arquivo}' não encontrado.")
            sys.exit(1)
        except ValueError as e:
            print(f"Erro no formato do arquivo: {e}")
            sys.exit(1)
    
    def executar_rk3(self, funcao, x0, y0, h, n):
        """
        Implementação do método de Runge-Kutta de 3ª ordem
        
        Fórmulas:
        k1 = f(x_n, y_n)
        k2 = f(x_n + h/2, y_n + (h/2)*k1)
        k3 = f(x_n + h, y_n - h*k1 + 2*h*k2)
        y_{n+1} = y_n + (h/6)*(k1 + 4*k2 + k3)
        """
        print("\nExecutando Runge-Kutta de 3ª ordem...")
        
        # Inicializa listas de resultados
        self.resultados_x = [x0]
        self.resultados_y = [y0]
        
        # Valores atuais
        x_atual = x0
        y_atual = y0
        
        # Loop de iterações
        for i in range(n):
            # Cálculo dos coeficientes
            k1 = funcao(x_atual, y_atual)
            k2 = funcao(x_atual + h/2, y_atual + (h/2) * k1)
            k3 = funcao(x_atual + h, y_atual - h*k1 + 2*h*k2)
            
            # Atualização dos valores
            y_atual = y_atual + (h/6) * (k1 + 4*k2 + k3)
            x_atual = x_atual + h
            
            # Armazenamento dos resultados
            self.resultados_x.append(x_atual)
            self.resultados_y.append(y_atual)
            
            # Feedback de progresso
            if (i + 1) % 25 == 0:
                print(f"  Iteração {i+1}/{n}: x = {x_atual:.6f}, y = {y_atual:.6f}")
        
        print("Runge-Kutta 3ª ordem concluído com sucesso!")
        return self.resultados_x, self.resultados_y
    
    def executar_rk4(self, funcao, x0, y0, h, n):
        """
        Implementação do método de Runge-Kutta de 4ª ordem
        
        Fórmulas:
        k1 = f(x_n, y_n)
        k2 = f(x_n + h/2, y_n + (h/2)*k1)
        k3 = f(x_n + h/2, y_n + (h/2)*k2)
        k4 = f(x_n + h, y_n + h*k3)
        y_{n+1} = y_n + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
        """
        print("\nExecutando Runge-Kutta de 4ª ordem...")
        
        # Inicializa listas de resultados
        self.resultados_x = [x0]
        self.resultados_y = [y0]
        
        # Valores atuais
        x_atual = x0
        y_atual = y0
        
        # Loop de iterações
        for i in range(n):
            # Cálculo dos coeficientes
            k1 = funcao(x_atual, y_atual)
            k2 = funcao(x_atual + h/2, y_atual + (h/2) * k1)
            k3 = funcao(x_atual + h/2, y_atual + (h/2) * k2)
            k4 = funcao(x_atual + h, y_atual + h * k3)
            
            # Atualização dos valores
            y_atual = y_atual + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
            x_atual = x_atual + h
            
            # Armazenamento dos resultados
            self.resultados_x.append(x_atual)
            self.resultados_y.append(y_atual)
            
            # Feedback de progresso
            if (i + 1) % 25 == 0:
                print(f"  Iteração {i+1}/{n}: x = {x_atual:.6f}, y = {y_atual:.6f}")
        
        print("Runge-Kutta 4ª ordem concluído com sucesso!")
        return self.resultados_x, self.resultados_y
    
    def salvar_resultados(self, metodo_nome, arquivo="saida.txt"):
        """
        Salva os resultados no arquivo de saída
        
        Formato:
        Método: [Nome do Método]
        x = valor, y = valor
        """
        try:
            with open(arquivo, 'w') as f:
                f.write(f"Método: {metodo_nome}\n")
                
                for x, y in zip(self.resultados_x, self.resultados_y):
                    linha = f"x = {x:.6f}, y = {y:.6f}\n"
                    f.write(linha)
            
            print(f" Resultados salvos em '{arquivo}'")
            print(f"  Total de pontos: {len(self.resultados_x)}")
            
        except IOError as e:
            print(f"Erro ao salvar resultados: {e}")
            sys.exit(1)
    
    def mostrar_resumo(self, metodo_nome):
        """
        Exibe um resumo dos resultados na tela
        """
        if not self.resultados_x:
            print("Nenhum resultado para exibir")
            return
        
        print("\n" + "="*60)
        print(f"RESUMO - {metodo_nome}")
        print("="*60)
        
        print(f"\n Condições iniciais:")
        print(f"  x0 = {self.resultados_x[0]:.6f}, y0 = {self.resultados_y[0]:.6f}")
        
        print(f"\n Valores finais:")
        print(f"  x_final = {self.resultados_x[-1]:.6f}, y_final = {self.resultados_y[-1]:.6f}")
        
        print(f"\n Estatísticas:")
        print(f"  Número de pontos: {len(self.resultados_x)}")
        print(f"  Variação em y: {self.resultados_y[-1] - self.resultados_y[0]:.6f}")
        
        # Mostra primeiros e últimos pontos
        if len(self.resultados_x) >= 4:
            print(f"\n Primeiros pontos:")
            for i in range(min(3, len(self.resultados_x))):
                print(f"  x = {self.resultados_x[i]:.6f}, y = {self.resultados_y[i]:.6f}")
            
            print(f"\n Últimos pontos:")
            for i in range(max(0, len(self.resultados_x)-3), len(self.resultados_x)):
                print(f"  x = {self.resultados_x[i]:.6f}, y = {self.resultados_y[i]:.6f}")
        
        print("="*60)


def apresentar_menu():
    """
    Exibe o menu de opções para o usuário
    """
    print("\n" + "="*50)
    print("MÉTODOS DE RUNGE-KUTTA")
    print("="*50)
    print("\nEscolha o método para resolver a EDO:")
    print("1. Runge-Kutta de 3ª ordem")
    print("2. Runge-Kutta de 4ª ordem")
    print("="*50)
    
    while True:
        try:
            escolha = input("\nDigite o número da opção (1 ou 2): ").strip()
            if escolha in ['1', '2']:
                return escolha
            else:
                print("Opção inválida! Digite 1 ou 2.")
        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário.")
            sys.exit(0)


def main():
    """
    Função principal do programa
    """
    print("="*60)
    print("IMPLEMENTAÇÃO DOS MÉTODOS DE RUNGE-KUTTA")
    print("Para Resolução de Equações Diferenciais Ordinárias")
    print("="*60)
    
    # Cria instância do solucionador
    solucionador = SolucionadorRungeKutta()
    
    # Carrega configuração do arquivo
    print("\n[1/4] Carregando configuração do arquivo 'entrada.txt'...")
    funcao_edo, x0, y0, h, n = solucionador.carregar_configuracao()
    
    # Mostra configuração carregada
    with open("entrada.txt", 'r') as f:
        expressao = f.readline().strip()
    print(f"  EDO: dy/dx = {expressao}")
    print(f"  Condições iniciais: x0 = {x0}, y0 = {y0}")
    print(f"  Parâmetros: passo h = {h}, iterações n = {n}")
    
    # Apresenta menu de escolha
    print("\n[2/4] Selecionando método...")
    escolha = apresentar_menu()
    
    # Executa o método escolhido
    print("\n[3/4] Executando método numérico...")
    if escolha == '1':
        solucionador.executar_rk3(funcao_edo, x0, y0, h, n)
        nome_metodo = "Runge-Kutta 3ª Ordem"
    else:
        solucionador.executar_rk4(funcao_edo, x0, y0, h, n)
        nome_metodo = "Runge-Kutta 4ª Ordem"
    
    # Salva os resultados
    print("\n[4/4] Salvando resultados no arquivo 'saida.txt'...")
    solucionador.salvar_resultados(nome_metodo)
    
    # Mostra resumo
    solucionador.mostrar_resumo(nome_metodo)
    
    # Oferece opção para ver detalhes
    try:
        resposta = input("\nDeseja visualizar todos os pontos? (s/n): ").lower().strip()
        if resposta == 's':
            print("\nTodos os pontos calculados:")
            print("-" * 40)
            for i, (x, y) in enumerate(zip(solucionador.resultados_x, solucionador.resultados_y)):
                # Mostra em grupos de 10 para facilitar visualização
                if i % 10 == 0 and i > 0:
                    input("\nPressione Enter para continuar...")
                    print("\n" + "-" * 40)
                print(f"Ponto {i:3d}: x = {x:8.6f}, y = {y:12.6f}")
    except KeyboardInterrupt:
        pass
    
    print("\n" + "="*60)
    print("Execução concluída com sucesso!")
    print("="*60)


if __name__ == "__main__":
    main()
