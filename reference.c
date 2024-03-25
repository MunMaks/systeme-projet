/* import les bibliotheques necessaires */
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]){

    if (argc != 3) return 0;    /* si nous avons assez d'arguments */

    printf("%d\n", atoi(argv[1]) + atoi(argv[2]));  /* afficher le resultat */

    return 0;   /* sortie de la programme */
}
