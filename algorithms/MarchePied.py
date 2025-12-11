def get_costs(arcs, couts, index_prov_arbitraire, display):
    n = len(couts)
    m = len(couts[0])

    E_prov = [None] * n
    E_com = [None] * m
    E_prov[index_prov_arbitraire] = 0
    print(f"\nOn fixe de façon arbitraire E(P{index_prov_arbitraire+1}) = 0")

    changed = True
    while changed:
        changed = False
        for (i, j) in arcs:
            if E_prov[i] is None and E_com[j] is not None:
                if display:
                    val_signe = f"+ ({E_com[j]})" if E_com[j] < 0 else f"+ {E_com[j]}"
                    print(f"E(P{i+1}) - E(C{j+1}) = {couts[i][j]} => E(P{i+1}) = {couts[i][j]} {val_signe} = {couts[i][j] + E_com[j]}")
                E_prov[i] = couts[i][j] + E_com[j]
                changed = True
            if E_com[j] is None and E_prov[i] is not None:
                if display:
                    val_signe = f"- ({couts[i][j]})" if couts[i][j] < 0 else f"- {couts[i][j]}"
                    print(f"E(P{i+1}) - E(C{j+1}) = {couts[i][j]} => E(C{j+1}) = {E_prov[i]} {val_signe}  = {E_prov[i] - couts[i][j]}")
                E_com[j] = E_prov[i] - couts[i][j]
                changed = True

    Couts_pot = [[E_prov[i] - E_com[j] for j in range(m)] for i in range(n)]
    Couts_mar = [[couts[i][j] - Couts_pot[i][j] for j in range(m)] for i in range(n)]

    if display:
        print()
        for i in range(len(E_prov)):
            print(f"E(P{i+1}) = {E_prov[i]}")
        for i in range(len(E_com)):
            print(f"E(C{i+1}) = {E_com[i]}")

    return Couts_pot, Couts_mar, E_prov, E_com

def lowest_cout_mar(Couts_mar):
    min_value = float('inf')
    min_pos = None
    for i in range(len(Couts_mar)):
        for j in range(len(Couts_mar[0])):
            if Couts_mar[i][j] < min_value:
                min_value = Couts_mar[i][j]
                min_pos = (i, j)
    if min_value > 0:
        return 0
    return min_pos