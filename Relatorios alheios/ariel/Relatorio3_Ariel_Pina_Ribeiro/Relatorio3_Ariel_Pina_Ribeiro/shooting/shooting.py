"""
Implementação do Método de Shooting para resolução de problemas de valor de contorno
"""

import math
import sys

class SolucionadorShooting:
    """Classe principal para implementação do método de Shooting"""
    
    def __init__(self):
        self.pontos_x = []
        self.pontos_y = []
        self.derivadas = []
        self.num_iteracoes = 0
        self.chute_final = 0.0
    
    def carregar_configuracao(self, arquivo_entrada="entrada.txt"):
        """
        Carrega os parâmetros do problema de valor de contorno
        
        Formato do arquivo:
        Linha 1: f(x, y, dy) - expressão da EDO de segunda ordem
        Linha 2: a - extremo inferior do intervalo
        Linha 3: b - extremo superior do intervalo
        Linha 4: ya - valor de y no ponto a
        Linha 5: yb - valor desejado de y no ponto b
        Linha 6: s0 - primeiro chute para y'(a)
        Linha 7: s1 - segundo chute para y'(a)
        Linha 8: h - tamanho do passo
        """
        try:
            with open(arquivo_entrada, 'r') as f:
                linhas = f.readlines()
            
            if len(linhas) < 8:
                raise ValueError("Arquivo de entrada incompleto")
            
            # Processa cada linha
            expressao_edo = linhas[0].strip()
            extremo_inferior = float(linhas[1].strip())
            extremo_superior = float(linhas[2].strip())
            valor_ya = float(linhas[3].strip())
            valor_yb = float(linhas[4].strip())
            chute_inicial_1 = float(linhas[5].strip())
            chute_inicial_2 = float(linhas[6].strip())
            passo = float(linhas[7].strip())
            
            # Cria a função da EDO de segunda ordem
            def funcao_segunda_ordem(x_val, y_val, derivada_val):
                contexto = {
                    'x': x_val, 'y': y_val, 'dy': derivada_val,
                    'math': math, 'sin': math.sin, 'cos': math.cos,
                    'exp': math.exp, 'log': math.log, 'sqrt': math.sqrt,
                    'e': math.e, 'pi': math.pi,
                    'tan': math.tan, 'asin': math.asin, 'acos': math.acos,
                    'atan': math.atan
                }
                return eval(expressao_edo, contexto)
            
            print("Configuração carregada com sucesso")
            print(f"  EDO: y'' = {expressao_edo}")
            print(f"  Intervalo: [{extremo_inferior}, {extremo_superior}]")
            print(f"  Condições: y({extremo_inferior}) = {valor_ya}, y({extremo_superior}) = {valor_yb}")
            print(f"  Chutes iniciais: s0 = {chute_inicial_1}, s1 = {chute_inicial_2}")
            print(f"  Passo: h = {passo}")
            
            return (funcao_segunda_ordem, extremo_inferior, extremo_superior, 
                    valor_ya, valor_yb, chute_inicial_1, chute_inicial_2, passo)
            
        except FileNotFoundError:
            print(f"Erro: Arquivo '{arquivo_entrada}' não encontrado")
            sys.exit(1)
        except ValueError as e:
            print(f"Erro no formato dos dados: {e}")
            sys.exit(1)
    
    def resolver_sistema_edo(self, funcao, x_inicio, y_inicio, derivada_inicio, passo, num_pontos):
        """
        Resolve um sistema de EDOs de primeira ordem usando Runge-Kutta de 4ª ordem
        
        Sistema transformado:
        y' = z
        z' = f(x, y, z)
        """
        x_vals = [x_inicio]
        y_vals = [y_inicio]
        z_vals = [derivada_inicio]
        
        x_atual = x_inicio
        y_atual = y_inicio
        z_atual = derivada_inicio  # z = y'
        
        for _ in range(num_pontos):
            # Coeficientes para y
            k1_y = passo * z_atual
            # Coeficientes para z = y'
            k1_z = passo * funcao(x_atual, y_atual, z_atual)
            
            # Segundo estágio
            k2_y = passo * (z_atual + k1_z/2)
            k2_z = passo * funcao(x_atual + passo/2, 
                                   y_atual + k1_y/2, 
                                   z_atual + k1_z/2)
            
            # Terceiro estágio
            k3_y = passo * (z_atual + k2_z/2)
            k3_z = passo * funcao(x_atual + passo/2, 
                                   y_atual + k2_y/2, 
                                   z_atual + k2_z/2)
            
            # Quarto estágio
            k4_y = passo * (z_atual + k3_z)
            k4_z = passo * funcao(x_atual + passo, 
                                   y_atual + k3_y, 
                                   z_atual + k3_z)
            
            # Atualização
            y_atual += (k1_y + 2*k2_y + 2*k3_y + k4_y) / 6
            z_atual += (k1_z + 2*k2_z + 2*k3_z + k4_z) / 6
            x_atual += passo
            
            # Armazenamento
            x_vals.append(x_atual)
            y_vals.append(y_atual)
            z_vals.append(z_atual)
        
        return x_vals, y_vals, z_vals
    
    def executar_shooting(self, funcao, a, b, ya, yb, s0, s1, h, tol=1e-6, max_iter=50):
        """
        Executa o método de Shooting para encontrar a derivada inicial correta
        
        Args:
            funcao: função f(x, y, y') da EDO de segunda ordem
            a, b: extremos do intervalo
            ya, yb: condições de contorno
            s0, s1: chutes iniciais para y'(a)
            h: tamanho do passo
            tol: tolerância para convergência
            max_iter: número máximo de iterações
        """
        print(f"\nIniciando método de Shooting...")
        print(f"  Tolerância: {tol}, Máximo de iterações: {max_iter}")
        
        # Calcula número de pontos
        num_pontos = int((b - a) / h)
        
        # Primeira tentativa com s0
        print(f"\n  Tentativa 1: s = {s0}")
        x_vals0, y_vals0, _ = self.resolver_sistema_edo(funcao, a, ya, s0, h, num_pontos)
        erro0 = y_vals0[-1] - yb
        print(f"    y({b}) obtido: {y_vals0[-1]:.6f}, Erro: {erro0:.6e}")
        
        # Segunda tentativa com s1
        print(f"\n  Tentativa 2: s = {s1}")
        x_vals1, y_vals1, _ = self.resolver_sistema_edo(funcao, a, ya, s1, h, num_pontos)
        erro1 = y_vals1[-1] - yb
        print(f"    y({b}) obtido: {y_vals1[-1]:.6f}, Erro: {erro1:.6e}")
        
        # Método da secante para refinamento
        s_atual = s1
        s_anterior = s0
        erro_atual = erro1
        erro_anterior = erro0
        
        self.num_iteracoes = 2  # Já fizemos 2 tentativas
        
        while abs(erro_atual) > tol and self.num_iteracoes < max_iter:
            # Método da secante para novo chute
            if abs(erro_atual - erro_anterior) < 1e-15:
                print(" Diferença entre erros muito pequena, interrompendo iterações")
                break
            
            s_novo = s_atual - erro_atual * (s_atual - s_anterior) / (erro_atual - erro_anterior)
            
            print(f"\n  Iteração {self.num_iteracoes + 1}: s = {s_novo:.6f}")
            x_vals_novo, y_vals_novo, _ = self.resolver_sistema_edo(funcao, a, ya, s_novo, h, num_pontos)
            erro_novo = y_vals_novo[-1] - yb
            print(f"    y({b}) obtido: {y_vals_novo[-1]:.6f}, Erro: {erro_novo:.6e}")
            
            # Atualiza para próxima iteração
            s_anterior, erro_anterior = s_atual, erro_atual
            s_atual, erro_atual = s_novo, erro_novo
            
            self.num_iteracoes += 1
        
        # Última solução (a mais precisa)
        print(f"\n  Solução final: s = {s_atual:.6f}")
        x_final, y_final, z_final = self.resolver_sistema_edo(funcao, a, ya, s_atual, h, num_pontos)
        erro_final = y_final[-1] - yb
        print(f"    y({b}) final: {y_final[-1]:.6f}, Erro final: {erro_final:.6e}")
        
        self.pontos_x = x_final
        self.pontos_y = y_final
        self.derivadas = z_final
        self.chute_final = s_atual
        
        return x_final, y_final
    
    def salvar_resultados(self, arquivo_saida="saida.txt"):
        """
        Salva os resultados no arquivo de saída
        """
        try:
            with open(arquivo_saida, 'w') as f:
                f.write("Método: Shooting\n")
                
                for x, y in zip(self.pontos_x, self.pontos_y):
                    linha = f"x = {x:.6f}, y = {y:.6f}\n"
                    f.write(linha)
            
            print(f"\nResultados salvos em '{arquivo_saida}'")
            print(f"  Total de pontos: {len(self.pontos_x)}")
            
        except IOError as e:
            print(f"Erro ao salvar resultados: {e}")
    
    def exibir_resumo(self):
        """
        Exibe um resumo detalhado dos resultados
        """
        if not self.pontos_x:
            print("Nenhum resultado para exibir")
            return
        
        print("\n" + "="*60)
        print("RESUMO DO MÉTODO DE SHOOTING")
        print("="*60)
        
        print(f"\nInformações da convergência:")
        print(f"  Número de iterações: {self.num_iteracoes}")
        print(f"  Derivada inicial encontrada: y' = {self.chute_final:.6f}")
        
        print(f"\nCondições de contorno:")
        print(f"  y({self.pontos_x[0]}) = {self.pontos_y[0]:.6f} (condição fornecida)")
        print(f"  y({self.pontos_x[-1]}) = {self.pontos_y[-1]:.6f} (calculada)")
        
        print(f"\nPrimeiros pontos:")
        for i in range(min(3, len(self.pontos_x))):
            print(f"  x = {self.pontos_x[i]:.6f}, y = {self.pontos_y[i]:.6f}, y' = {self.derivadas[i]:.6f}")
        
        print(f"\nÚltimos pontos:")
        for i in range(max(0, len(self.pontos_x)-3), len(self.pontos_x)):
            print(f"  x = {self.pontos_x[i]:.6f}, y = {self.pontos_y[i]:.6f}, y' = {self.derivadas[i]:.6f}")
        
        print(f"\nEstatísticas:")
        print(f"  Intervalo: [{self.pontos_x[0]}, {self.pontos_x[-1]}]")
        print(f"  Variação em y: {self.pontos_y[-1] - self.pontos_y[0]:.6f}")
        print(f"  Derivada inicial: {self.derivadas[0]:.6f}")
        print(f"  Derivada final: {self.derivadas[-1]:.6f}")
        
        print("="*60)


def main():
    """
    Função principal do programa
    """
    print("="*60)
    print("IMPLEMENTAÇÃO DO MÉTODO DE SHOOTING")
    print("Para problemas de valor de contorno em EDOs de segunda ordem")
    print("="*60)
    
    # Cria instância do solucionador
    solucionador = SolucionadorShooting()
    
    # Carrega configuração
    print("\n[1/4] Carregando configuração do arquivo 'entrada.txt'...")
    (funcao_edo, a, b, ya, yb, s0, s1, h) = solucionador.carregar_configuracao()
    
    # Executa o método de Shooting
    print("\n[2/4] Executando método de Shooting...")
    solucionador.executar_shooting(funcao_edo, a, b, ya, yb, s0, s1, h)
    
    # Salva os resultados
    print("\n[3/4] Salvando resultados no arquivo 'saida.txt'...")
    solucionador.salvar_resultados()
    
    # Exibe resumo
    print("\n[4/4] Gerando resumo dos resultados...")
    solucionador.exibir_resumo()
    
    # Opção para visualização detalhada
    try:
        resposta = input("\n Deseja visualizar todos os pontos? (s/n): ").lower().strip()
        if resposta == 's':
            print("\nTodos os pontos calculados:")
            print("-" * 60)
            for i, (x, y, dy) in enumerate(zip(solucionador.pontos_x, solucionador.pontos_y, solucionador.derivadas)):
                # Mostra em grupos de 10 para facilitar visualização
                if i % 10 == 0 and i > 0:
                    input("\nPressione Enter para continuar...")
                    print("\n" + "-" * 60)
                print(f"Ponto {i:3d}: x = {x:6.2f}, y = {y:10.6f}, y' = {dy:10.6f}")
    except KeyboardInterrupt:
        pass
    
    print("\n" + "="*60)
    print("Método de Shooting concluído com sucesso!")
    print("="*60)


if __name__ == "__main__":
    main()
