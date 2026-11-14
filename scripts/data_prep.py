import argparse
import random
from pathlib import Path

SEED = 42

EXO1_SIZES = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1200, 1500]
EXO1_MAX_VALUE = 99

EXO2_MAX_VALUE = 999999

EXO2_VAR_A_SIZES = [(100, 100), (200, 200), (400, 400), (600, 600),
                    (800, 800), (1000, 1000), (1500, 1500), (2000, 2000)]
EXO2_VAR_A_B_SIZE = (10, 10)

EXO2_VAR_B_A_SIZE = (1000, 1000)
EXO2_VAR_B_SIZES = [(5, 5), (10, 10), (20, 20), (50, 50),
                    (100, 100), (200, 200), (400, 400), (800, 800)]


def random_matrix(rng, rows, cols, max_value):
    population = range(max_value + 1)
    return [rng.choices(population, k=cols) for _ in range(rows)]


def write_matrix(path, matrix):
    with open(path, "w") as file:
        file.write(f"{len(matrix)} {len(matrix[0])}\n")
        for row in matrix:
            file.write(" ".join(map(str, row)) + "\n")


def block(matrix, row, col, height, width):
    return [line[col:col + width] for line in matrix[row:row + height]]


def generate_exo1(rng, out):
    folder = out / "exo1"
    folder.mkdir(parents=True, exist_ok=True)
    for n in EXO1_SIZES:
        write_matrix(folder / f"A_{n}.txt", random_matrix(rng, n, n, EXO1_MAX_VALUE))
        write_matrix(folder / f"B_{n}.txt", random_matrix(rng, n, n, EXO1_MAX_VALUE))
        print(f"exo1: n={n} done")


def generate_exo2(rng, out):
    base = out / "exo2"
    for variant in ("non_tries", "tries"):
        (base / variant).mkdir(parents=True, exist_ok=True)

    index = []

    def add_case(serie, case_id, matrix, b_rows, b_cols, a_name, b_name, write_a):
        n, m = len(matrix), len(matrix[0])
        row, col = n - b_rows, m - b_cols
        sorted_matrix = [sorted(line) for line in matrix]
        for variant, content in (("non_tries", matrix), ("tries", sorted_matrix)):
            if write_a:
                write_matrix(base / variant / a_name, content)
            b_matrix = block(content, row, col, b_rows, b_cols)
            write_matrix(base / variant / b_name, b_matrix)
            assert block(content, row, col, b_rows, b_cols) == b_matrix
        index.append([serie, case_id, n, m, b_rows, b_cols, row, col, a_name, b_name])
        print(f"exo2: {serie} case {case_id}: A={n}x{m}, B={b_rows}x{b_cols}")

    b_rows, b_cols = EXO2_VAR_A_B_SIZE
    for case_id, (n, m) in enumerate(EXO2_VAR_A_SIZES, 1):
        matrix = random_matrix(rng, n, m, EXO2_MAX_VALUE)
        add_case("varA", case_id, matrix, b_rows, b_cols,
                 f"varA_A_{n}x{m}.txt", f"varA_B_{b_rows}x{b_cols}_for_{n}x{m}.txt", True)

    n, m = EXO2_VAR_B_A_SIZE
    matrix = random_matrix(rng, n, m, EXO2_MAX_VALUE)
    a_name = f"varB_A_{n}x{m}.txt"
    for case_id, (b_rows, b_cols) in enumerate(EXO2_VAR_B_SIZES, 1):
        add_case("varB", case_id, matrix, b_rows, b_cols,
                 a_name, f"varB_B_{b_rows}x{b_cols}.txt", case_id == 1)

    with open(base / "index.csv", "w") as file:
        file.write("serie,id,n,m,n_b,m_b,row,col,A_file,B_file\n")
        for line in index:
            file.write(",".join(map(str, line)) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="data")
    args = parser.parse_args()

    out = Path(args.out)
    rng = random.Random(SEED)
    generate_exo1(rng, out)
    generate_exo2(rng, out)
    print(f"All files written in {out.resolve()}")


if __name__ == "__main__":
    main()