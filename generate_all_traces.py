import os
import shutil
from io import StringIO
from contextlib import redirect_stdout

from utils.reader import read_table_file
from utils.trace_generator import generate_trace_file
from algorithms.northwest import northwest_solution, cout_total
from algorithms.BalasHammer import balas_hammer
from algorithms.MarchePied import marche_pied_complet


GROUP = "NEW3"
TEAM = "5"
TABLEAU_DIR = "Tableaux"


def clean_trace_folder():
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

        # ==================================================
        # Nord-Ouest
        # ==================================================
        sol_no = northwest_solution(original_P.copy(), original_C.copy())
        cost_no = cout_total(original_couts, sol_no)

        generate_trace_file(
            GROUP, TEAM, problem_number, "no",
            original_couts, original_P, original_C,
            sol_no, cost_no
        )

        # ==================================================
        # Nord-Ouest + Marche-Pied (avec étapes)
        # ==================================================
        buffer = StringIO()
        with redirect_stdout(buffer):
            sol_mp_no = marche_pied_complet(
                sol_no,
                original_couts,
                original_P,
                original_C,
                display=True
            )
        steps_no = buffer.getvalue()
        cost_mp_no = cout_total(original_couts, sol_mp_no)

        generate_trace_file(
            GROUP, TEAM, problem_number, "mp_no",
            original_couts, original_P, original_C,
            sol_mp_no, cost_mp_no,
            steps_output=steps_no
        )

        # ==================================================
        # Balas-Hammer
        # ==================================================
        sol_bh = balas_hammer(
            original_couts,
            original_P.copy(),
            original_C.copy()
        )
        cost_bh = cout_total(original_couts, sol_bh)

        generate_trace_file(
            GROUP, TEAM, problem_number, "bh",
            original_couts, original_P, original_C,
            sol_bh, cost_bh
        )

        # ==================================================
        # Balas-Hammer + Marche-Pied (avec étapes)
        # ==================================================
        buffer = StringIO()
        with redirect_stdout(buffer):
            sol_mp_bh = marche_pied_complet(
                sol_bh,
                original_couts,
                original_P,
                original_C,
                display=True
            )
        steps_bh = buffer.getvalue()
        cost_mp_bh = cout_total(original_couts, sol_mp_bh)

        generate_trace_file(
            GROUP, TEAM, problem_number, "mp_bh",
            original_couts, original_P, original_C,
            sol_mp_bh, cost_mp_bh,
            steps_output=steps_bh
        )


if __name__ == "__main__":
    generate_all_traces()
