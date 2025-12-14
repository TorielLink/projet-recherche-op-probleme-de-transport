import os
import shutil
from contextlib import redirect_stdout
from io import StringIO

from algorithms.balas_hammer import compute_balas_hammer_solution
from algorithms.northwest_corner import compute_northwest_solution
from algorithms.stepping_stone import solve_stepping_stone
from utils.io.table_reader import read_table_file
from utils.io.trace_writer import generate_trace_file
from utils.math.cost import compute_total_cost

GROUP = "NEW3"
TEAM = "5"
TABLEAU_DIR = "Tableaux"


def clean_trace_folder():
    """
    Supprime et recrée le dossier des traces.

    Principe :
        - Supprime le dossier Traces s’il existe
        - Crée un dossier Traces vide
    """
    if os.path.exists("Traces"):
        shutil.rmtree("Traces")
    os.makedirs("Traces")


def generate_all_traces():
    """
    Génère toutes les traces pour les problèmes fournis.

    Principe :
        - Lit chaque tableau de test
        - Calcule les solutions Nord-Ouest et Balas-Hammer
        - Applique le Marche-Pied avec affichage des étapes
        - Génère un fichier de trace pour chaque méthode
    """
    clean_trace_folder()

    for problem_number in range(1, 13):
        filename = f"{TABLEAU_DIR}/tableau{problem_number}.txt"
        couts, P, C = read_table_file(filename)

        original_couts = [row.copy() for row in couts]
        original_P = P.copy()
        original_C = C.copy()

        # Nord-Ouest
        sol_no = compute_northwest_solution(
            original_P.copy(),
            original_C.copy()
        )
        cost_no = compute_total_cost(original_couts, sol_no)

        generate_trace_file(
            GROUP, TEAM, problem_number, "no",
            original_couts, original_P, original_C,
            sol_no, cost_no
        )

        # Nord-Ouest + Marche-Pied (avec étapes)
        buffer = StringIO()
        with redirect_stdout(buffer):
            sol_mp_no = solve_stepping_stone(
                sol_no,
                original_couts,
                original_P,
                original_C,
                display=True
            )
        steps_no = buffer.getvalue()
        cost_mp_no = compute_total_cost(original_couts, sol_mp_no)

        generate_trace_file(
            GROUP, TEAM, problem_number, "mp_no",
            original_couts, original_P, original_C,
            sol_mp_no, cost_mp_no,
            steps_output=steps_no
        )

        # Balas-Hammer
        sol_bh = compute_balas_hammer_solution(
            original_couts,
            original_P.copy(),
            original_C.copy(),
            display=False
        )
        cost_bh = compute_total_cost(original_couts, sol_bh)

        generate_trace_file(
            GROUP, TEAM, problem_number, "bh",
            original_couts, original_P, original_C,
            sol_bh, cost_bh
        )

        # Balas-Hammer + Marche-Pied (avec étapes)
        buffer = StringIO()
        with redirect_stdout(buffer):
            sol_mp_bh = solve_stepping_stone(
                sol_bh,
                original_couts,
                original_P,
                original_C,
                display=True
            )
        steps_bh = buffer.getvalue()
        cost_mp_bh = compute_total_cost(original_couts, sol_mp_bh)

        generate_trace_file(
            GROUP, TEAM, problem_number, "mp_bh",
            original_couts, original_P, original_C,
            sol_mp_bh, cost_mp_bh,
            steps_output=steps_bh
        )


if __name__ == "__main__":
    generate_all_traces()
