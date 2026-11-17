import argparse
import random
from collections import deque
from pathlib import Path

SEED = 42

EXO1_SIZES = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1200, 1500]
EXO1_MAX_VALUE = 99

EXO2_MAX_VALUE = 99999
EXO2_A_SIZES = [100, 200, 400, 600, 800, 1000, 2000, 4000, 6000, 8000]
EXO2_THRESHOLD = 2000
EXO2_B_SIZES_BELOW = [10, 20, 30, 40, 50]
EXO2_B_SIZES_FROM = [100, 200, 300, 400, 500]


def random_matrix(rng, rows, cols, max_value):
    population = range(max_value + 1)
    return [rng.choices(population, k=cols) for _ in range(rows)]


def write_matrix(path, matrix):
    with open(path, "w") as file:
        file.write(f"{len(matrix)} {len(matrix[0])}\n")
        for row in matrix:
            file.write(" ".join(map(str, row)) + "\n")


def generate_exo1(rng, out):
    folder = out / "exo1"
    folder.mkdir(parents=True, exist_ok=True)
    for n in EXO1_SIZES:
        write_matrix(folder / f"A_{n}.txt",
                     random_matrix(rng, n, n, EXO1_MAX_VALUE))
        write_matrix(folder / f"B_{n}.txt",
                     random_matrix(rng, n, n, EXO1_MAX_VALUE))
        print(f"exo1: n={n} done")


def generate_exo2(rng, out):
    base = out / "exo2"
    for variant in ("non_tries", "tries"):
        (base / variant).mkdir(parents=True, exist_ok=True)

    population = range(EXO2_MAX_VALUE + 1)
    index = []
    case_id = 0

    for n in EXO2_A_SIZES:
        m = n
        b_sizes = EXO2_B_SIZES_BELOW if n < EXO2_THRESHOLD else EXO2_B_SIZES_FROM
        keep = max(b_sizes)
        tail_unsorted = deque(maxlen=keep)
        tail_sorted = deque(maxlen=keep)
        a_name = f"A_{n}x{m}.txt"

        with open(base / "non_tries" / a_name, "w") as file_unsorted, \
                open(base / "tries" / a_name, "w") as file_sorted:
            file_unsorted.write(f"{n} {m}\n")
            file_sorted.write(f"{n} {m}\n")
            for _ in range(n):
                row = rng.choices(population, k=m)
                sorted_row = sorted(row)
                file_unsorted.write(" ".join(map(str, row)) + "\n")
                file_sorted.write(" ".join(map(str, sorted_row)) + "\n")
                tail_unsorted.append(row[-keep:])
                tail_sorted.append(sorted_row[-keep:])

        for size in b_sizes:
            case_id += 1
            b_name = f"B_{size}x{size}_in_{n}x{m}.txt"
            block_unsorted = [line[-size:]
                              for line in list(tail_unsorted)[-size:]]
            block_sorted = [line[-size:] for line in list(tail_sorted)[-size:]]
            write_matrix(base / "non_tries" / b_name, block_unsorted)
            write_matrix(base / "tries" / b_name, block_sorted)
            index.append([case_id, n, m, size, size, n -
                         size, m - size, a_name, b_name])
            print(f"exo2: case {case_id}: A={n}x{m}, B={size}x{size}")

    with open(base / "index.csv", "w") as file:
        file.write("id,n,m,n_b,m_b,row,col,A_file,B_file\n")
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
