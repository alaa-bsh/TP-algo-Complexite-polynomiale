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

// Recherche naïve
int sousMat1(int** A, int n, int m, int** B, int n2, int m2) {
    for (int i = 0; i <= n - n2; i++) {
        for (int j = 0; j <= m - m2; j++) {
            int trouve = 1;
            for (int r = 0; r < n2; r++) {
                for (int c = 0; c < m2; c++) {
                    if (A[i + r][j + c] != B[r][c]) {
                        trouve = 0;
                        break;
                    }
                }
                if (trouve == 0) break;
            }
            if (trouve == 1) return 1;
        }
    }
    return 0;
}

// Recherche optimisée (recherche dichotomique sur la première ligne)
int sousMat2(int** A, int n, int m, int** B, int n2, int m2) {
    for (int i = 0; i <= n - n2; i++) {
        // On cherche le premier élément de B dans la ligne triée de A
        int gauche = 0;
        int droite = m - 1;
        int colCandidat = -1;

        while (gauche <= droite) {
            int milieu = gauche + (droite - gauche) / 2;
            if (A[i][milieu] == B[0][0]) {
                colCandidat = milieu;
                break;
            } else if (A[i][milieu] < B[0][0]) {
                gauche = milieu + 1;
            } else {
                droite = milieu - 1;
            }
        }

        // Si on a trouvé le premier élément, on vérifie toute la sous-matrice
        if (colCandidat != -1 && colCandidat <= m - m2) {
            int trouve = 1;
            for (int r = 0; r < n2; r++) {
                for (int c = 0; c < m2; c++) {
                    if (A[i + r][colCandidat + c] != B[r][c]) {
                        trouve = 0;
                        break;
                    }
                }
                if (trouve == 0) break;
            }
            if (trouve == 1) return 1;
        }
    }
    return 0;
}

int main(int argc, char* argv[]) {
    if (argc < 4) {
        printf("Usage: %s <fichier_A.txt> <fichier_B.txt> <mode: 1 pour sousMat1, 2 pour sousMat2>\n", argv[0]);
        return 1;
    }

    int n, m, n2, m2;
    int** A = lireMatrice(argv[1], &n, &m);
    int** B = lireMatrice(argv[2], &n2, &m2);
    int mode = atoi(argv[3]);

    clock_t debut = clock();
    int resultat = 0;

    if (mode == 1) {
        resultat = sousMat1(A, n, m, B, n2, m2);
    } else {
        resultat = sousMat2(A, n, m, B, n2, m2);
    }

    clock_t fin = clock();
    double temps = (double)(fin - debut) / CLOCKS_PER_SEC;

    if (resultat == 1) {
        printf("Sous-matrice trouvee !\n");
    } else {
        printf("Sous-matrice non trouvee.\n");
    }
    printf("Temps d'execution (mode %d) : %f secondes\n", mode, temps);

    return 0;
}