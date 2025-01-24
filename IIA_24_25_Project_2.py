# Projeto 2 IIA 2024/2025
# Grupo 77
# 59886 - Pedro Silva
# 60447 - Diogo Lopes

def h_util(self, node):
    """Para cada objetivo (lugar de armazenamento), calcula a distância de Manhattan à caixa mais próxima
    que ainda não foi alocada, ignorando a existência de paredes e/ou obstáculos, e aloca essa caixa ao objetivo.
    O valor da heurística é a soma todas estas distâncias + a distância entre o sokoban e a caixa mais longínqua
    que ainda não está arrumada. Se estamos num estado final, devolve 0."""
    clone=copy.deepcopy(node.state)

    if self.goal_test(clone):
        return 0

    sokoban = clone['sokoban']
    caixas_disponiveis = clone['caixas'].copy()
    objetivos = self.goal

    distancias_sum = 0
    for objetivo in objetivos:
        if not caixas_disponiveis:
            break

        caixa_mais_proxima = min(caixas_disponiveis, key=lambda caixa: manhattan(objetivo, caixa))
        distancias_sum += manhattan(objetivo, caixa_mais_proxima)
        caixas_disponiveis.remove(caixa_mais_proxima)

    caixas_por_arrumar = [caixa for caixa in clone['caixas'] if caixa not in objetivos]
    distancia_longinqua = max([manhattan(sokoban, caixa) for caixa in caixas_por_arrumar])

    return distancias_sum + distancia_longinqua

def beam_search_plus_count(problem, W, f):
    """Beam Search: search the nodes with the best W scores in each depth.
    Return the solution and how many nodes were expanded."""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    
    if problem.goal_test(node.state):
        return node, 0
    
    parents = PriorityQueue(min, f)
    children = PriorityQueue(min, f)
    parents.append(node)

    explored = set()
    visited = {node.state}
    
    while parents or children:
        if parents:
            node = parents.pop()
            if problem.goal_test(node.state):
                return node, len(explored)
            explored.add(node.state)
            visited.remove(node.state)
            for child in node.expand(problem):
                if child.state not in explored and child.state not in visited:
                    children.append(child)
                    visited.add(child.state)
                elif child.state in visited:
                    if child in parents:
                        incumbent = parents[child]
                        if f(child) < f(incumbent):
                            del parents[incumbent]
                            children.append(child)
  
        else:
            visited.clear()
            for _ in range(min(W, len(children))):
                c = children.pop()
                parents.append(c)
                visited.add(c.state)
            
            while children:
                children.pop()
    
    return None, len(explored)

def IW_beam_search(problem, h):
    """IW_beam_search (Iterative Widening Beam Search) começa com beam width W=1 e aumenta W iterativamente até
    se obter uma solução. Devolve a solução, o W com que se encontrou a solução, e o número total (acumulado desde W=1)
    de nós expandidos. Assume-se que existe uma solução."""
    W = 1
    total_nodes = 0
    while True:
        solution, nodes_number = beam_search(problem, W, h)
        total_nodes += nodes_number
        if solution:
            return solution, W, total_nodes
        W += 1
