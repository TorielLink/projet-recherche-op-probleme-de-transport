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


def generate_trace_file(
    group, team, problem_number, method,
    couts, P, C, solution, total_cost,
    steps_output=None
):
    """
    Génère un fichier de trace.

    method ∈ {"no", "bh", "mp_no", "mp_bh"}
    steps_output : texte des étapes du Marche-Pied (optionnel)
    """

    os.makedirs("Traces", exist_ok=True)

    filename = f"Traces/{group}-{team}-trace{problem_number}-{method}.txt"

    input_table_str = table_to_string(couts, P, C)
    solution_table_str = table_to_string(solution, P, C)

    method_label = (
        "Nord-Ouest" if method == "no" else
        "Balas-Hammer" if method == "bh" else
        "Nord-Ouest + Marche-Pied" if method == "mp_no" else
        "Balas-Hammer + Marche-Pied"
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Groupe : {group}\n")
        f.write(f"Équipe : {team}\n")
        f.write(f"Problème : {problem_number}\n")
        f.write(f"Méthode : {method_label}\n\n")

        f.write("=== Problème initial ===\n")
        f.write(input_table_str + "\n")

        if steps_output:
            f.write("=== Étapes de l’optimisation (Marche-Pied) ===\n")
            f.write(steps_output + "\n")

        f.write("=== Solution finale ===\n")
        f.write(solution_table_str + "\n")

        cout_formatte = format(total_cost, ",").replace(",", " ")
        f.write(f"Coût total : {cout_formatte}\n")

    print(f"Trace générée : {filename}")
