import os
from io import StringIO
from contextlib import redirect_stdout
from utils.display import DisplayTable


def table_to_string(couts, P, C):
    """
    Génère une représentation textuelle d'un tableau de transport.
    """
    dt = DisplayTable.DonneesTest(couts, P, C)
    table = DisplayTable()

    buffer = StringIO()
    with redirect_stdout(buffer):
        table.afficher_table(dt)

    return buffer.getvalue()


def generate_trace_file(group, team, problem_number, method,
                        couts, P, C, solution, total_cost):
    """
    Génère les fichiers de trace
    method ∈ {"no", "bh"}.
    """

    os.makedirs("Traces", exist_ok=True)

    filename = f"Traces/{group}-{team}-trace{problem_number}-{method}.txt"

    # Tableau d'affichage
    input_table_str = table_to_string(couts, P, C)
    solution_table_str = table_to_string(solution, P, C)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Groupe : {group}\n")
        f.write(f"Équipe : {team}\n")
        f.write(f"Problème : {problem_number}\n")
        method_label = (
                ('Nord-Ouest' if method in ('no', 'mp_no') else
                 'Balas-Hammer' if method in ('bh', 'mp_bh') else method)
                + (' avec Marche-Pied' if method.startswith('mp_') else '')
        )
        f.write(f"Méthode : {method_label}\n\n")

        f.write("=== Problème initial ===\n")
        f.write(input_table_str + "\n")

        f.write("=== Solution proposée ===\n")
        f.write(solution_table_str + "\n")

        f.write(f"Coût total : {total_cost}\n")

    print(f"Trace générée : {filename}")
