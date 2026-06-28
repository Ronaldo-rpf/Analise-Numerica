def simular_covid_seiahr():
    # Parâmetros do modelo
    chi = 0.6    # Fração de quarentenados
    alpha = 0.33 # Taxa de incubação
    p = 0.75     # Fração de assintomáticos
    delta = 0.1  # Taxa de recuperação
    phi = 0.01   # Taxa de hospitalização
    mu = 0.03    # Taxa de mortalidade
    beta = 0.5   # Taxa de transmissão
    rho = 0.1    # Taxa de recuperação hospitalar (Assumido)
    N = 400000.0 # População Total (Correção do Modelo)

    # Condições iniciais
    S = 400000.0
    E = 0.0
    I = 1.0      # Único infectado inicial
    A = 0.0
    H = 0.0
    R = 0.0
    D = 0.0      # Óbitos (Variável para responder ao professor)

    dias = 50
    h = 1.0      # Passo de 1 dia

    # Função que retorna as derivadas simultâneas
    def derivadas(S, E, I, A, H, R, D):
        # A CORREÇÃO ESTÁ AQUI: dividindo por N
        lambd = beta * (I + A) / N
        
        dS = -lambd * ((1 - chi) * S)
        dE = lambd * ((1 - chi) * S) - alpha * E
        dI = (1 - p) * alpha * E - delta * I
        dA = p * alpha * E - delta * A
        dH = phi * delta * I - (rho + mu) * H
        dR = (1 - phi) * delta * I + rho * H + delta * A
        dD = mu * H
        
        return dS, dE, dI, dA, dH, dR, dD

    print(f"{'Dia':<5} | {'Suscetiveis':<12} | {'Expostos':<10} | {'Infectados':<10} | {'Hospitalizados':<14} | {'Obitos':<10}")
    print("-" * 75)

    # Laço do RK4
    for t in range(dias + 1):
        if t % 5 == 0 or t == dias:  # Imprime a cada 5 dias e no último dia
            print(f"{t:<5} | {S:<12.1f} | {E:<10.1f} | {I:<10.1f} | {H:<14.2f} | {D:<10.2f}")

        # k1
        dS1, dE1, dI1, dA1, dH1, dR1, dD1 = derivadas(S, E, I, A, H, R, D)
        
        # k2
        dS2, dE2, dI2, dA2, dH2, dR2, dD2 = derivadas(
            S + 0.5*h*dS1, E + 0.5*h*dE1, I + 0.5*h*dI1, 
            A + 0.5*h*dA1, H + 0.5*h*dH1, R + 0.5*h*dR1, D + 0.5*h*dD1
        )
        
        # k3
        dS3, dE3, dI3, dA3, dH3, dR3, dD3 = derivadas(
            S + 0.5*h*dS2, E + 0.5*h*dE2, I + 0.5*h*dI2, 
            A + 0.5*h*dA2, H + 0.5*h*dH2, R + 0.5*h*dR2, D + 0.5*h*dD2
        )
        
        # k4
        dS4, dE4, dI4, dA4, dH4, dR4, dD4 = derivadas(
            S + h*dS3, E + h*dE3, I + h*dI3, 
            A + h*dA3, H + h*dH3, R + h*dR3, D + h*dD3
        )
        
        # Atualização (Passo)
        S += (h/6.0) * (dS1 + 2*dS2 + 2*dS3 + dS4)
        E += (h/6.0) * (dE1 + 2*dE2 + 2*dE3 + dE4)
        I += (h/6.0) * (dI1 + 2*dI2 + 2*dI3 + dI4)
        A += (h/6.0) * (dA1 + 2*dA2 + 2*dA3 + dA4)
        H += (h/6.0) * (dH1 + 2*dH2 + 2*dH3 + dH4)
        R += (h/6.0) * (dR1 + 2*dR2 + 2*dR3 + dR4)
        D += (h/6.0) * (dD1 + 2*dD2 + 2*dD3 + dD4)

simular_covid_seiahr()

