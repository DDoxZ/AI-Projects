# Trabalho 4 IIA 2024/2025
# Grupo 77
# 59886 - Pedro Silva
# 60447 - Diogo Lopes


from csp_v3 import *

def csp_possivel_solucao(caixas,goals_alcancaveis):
    """
    Retorna um objeto da classe CSP inicializado com as variáveis, os domínios,
    os vizinhos e restrições do problema de coloracao de mapas associado ao problema
    do Sokoban onde o objetivo é uma possível atribuição de caixas a objetivos, ou
    None caso seja impossível arrumar todas as caixas nos objectivos
    """

    # Definir variáveis
    # variables: Lista de variáveis (strings ou inteiros)
    # As células são as variáveis (as regiões num mapa)
    variaveis = caixas

    # Definir domínios
    # domains: Dicionário com elementos do tipo {var:[valor, ...]}
    # Os domínios são dados pela lista de goals alcançáveis pelas respectivas células (as cores para colorir o mapa)
    dominios = {var: goals_alcancaveis[var] for var in variaveis}

    # Definir vizinhos
    # neighbors: Dicionário com elementos do tipo {var:[var,...]} em que cada variável var (chave) tem como valor
    # uma lista das variáveis com as quais tem restrições (vizinhos no grafo de restrições), que define o grafo de restrições
    # Duas células são vizinhas se partilharem algum dos goals (se forem regiões contíguas)
    vizinhos = {}
    for var in variaveis:
        for var2 in variaveis:
            if var != var2:
                if set(dominios[var]).intersection(dominios[var2]) != set():
                    if var not in vizinhos:
                        vizinhos[var] = []
                    vizinhos[var].append(var2)

    # Definir restrições
    # constraints: Função do tipo f(A, a, B, b) que devolve True se os vizinhos A e B satisfazem a restrição quando têm valores A=a e B=b
    # Duas células vizinhas não podem ter o mesmo valor (duas regiões contíguas não podem ter a mesma cor)
    # Podemos usar o different_values_constraint que é precisamente o que precisamos
    # Retornar o CSP com as variáveis, domínios, vizinhos e restrições
    return CSP(variaveis, dominios, vizinhos, different_values_constraint)


def csp_find_alcancaveis_1goal(s,goal):
    """
    Retorna um objeto da classe CSP inicializado com as variáveis, os domínios,
    os vizinhos e restrições associado ao problema do Sokoban onde o objetivo é
    para cada celula navegavel verificar se seria possivel a partir desta celula
    empurrar a caixa para o objetivo, retornando 0 se for possivel e 1 caso contrario
    """

    def can_push_box_from_A_to_B(A, B):
        """
        Verifica se é possível empurrar uma caixa de A para B
        """
        x1, y1 = A
        x2, y2 = B

        # A e B devem ser adjacentes
        if abs(x1 - x2) + abs(y1 - y2) != 1:
            return False

        # B deve ser navegável e não conter ma parede
        if B in s.paredes:
            return False

        # A celula oposta a A relativamente a B deve ser navegável para o jogador se posicionar
        dx = x1 - x2
        dy = y1 - y2
        player_pos = (x1 + dx, y1 + dy)
        if player_pos in s.paredes or player_pos not in s.navegaveis:
            return False

        return True

    def canto(celula):
        """
        Função auxiliar que verifica se uma caixa está num canto
        Retorna True se sim, False caso contrário
        """
        l, c = celula

        # Verificar se a caixa está num canto
        if ((l, c + 1) in s.paredes and (l + 1, c) in s.paredes) or \
            ((l, c - 1) in s.paredes and (l + 1, c) in s.paredes) or \
            ((l, c + 1) in s.paredes and (l - 1, c) in s.paredes) or \
            ((l, c - 1) in s.paredes and (l - 1, c) in s.paredes):
            return True

        return False


    # Definir variáveis
    # variables: Lista de variáveis (strings ou inteiros)
    # As células são as variáveis
    variaveis = [coord for coord in s.navegaveis]

    # Definir domínios
    # domains: Dicionário com elementos do tipo {var:[valor, ...]}
    # Os domínios são a possibilidade (1) ou não (0) de uma caixa partir da célula e chegar ao goal
    dominios = {celula: [0] if canto(celula) else [1,0] for celula in variaveis}
    dominios[goal] = [1]  # O goal é sempre alcançável

    # Definir vizinhos
    # neighbors: Dicionário com elementos do tipo {var:[var,...]} em que cada variável var (chave) tem como valor
    # uma lista das variáveis com as quais tem restrições (vizinhos no grafo de restrições), que define o grafo de restrições
    # Duas células são vizinhas se forem adjacentes (na vertical ou horizontal) e se for possível empurrar uma caixa de uma para a outra,
    # num dos sentidos ou nos dois. Se forem adjacentes, mas se nenhuma caixa pode ser empurrada de uma para a outra, então não são vizinhas.
    vizinhos = {}
    for var in variaveis:
        vizinhos[var] = []
        for var2 in variaveis:
            if var != var2 and (can_push_box_from_A_to_B(var, var2) or can_push_box_from_A_to_B(var2, var)):
                vizinhos[var].append(var2)

    # Definir restrições
    # constraints: Função do tipo f(A, a, B, b) que devolve True se os vizinhos A e B satisfazem a restrição quando têm valores A=a e B=b
    # As restrições, tantos as unárias como as binárias, ficam por vossa conta!
    def restricao(A, a, B, b):
        """
        Se for possível empurrar uma caixa de A para B,
        então se uma caixa em B pode alcançar o goal (b == 1),
        então uma caixa em A também deve poder (a == 1).
        """
        if can_push_box_from_A_to_B(A, B):
            if a == 0 and b == 1:
                return False

        if can_push_box_from_A_to_B(B, A):
            if a == 1 and b == 0:
                return False

        return A != B

    # Retornar o CSP com as variáveis, domínios, vizinhos e restrições
    return CSP(variaveis, dominios, vizinhos, restricao)


def find_alcancaveis_all_goals(s):
    """
    Retorna um dicionário com as células navegáveis como chaves e uma lista de posições de goals
    como valores, representando a possibilidade de uma caixa partir da célula e chegar
    a cada um dos goals
    """

    sorted_goals = sorted(list(s.goal))
    result_alcancaveis = {}

    for goal in sorted_goals:
        r = find_alcancaveis_1goal(s, goal)

        for var in r:
            if r[var] == 1:
                if var in result_alcancaveis:
                    result_alcancaveis[var].append(goal)
                else:
                    result_alcancaveis[var] = [goal]
            else:
                if var not in result_alcancaveis:
                    result_alcancaveis[var] = []

    return result_alcancaveis


def possivel_solucao(caixas, goals_alcancaveis):
    csp_sokoban1 = csp_possivel_solucao(caixas, goals_alcancaveis)  # <--- a vossa função csp_possivel_solucao
    r = backtracking_search(csp_sokoban1, inference=forward_checking)
    return r


def find_alcancaveis_1goal(s, goal):
    csp_sokoban2 = csp_find_alcancaveis_1goal(s, goal)  # <--- a vossa função csp_find_alcancaveis_1goal
    r = backtracking_search(csp_sokoban2, order_domain_values=number_ascending_order, inference=forward_checking)
    return {} if r == None else r
