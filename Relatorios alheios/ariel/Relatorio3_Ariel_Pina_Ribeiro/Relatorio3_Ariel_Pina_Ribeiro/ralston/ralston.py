"""
Implementação do método de Ralston para resolução de equações diferenciais
"""

import math

class SolucionadorRalston:
    """Classe principal para implementação do método de Ralston"""
    
    def __init__(self):
        self.resultados_x = []
        self.resultados_y = []
    
    def ler_parametros(self, arquivo_entrada="entrada.txt"):
        """
        Lê os parâmetros do arquivo de entrada no formato padrão
        
        Formato do arquivo:
        Linha 1: f(x, y) - expressão da EDO
        Linha 2: x0 - valor inicial de x
        Linha 3: y0 - valor inicial de y
        Linha 4: h - tamanho do passo
        Linha 5: n - número de iterações
        """
        try:
            with open(arquivo_entrada, 'r') as f:
                conteudo = f.read().strip().split('\n')
            
            if len(conteudo) < 5:
                raise ValueError("Arquivo de entrada incompleto")
            
            # Extração dos parâmetros
            expressao_edo = conteudo[0].strip()
            inicio_x = float(conteudo[1].strip())
            inicio_y = float(conteudo[2].strip())
            passo = float(conteudo[3].strip())
            num_iteracoes = int(conteudo[4].strip())
            
            # Criação da função a partir da expressão
            def funcao_diferencial(x_val, y_val):
                contexto = {
                    'x': x_val,
                    'y': y_val,
                    'math': math,
                    'sin': math.sin,
                    'cos': math.cos,
                    'exp': math.exp,
                    'log': math.log,
                    'sqrt': math.sqrt,
                    'e': math.e,
                    'pi': math.pi
                }
                return eval(expressao_edo, contexto)
            
            print("✓ Parâmetros carregados com sucesso")
            print(f"  EDO: dy/dx = {expressao_edo}")
            print(f"  Condições iniciais: x0 = {inicio_x}, y0 = {inicio_y}")
            print(f"  Passo: h = {passo}, Iterações: n = {num_iteracoes}")
            
            return funcao_diferencial, inicio_x, inicio_y, passo, num_iteracoes
            
        except FileNotFoundError:
            print(f"Erro: Arquivo '{arquivo_entrada}' não encontrado")
            exit(1)
        except ValueError as e:
            print(f"Erro no formato dos dados: {e}")
            exit(1)
    
    def calcular_passo_ralston(self, funcao, x_atual, y_atual, passo):
        """
        Realiza um único passo do método de Ralston
        
        Fórmula do método de Ralston:
        k1 = f(x_n, y_n)
        k2 = f(x_n + (3/4)h, y_n + (3/4)h*k1)
        y_{n+1} = y_n + (h/3)*(k1 + 2*k2)
        """
        # Coeficiente k1 - inclinação no ponto atual
        coeficiente_k1 = funcao(x_atual, y_atual)
        
        # Coeficiente k2 - inclinação no ponto a 75% do passo
        x_intermediario = x_atual + (3/4) * passo
        y_intermediario = y_atual + (3/4) * passo * coeficiente_k1
        coeficiente_k2 = funcao(x_intermediario, y_intermediario)
        
        # Atualização de y usando a combinação ponderada
        y_novo = y_atual + (passo/3) * (coeficiente_k1 + 2 * coeficiente_k2)
        x_novo = x_atual + passo
        
        return x_novo, y_novo
    
    def executar(self, funcao, x0, y0, h, n):
        """
        Executa o método de Ralston para n iterações
        
        Args:
            funcao: função f(x, y) da EDO
            x0, y0: condições iniciais
            h: tamanho do passo
            n: número de iterações
        """
        print("\n⏳ Executando método de Ralston...")
        
        # Inicialização das listas de resultados
        self.resultados_x = [x0]
        self.resultados_y = [y0]
        
        # Valores atuais
        x_atual = x0
        y_atual = y0
        
        # Execução das iterações
        for iteracao in range(n):
            x_atual, y_atual = self.calcular_passo_ralston(funcao, x_atual, y_atual, h)
            
            # Armazenamento dos resultados
            self.resultados_x.append(x_atual)
            self.resultados_y.append(y_atual)
            
            # Feedback de progresso a cada 20 iterações
            if (iteracao + 1) % 20 == 0:
                print(f"  Iteração {iteracao + 1}/{n}: x = {x_atual:.6f}, y = {y_atual:.6f}")
        
        print("✓ Método de Ralston concluído com sucesso!")
        return self.resultados_x, self.resultados_y
    
    def salvar_resultados(self, arquivo_saida="saida.txt"):
        """
        Salva os resultados no arquivo de saída no formato padrão
        """
        try:
            with open(arquivo_saida, 'w') as f:
                f.write("Método: Ralston\n")
                
                for x, y in zip(self.resultados_x, self.resultados_y):
                    linha = f"x = {x:.6f}, y = {y:.6f}\n"
                    f.write(linha)
            
            print(f"✓ Resultados salvos em '{arquivo_saida}'")
            print(f"  Total de pontos calculados: {len(self.resultados_x)}")
            
        except IOError as e:
            print(f"Erro ao salvar resultados: {e}")
    
    def exibir_resumo(self):
        """
        Exibe um resumo dos resultados obtidos
        """
        if not self.resultados_x:
            print("Nenhum resultado para exibir")
            return
        
        print("\n" + "="*60)
        print("RESUMO DOS RESULTADOS - MÉTODO DE RALSTON")
        print("="*60)
        
        # Primeiros 3 pontos
        print("\nPrimeiros pontos calculados:")
        for i in range(min(3, len(self.resultados_x))):
            print(f"  x = {self.resultados_x[i]:.6f}, y = {self.resultados_y[i]:.6f}")
        
        # Últimos 3 pontos
        if len(self.resultados_x) > 6:
            print("\nÚltimos pontos calculados:")
            for i in range(len(self.resultados_x)-3, len(self.resultados_x)):
                print(f"  x = {self.resultados_x[i]:.6f}, y = {self.resultados_y[i]:.6f}")
        elif len(self.resultados_x) > 3:
            print("\nÚltimos pontos calculados:")
            for i in range(3, len(self.resultados_x)):
                print(f"  x = {self.resultados_x[i]:.6f}, y = {self.resultados_y[i]:.6f}")
        
        # Estatísticas
        print("\nEstatísticas:")
        print(f"  Intervalo de x: de {self.resultados_x[0]:.4f} a {self.resultados_x[-1]:.4f}")
        print(f"  Variação total em y: {self.resultados_y[-1] - self.resultados_y[0]:.6f}")
        print(f"  Média dos valores de y: {sum(self.resultados_y)/len(self.resultados_y):.6f}")
        
        # Verificação de convergência
        if len(self.resultados_y) > 1:
            variacao_final = abs(self.resultados_y[-1] - self.resultados_y[-2])
            print(f"  Variação no último passo: {variacao_final:.6e}")
        
        print("="*60)


def main():
    """
    Função principal do programa
    """
    print("="*60)
    print("IMPLEMENTAÇÃO DO MÉTODO DE RALSTON")
    print("Solução Numérica de Equações Diferenciais Ordinárias")
    print("="*60)
    
    # Cria instância do solucionador
    solucionador = SolucionadorRalston()
    
    # Carrega parâmetros do arquivo de entrada
    print("\n[1/4] Carregando parâmetros do arquivo 'entrada.txt'...")
    funcao_edo, x_inicial, y_inicial, passo, iteracoes = solucionador.ler_parametros()
    
    # Executa o método
    print("\n[2/4] Executando o método numérico...")
    solucionador.executar(funcao_edo, x_inicial, y_inicial, passo, iteracoes)
    
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
            print("\nPontos calculados:")
            for i, (x, y) in enumerate(zip(solucionador.resultados_x, solucionador.resultados_y)):
                print(f"{i:3d}: x = {x:8.6f}, y = {y:12.6f}")
    except KeyboardInterrupt:
        pass
    
    print("\n" + "="*60)
    print("Execução concluída com sucesso!")
    print("="*60)


if __name__ == "__main__":
    main()
