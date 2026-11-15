#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int** allouerMatrice(int lignes, int cols) {
    int** M = (int**)malloc(lignes * sizeof(int*));
    for (int i = 0; i < lignes; i++) {
        M[i] = (int*)malloc(cols * sizeof(int));
    }
    return M;
}

int** lireMatrice(const char* nomFichier, int* lignes, int* cols) {
    FILE* f = fopen(nomFichier, "r");
    if (f == NULL) {
        printf("Erreur d'ouverture du fichier %s\n", nomFichier);
        exit(1);
    }
    
    fscanf(f, "%d %d", lignes, cols);
    int** M = allouerMatrice(*lignes, *cols);
    
    for (int i = 0; i < *lignes; i++) {
        for (int j = 0; j < *cols; j++) {
            fscanf(f, "%d", &M[i][j]);
        }
    }
    fclose(f);
    return M;
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        printf("Usage: %s <fichier_A.txt> <fichier_B.txt>\n", argv[0]);
        return 1;
    }

    int n, m, m2, p;
    int** A = lireMatrice(argv[1], &n, &m);
    int** B = lireMatrice(argv[2], &m2, &p);

    if (m != m2) {
        printf("Erreur de dimensions pour la multiplication.\n");
        return 1;
    }

    int** C = allouerMatrice(n, p);

    clock_t debut = clock();

    // Calcul du produit : C = A * B
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < p; j++) {
            C[i][j] = 0;
            for (int k = 0; k < m; k++) {
                C[i][j] = C[i][j] + (A[i][k] * B[k][j]);
            }
        }
    }

    clock_t fin = clock();
    double temps = (double)(fin - debut) / CLOCKS_PER_SEC;

    printf("Temps d'execution : %f secondes\n", temps);
    printf("C[0][0] = %d\n", C[0][0]);

    return 0;
}