from utils.ramdom_problem import generate_random_transport_problem
from utils.time_test_fonction import (
    measure_time_nord_ouest,
    measure_time_balas_hammer,
    measure_time_marche_pied_from_NO,
    measure_time_marche_pied_from_BH,
)


# ---------------------------------------------------------------------
# test du temps des algorithmes de taille n
# ---------------------------------------------------------------------
def benchmark(n_values):
    print("\n=== Benchmark des algorithmes ===\n")

    for n in n_values:
        print(f"--- Taille n = {n} ---")

        couts, P, C = generate_random_transport_problem(n)

        # θNO(n)
        t_no = measure_time_nord_ouest(couts, P, C)
        print(f"θNO(n)  : {t_no:.6f} s")

        # θBH(n)
        t_bh = measure_time_balas_hammer(couts, P, C)
        print(f"θBH(n)  : {t_bh:.6f} s")

        # tNO(n)
        t_mp_no = measure_time_marche_pied_from_NO(couts, P, C)
        print(f"tNO(n)  : {t_mp_no:.6f} s")

        # tBH(n)
        t_mp_bh = measure_time_marche_pied_from_BH(couts, P, C)
        print(f"tBH(n)  : {t_mp_bh:.6f} s")

        print()


if __name__ == "__main__":
    benchmark([3, 5, 8, 10])
