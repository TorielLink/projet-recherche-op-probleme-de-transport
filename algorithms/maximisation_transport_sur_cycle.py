def maximiser_transport_sur_cycle(solution, cycle):
    # 
    # Maximise le transport sur un cycle en alternant ajout/retrait.
    
    # Args:
    #     solution: Matrice de transport [n × m]
    #     cycle: Liste des sommets du cycle retournée par la fonction bfs_detect_cycle (ex: ['P0', 'C1', 'P2', 'C0'])
    
    # Returns:
    #     (solution, delta, aretes_supprimees)
    # 
    aretes = []
    delta = float('inf')
    
    for k in range(len(cycle)):
        s1 = cycle[k]
        s2 = cycle[(k + 1) % len(cycle)]
        
        if s1[0] == 'P':
            i, j = int(s1[1:]), int(s2[1:])
        else:
            i, j = int(s2[1:]), int(s1[1:])
        
        signe = 1 if k % 2 == 0 else -1
        aretes.append((i, j, signe, s1, s2))
        
        if signe == -1:
            delta = min(delta, solution[i][j])
    
    # =====================================================
    # AFFICHAGE DES CONDITIONS POUR CHAQUE CASE
    # =====================================================
    print("\n=== Maximisation du transport sur le cycle ===")
    print(f"Cycle : {' -> '.join(cycle)} -> {cycle[0]}")
    print("\nConditions pour chaque case :")
    
    for i, j, signe, s1, s2 in aretes:
        action = "+ δ" if signe == 1 else "- δ"
        print(f"  ({s1}, {s2}) : {solution[i][j]:>4} {action}")
    
    print(f"\nδ = {delta}")
    
    if delta == 0 or delta == float('inf'):
        print("Aucune modification (δ = 0)")
        return solution, 0, []
    
    # Application du transfert
    aretes_supprimees = []
    for i, j, signe, s1, s2 in aretes:
        solution[i][j] += signe * delta
        if signe == -1 and solution[i][j] == 0:
            aretes_supprimees.append((i, j))
    
    # =====================================================
    # AFFICHAGE DES ARÊTES SUPPRIMÉES
    # =====================================================
    if aretes_supprimees:
        print("\nArête(s) supprimée(s) :")
        for i, j in aretes_supprimees:
            print(f"  (P{i}, C{j})")
    else:
        print("\nAucune arête supprimée.")
    
    return solution, delta, aretes_supprimees
