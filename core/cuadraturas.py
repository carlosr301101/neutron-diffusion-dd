
# =================================================================
DATA = {
    'N': [2, 4, 4, 8, 8, 8, 8],
    'm': [1, 1, 2, 1, 2, 3, 4],
    'mu_m': [
        0.577350269189626,  # N=2, m=1
        0.861136311594053,  # N=4, m=1
        0.339981043584856,  # N=4, m=2
        0.960289856497536,  # N=8, m=1
        0.796666477413627,  # N=8, m=2
        0.525532409916329,  # N=8, m=3
        0.183434642495650   # N=8, m=4
    ],
    'omega_m': [
        1.0,               # N=2, m=1
        0.347854845137454, # N=4, m=1
        0.652145154862546, # N=4, m=2
        0.101228536290376, # N=8, m=1
        0.222381034453374, # N=8, m=2
        0.313706645877887, # N=8, m=3
        0.362683783378362  # N=8, m=4
    ]
}
# import pandas as pd
# dataframe= pd.DataFrame(DATA) 
# miu_m = dataframe.loc[(dataframe['N'] == 8), 'mu_m'].values
# omega_m = dataframe.loc[(dataframe['N'] == 4), 'omega_m'].values

# print(omega_m/miu_m)

import numpy as np

def algoritmo_dd_sn_si(NR, NZ, IZL, SCT, SCS, Q, HR, NC, NW, MU, W, EPSILON):
    """
    Implementação do Algoritmo DD (Método dos Ordens Discretas)
    unidimensional com iteração de fonte (SI).
    """

    # --- A) Dados de entrada são recebidos como argumentos da função ---
    
    # MU e W representam os mu_k (ordenadas discretas) e W_k (pesos)
    # A entrada NW é a Ordem da quadratura angular SN, NW = N/2.
    
    # --- B) Calcule: Tamanhos Totais ---
    
    # O total de células (NTC) e pontos (NTP) são calculados a partir de NC(J).
    NTC = sum(NC) # NTC = total de células
    NTP = NTC + 1 # NTP = total de pontos
    
    # --- C) Inicialize: Variáveis e Vetores de Fluxos ---
    
    # S(I) é a fonte de espalhamento
    S = np.zeros(NTC) # I=1:NTC
    
    # Fluxos Angulares (Forward e Backward)
    # FORTH(Ponto, Direção) e BACK(Ponto, Direção)
    FORTH = np.zeros((NTP, NW)) # J=1:NTP, I=1:NW
    BACK = np.zeros((NTP, NW))  # J=1:NTP, I=1:NW
    
    # HC(I) é a espessura das células por região
    HC = []
    for hr_j, nc_j in zip(HR, NC):
        # A notação no documento é HC(I) = HR(J) / NC(J) para I=1:NTC?
        # A interpretação mais comum é que HC é o tamanho da célula para a região J.
        hc_j = hr_j / nc_j
        HC.extend([hc_j] * nc_j)
    HC = np.array(HC)

    # Inicialização da Fonte de Espalhamento (S(I)=0) já foi feita
    
    # Início do loop de iteração (Iteração da Fonte - SI)
    MAX_ITER = 1000 # Número máximo de iterações
    iter_count = 0
    converged = False
    
    while not converged and iter_count < MAX_ITER:
        iter_count += 1
        S_old = S.copy() # Cópia de S para teste de convergência

        # --- D) Condições de Contorno (CC) ---
        # Implementar as CCs Prescritas, Reflexivas, etc., aqui.
        # Por exemplo, para CC Prescrita à esquerda:
        # FORTH[0, :] = valor_prescrito_esquerda # I=1:NW
        # Por exemplo, para CC Reflexiva à esquerda (seria atualizada no final do passo F)
        
        # --- E) Varredura para a Direita ($\mu_m > 0$) ---
        
        JF = 1 # Índice do ponto à direita da célula (J+1)
        JT_offset = 0 # Offset para o índice global da célula S(JT) e HC(JR)
        
        for JR in range(NR): # JR = 1:NR (Regiões)
            IZ = IZL[JR] # Zona Material
            XT = 0.5 * SCT[IZ] # 0.5 * Secção de choque total
            XC_J = HC[JT_offset] # Tamanho da célula para a região JR.
            F = Q[JR] # Fonte de espalhamento (com intensidade constante)
            GR = NC[JR] # Número de células na região JR
            
            for J in range(GR): # J = 1:GR (Células dentro da Região JR)
                JT = JF # JT é o índice do ponto à esquerda da célula (J)
                JF = JF + 1 # JF é o índice do ponto à direita (J+1)
                
                ESP = S[JT - 1] # Fonte de espalhamento para a célula atual (S(J))
                XC_c = HC[JT - 1] # Tamanho da célula atual
                
                for I in range(NW): # I = 1:NW (Direções $\mu_m > 0$)
                    OD = MU[I] / XC_c # $\mu_m / \Delta x_c$ (Odenada discreta / Espessura da Célula)
                    AUXT = FORTH[JT - 1, I] # Fluxo de entrada no ponto J
                    
                    NUM = (OD - XT) * AUXT + ESP + F
                    DEN = OD + XT
                    
                    FORTH[JF - 1, I] = NUM / DEN # Fluxo de saída no ponto J+1
            
            JT_offset += GR # Atualiza o offset para a próxima região
        
        # --- F) Varredura para a Esquerda ($\mu_m < 0$) ---
        
        JF = NTP # Índice do ponto à direita da célula (J+1)
        JT_offset = NTC - 1 # Offset para o índice global da célula S(JF)
        
        # Itera sobre as regiões de forma reversa (JR=NR:-1:1)
        for JR in range(NR - 1, -1, -1):
            IZ = IZL[JR] # Zona Material
            XT = 0.5 * SCT[IZ]
            XC_J = HC[JT_offset]
            F = Q[JR]
            GR = NC[JR]
            
            # Itera sobre as células de forma reversa (J=GR:-1:1)
            for J in range(GR - 1, -1, -1): 
                JT = JF # JT é o índice do ponto à direita (J+1)
                JF = JF - 1 # JF é o índice do ponto à esquerda (J)
                
                ESP = S[JF - 1] # Fonte de espalhamento para a célula atual (S(J))
                XC_c = HC[JF - 1] # Tamanho da célula atual
                
                for I in range(NW, 2 * NW): # I = NW+1:2*NW (Direções $\mu_m < 0$)
                    # Nota: O MU deve ter 2*NW elementos, onde MU[I] para I >= NW são negativos
                    OD = -MU[I] / XC_c # Usando |mu_m| / Delta_x_c
                    AUXT = BACK[JT - 1, I] # Fluxo de entrada no ponto J+1
                    
                    NUM = (OD - XT) * AUXT + ESP + F
                    DEN = OD + XT
                    
                    BACK[JF - 1, I] = NUM / DEN # Fluxo de saída no ponto J

            JT_offset -= GR # Atualiza o offset para a próxima região
            
        # Nota: As CCs Reflexivas devem ser aplicadas aqui, se necessário.
        # Ex: Reflexiva à esquerda: FORTH[0, I] = BACK[0, I] (para I=1:NW)
        # Ex: Reflexiva à direita: BACK[NTP-1, I] = FORTH[NTP-1, I] (para I=1:NW)

        # --- G) Fluxo Escalar Médio ($\bar{\phi}$) ---
        
        AVFLESCC = np.zeros(NTC) # Fluxo escalar médio na célula
        PESOW = W # Supõe que W é um vetor de 2*NW elementos ou que W_k = W_{k+NW}
        
        for J in range(NTC): # J = 1:NTC (Células)
            JF = J + 1 # JF é o ponto à direita (J+1)
            SOMA = 0
            
            # Varredura sobre todas as direções (ID = 1:2*NW)
            for ID in range(2 * NW): 
                # AUX1 e AUX2 são os fluxos angulares médios (FORWARD e BACKWARD) na célula
                AUX1 = 0.5 * (FORTH[JF, ID] + FORTH[J, ID]) # Fluxo angular médio na célula para $\mu_m > 0$
                AUX2 = 0.5 * (BACK[J, ID] + BACK[JF, ID]) # Fluxo angular médio na célula para $\mu_m < 0$
                
                # SOMA = SOMA + (AUX1 + AUX2) * PESO(ID)
                SOMA += (AUX1 + AUX2) * PESOW[ID] # SOMA = soma(phi_m * W_m)
            
            AVFLESCC[J] = SOMA # Média sobre a célula J
        
        # --- H) Atualização da Fonte de Espalhamento (SI) ---
        
        JS = 0 # Índice da célula
        
        for JR in range(NR): # JR = 1:NR (Regiões)
            IZ = IZL[JR] # Zona Material
            XS = 0.5 * SCS[IZ] # 0.5 * Secção de choque de espalhamento macroscópica total
            GR = NC[JR] # Número de células na região JR
            
            for JC in range(GR): # JC = 1:GR (Células na Região JR)
                JS = JS + 1 # Atualiza o índice global da célula
                
                # S(Js) = $\Sigma_s * \bar{\phi}$
                S[JS - 1] = XS * AVFLESCC[JS - 1] # Atualiza a fonte de espalhamento

        # --- Teste o critério de parada ---
        
        # Critério de convergência (ex: em norma L2)
        # Comparar S com S_old usando o EPSILON
        
        diff_norm = np.linalg.norm(S - S_old)
        if diff_norm < EPSILON:
            converged = True
            
        # O teste deve ser mais rigoroso para o fluxo escalar médio.
        # Por exemplo, se o fluxo escalar médio for o que converge:
        # diff_phi = np.linalg.norm(AVFLESCC - AVFLESCC_old) / np.linalg.norm(AVFLESCC)

        if converged:
            print(f"Convergência alcançada após {iter_count} iterações.")
        
    if not converged:
        print(f"Não houve convergência após o máximo de {MAX_ITER} iterações.")

    return AVFLESCC, FORTH, BACK

# O diagrama de fluxo do documento  mostra o processo iterativo do método.