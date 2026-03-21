"""
Implementação do Método das Diferenças Finitas para problemas de valor de contorno
"""

import numpy as np
import math
import sys

class SolucionadorDiferencasFinitas:
    """
    Classe para resolver problemas de valor de contorno usando o método das diferenças finitas.
    
    O método transforma a equação diferencial em um sistema linear tridiagonal
    que é resolvido usando álgebra linear numérica.
    """
    
    def __init__(self):
        """Inicializa o solucionador de diferenças finitas."""
        self.pontos_x = None
        self.pontos_y = None
        self.tamanho_passo = 0.0
        self.num_subintervalos = 0
    
    def ler_parametros_entrada(self, nome_arquivo="entrada.txt"):
        """
        Lê os parâmetros do problema a partir do arquivo de entrada.
        
        Formato esperado do arquivo:
        Linha 1: f(x, y) - termo fonte da equação y'' = f(x, y)
        Linha 2: a - extremo inferior do intervalo
        Linha 3: b - extremo superior do intervalo
        Linha 4: ya - valor de y no ponto a (condição de contorno)
        Linha 5: yb - valor de y no ponto b (condição de contorno)
        Linha 6: n - número de subintervalos para discretização
        
        Retorna: tupla (funcao_f, a, b, ya, yb, n)
        """
        try:
            with open(nome_arquivo, 'r') as arquivo:
                linhas = arquivo.readlines()
            
            if len(linhas) < 6:
                raise ValueError("O arquivo de entrada deve conter pelo menos 6 linhas")
            
            # Processa cada linha, removendo espaços em branco
            expressao_fonte = linhas[0].strip()
            limite_inferior = float(linhas[1].strip())
            limite_superior = float(linhas[2].strip())
            condicao_inicial = float(linhas[3].strip())
            condicao_final = float(linhas[4].strip())
            num_divisoes = int(linhas[5].strip())
            
            # Validação dos parâmetros
            if limite_inferior >= limite_superior:
                raise ValueError("O limite inferior deve ser menor que o limite superior")
            
            if num_divisoes <= 0:
                raise ValueError("O número de subintervalos deve ser positivo")
            
            # Cria a função f(x, y) a partir da expressão fornecida
            def funcao_fonte(x_valor, y_valor):
                contexto = {
                    'x': x_valor, 
                    'y': y_valor,
                    'math': math,
                    'sin': math.sin,
                    'cos': math.cos,
                    'exp': math.exp,
                    'log': math.log,
                    'sqrt': math.sqrt,
                    'e': math.e,
                    'pi': math.pi
                }
                return eval(expressao_fonte, contexto)
            
            print("Parametros carregados com sucesso:")
            print(f"  Equacao: y'' = {expressao_fonte}")
            print(f"  Intervalo: [{limite_inferior}, {limite_superior}]")
            print(f"  Condicoes de contorno: y({limite_inferior}) = {condicao_inicial}, y({limite_superior}) = {condicao_final}")
            print(f"  Numero de subintervalos: {num_divisoes}")
            
            return (funcao_fonte, limite_inferior, limite_superior, 
                    condicao_inicial, condicao_final, num_divisoes)
                    
        except FileNotFoundError:
            print(f"Erro: Arquivo '{nome_arquivo}' nao encontrado")
            sys.exit(1)
        except ValueError as e:
            print(f"Erro no formato dos dados: {e}")
            sys.exit(1)
    
    def construir_malha_uniforme(self, inicio, fim, num_subintervalos):
        """
        Cria uma malha uniforme de pontos no intervalo [inicio, fim].
        
        Args:
            inicio: valor inicial do intervalo
            fim: valor final do intervalo
            num_subintervalos: número de subintervalos para dividir o intervalo
            
        Returns:
            vetor_x: array com os pontos da malha
            passo_h: tamanho do passo entre os pontos
        """
        passo_h = (fim - inicio) / num_subintervalos
        vetor_x = np.linspace(inicio, fim, num_subintervalos + 1)
        return vetor_x, passo_h
    
    def construir_sistema_linear(self, funcao_fonte, inicio, fim, 
                                 condicao_inicio, condicao_fim, num_subintervalos):
        """
        Constrói o sistema linear tridiagonal resultante da discretização.
        
        Args:
            funcao_fonte: função f(x, y) do termo fonte
            inicio: início do intervalo
            fim: fim do intervalo
            condicao_inicio: valor de y no início (y(a))
            condicao_fim: valor de y no fim (y(b))
            num_subintervalos: número de subintervalos
            
        Returns:
            matriz_A: matriz tridiagonal do sistema
            vetor_B: vetor do lado direito
            vetor_x: pontos da malha
            passo_h: tamanho do passo
        """
        # Cria a malha uniforme
        vetor_x, passo_h = self.construir_malha_uniforme(inicio, fim, num_subintervalos)
        
        # Número de pontos internos (sem incluir as extremidades)
        num_pontos_internos = num_subintervalos - 1
        
        # Inicializa a matriz A (tridiagonal) e o vetor B
        matriz_A = np.zeros((num_pontos_internos, num_pontos_internos))
        vetor_B = np.zeros(num_pontos_internos)
        
        # Preenche a matriz A e o vetor B
        for indice in range(num_pontos_internos):
            # Ponto x correspondente (ponto interno)
            x_atual = inicio + (indice + 1) * passo_h
            
            # Diagonal principal: -2
            matriz_A[indice, indice] = -2.0
            
            # Diagonal inferior (exceto para o primeiro ponto interno)
            if indice > 0:
                matriz_A[indice, indice - 1] = 1.0
            
            # Diagonal superior (exceto para o último ponto interno)
            if indice < num_pontos_internos - 1:
                matriz_A[indice, indice + 1] = 1.0
            
            # Estimativa inicial para y no ponto atual (interpolação linear)
            y_estimado = condicao_inicio + (indice + 1) * (condicao_fim - condicao_inicio) / num_subintervalos
            
            # Calcula o termo do lado direito
            vetor_B[indice] = passo_h**2 * funcao_fonte(x_atual, y_estimado)
        
        # Ajusta o vetor B para incluir as condições de contorno
        # O primeiro ponto interno é afetado por y(a)
        vetor_B[0] -= condicao_inicio
        
        # O último ponto interno é afetado por y(b)
        vetor_B[-1] -= condicao_fim
        
        return matriz_A, vetor_B, vetor_x, passo_h
    
    def resolver_sistema_tridiagonal(self, matriz_A, vetor_B):
        """
        Resolve o sistema linear tridiagonal usando um método direto.
        
        Args:
            matriz_A: matriz tridiagonal do sistema
            vetor_B: vetor do lado direito
            
        Returns:
            vetor_solucao: solução do sistema linear
        """
        # Verifica se a matriz é quadrada
        if matriz_A.shape[0] != matriz_A.shape[1]:
            raise ValueError("A matriz A deve ser quadrada")
        
        # Verifica se as dimensões são compatíveis
        if matriz_A.shape[0] != vetor_B.shape[0]:
            raise ValueError("Dimensoes incompatíveis entre matriz A e vetor B")
        
        # Resolve o sistema linear usando a biblioteca NumPy
        vetor_solucao = np.linalg.solve(matriz_A, vetor_B)
        
        return vetor_solucao
    
    def executar(self, funcao_fonte, inicio, fim, condicao_inicio, condicao_fim, num_subintervalos):
        """
        Executa o método das diferenças finitas para o problema fornecido.
        
        Args:
            funcao_fonte: função f(x, y) do termo fonte
            inicio: início do intervalo
            fim: fim do intervalo
            condicao_inicio: valor de y no início (y(a))
            condicao_fim: valor de y no fim (y(b))
            num_subintervalos: número de subintervalos
            
        Returns:
            pontos_x: array com os pontos x da solução
            pontos_y: array com os valores y da solução
        """
        print("Construindo sistema linear a partir da discretizacao...")
        
        # Constrói o sistema linear
        matriz_A, vetor_B, pontos_x, passo_h = self.construir_sistema_linear(
            funcao_fonte, inicio, fim, condicao_inicio, condicao_fim, num_subintervalos
        )
        
        print(f"Matriz do sistema: {matriz_A.shape[0]}x{matriz_A.shape[1]}")
        print(f"Numero de pontos internos: {matriz_A.shape[0]}")
        
        # Resolve o sistema linear
        print("Resolvendo sistema linear...")
        solucao_interna = self.resolver_sistema_tridiagonal(matriz_A, vetor_B)
        
        # Combina a solução interna com as condições de contorno
        pontos_y = np.concatenate([[condicao_inicio], solucao_interna, [condicao_fim]])
        
        # Armazena os resultados
        self.pontos_x = pontos_x
        self.pontos_y = pontos_y
        self.tamanho_passo = passo_h
        self.num_subintervalos = num_subintervalos
        
        print("Metodo das diferencas finitas concluido com sucesso")
        return pontos_x, pontos_y
    
    def salvar_resultados(self, nome_arquivo="saida.txt"):
        """
        Salva os resultados no arquivo de saída no formato especificado.
        
        Args:
            nome_arquivo: nome do arquivo de saída
        """
        if self.pontos_x is None or self.pontos_y is None:
            print("Erro: Nenhum resultado para salvar")
            return
        
        try:
            with open(nome_arquivo, 'w') as arquivo:
                arquivo.write("Metodo: Diferencas Finitas\n")
                
                for x, y in zip(self.pontos_x, self.pontos_y):
                    linha = f"x = {x:.6f}, y = {y:.6f}\n"
                    arquivo.write(linha)
            
            print(f"Resultados salvos no arquivo '{nome_arquivo}'")
            print(f"Total de pontos salvos: {len(self.pontos_x)}")
            
        except IOError as e:
            print(f"Erro ao salvar resultados: {e}")
            sys.exit(1)
    
    def exibir_resumo(self):
        """
        Exibe um resumo dos resultados obtidos.
        """
        if self.pontos_x is None or self.pontos_y is None:
            print("Nenhum resultado disponivel para exibir")
            return
        
        print("\n" + "="*60)
        print("RESUMO DO METODO DAS DIFERENCAS FINITAS")
        print("="*60)
        
        print(f"\nParametros da discretizacao:")
        print(f"  Numero de subintervalos: {self.num_subintervalos}")
        print(f"  Tamanho do passo (h): {self.tamanho_passo:.6f}")
        print(f"  Numero total de pontos: {len(self.pontos_x)}")
        
        print(f"\nCondicoes de contorno:")
        print(f"  y({self.pontos_x[0]:.1f}) = {self.pontos_y[0]:.6f}")
        print(f"  y({self.pontos_x[-1]:.1f}) = {self.pontos_y[-1]:.6f}")
        
        print(f"\nPrimeiros pontos da solucao:")
        for i in range(min(3, len(self.pontos_x))):
            print(f"  x = {self.pontos_x[i]:.6f}, y = {self.pontos_y[i]:.6f}")
        
        if len(self.pontos_x) > 3:
            print(f"\nUltimos pontos da solucao:")
            for i in range(max(0, len(self.pontos_x)-3), len(self.pontos_x)):
                print(f"  x = {self.pontos_x[i]:.6f}, y = {self.pontos_y[i]:.6f}")
        
        print(f"\nEstatisticas:")
        print(f"  Valor minimo de y: {np.min(self.pontos_y):.6f}")
        print(f"  Valor maximo de y: {np.max(self.pontos_y):.6f}")
        print(f"  Media dos valores de y: {np.mean(self.pontos_y):.6f}")
        
        print("="*60)


def main():
    """
    Função principal do programa.
    """
    print("="*60)
    print("IMPLEMENTACAO DO METODO DAS DIFERENCAS FINITAS")
    print("Para problemas de valor de contorno em EDOs de segunda ordem")
    print("="*60)
    
    # Cria uma instância do solucionador
    solucionador = SolucionadorDiferencasFinitas()
    
    # Etapa 1: Ler os parâmetros do arquivo de entrada
    print("\n[1/4] Carregando parametros do arquivo 'entrada.txt'...")
    (funcao_fonte, limite_inferior, limite_superior, 
     condicao_inicial, condicao_final, num_subintervalos) = solucionador.ler_parametros_entrada()
    
    # Etapa 2: Executar o método das diferenças finitas
    print("\n[2/4] Executando metodo das diferencas finitas...")
    solucionador.executar(funcao_fonte, limite_inferior, limite_superior, 
                          condicao_inicial, condicao_final, num_subintervalos)
    
    # Etapa 3: Salvar os resultados no arquivo de saída
    print("\n[3/4] Salvando resultados no arquivo 'saida.txt'...")
    solucionador.salvar_resultados()
    
    # Etapa 4: Exibir um resumo dos resultados
    print("\n[4/4] Gerando resumo dos resultados...")
    solucionador.exibir_resumo()
    
    # Opção para visualizar todos os pontos
    try:
        resposta = input("\nDeseja visualizar todos os pontos? (s/n): ").lower().strip()
        if resposta == 's':
            print("\nTodos os pontos calculados:")
            print("-" * 50)
            for i, (x, y) in enumerate(zip(solucionador.pontos_x, solucionador.pontos_y)):
                # Mostra em grupos de 10 para facilitar a visualização
                if i % 10 == 0 and i > 0:
                    input("\nPressione Enter para continuar...")
                    print("\n" + "-" * 50)
                print(f"Ponto {i:3d}: x = {x:8.3f}, y = {y:12.6f}")
    except KeyboardInterrupt:
        print("\nVisualizacao interrompida pelo usuario")
    
    print("\n" + "="*60)
    print("Execucao concluida com sucesso!")
    print("="*60)


if __name__ == "__main__":
    main()
