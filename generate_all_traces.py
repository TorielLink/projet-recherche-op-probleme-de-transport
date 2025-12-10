import os
import shutil

from utils.reader import read_table_file
from utils.trace_generator import generate_trace_file
from algorithms.northwest import northwest_solution, cout_total
from algorithms.BalasHammer import balas_hammer


GROUP = "NEW3"
TEAM = "5"
TABLEAU_DIR = "Tableaux"


def clean_trace_folder():
    """Supprime tous les fichiers du dossier Traces/ avant régénération."""
    if os.path.exists("Traces"):
        shutil.rmtree("Traces")
    os.makedirs("Traces")


def generate_all_traces():
    clean_trace_folder()

    for problem_number in range(1, 13):

        filename = f"{TABLEAU_DIR}/tableau{problem_number}.txt"
        couts, P, C = read_table_file(filename)

        original_couts = [row.copy() for row in couts]
        original_P = P.copy()
        original_C = C.copy()

        # --------------------------------
        # Nord-Ouest
        # --------------------------------
        no_P = original_P.copy()
        no_C = original_C.copy()

        sol_no = northwest_solution(no_P, no_C)
        cost_no = cout_total(original_couts, sol_no)

        generate_trace_file(
            GROUP, TEAM, problem_number, "no",
            original_couts, original_P, original_C,
            sol_no, cost_no
        )

        # --------------------------------
        # Balas-Hammer
        # --------------------------------
        bh_P = original_P.copy()
        bh_C = original_C.copy()

        sol_bh = balas_hammer(original_couts, bh_P, bh_C)
        cost_bh = cout_total(original_couts, sol_bh)

        generate_trace_file(
            GROUP, TEAM, problem_number, "bh",
            original_couts, original_P, original_C,
            sol_bh, cost_bh
        )


if __name__ == "__main__":
    generate_all_traces()
