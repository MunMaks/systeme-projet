"""
22 mars 2024, Copyright MUNAIT Maks
Université Gustave Eiffel
"""

import os
import csv
import subprocess


def extraire_nom_etudiant(nom_fichier):
    """
    Extrait le prénom et le nom de l'étudiant à partir du nom du fichier.

    Args:
        nom_fichier (str): Le nom du fichier contenant le prénom et le nom de l'étudiant.

    Returns:
        tuple: Un tuple contenant le prénom et le nom de l'étudiant.
    """
    nom_fichier_sans_extension = os.path.splitext(nom_fichier)[0]
    prenom, nom = nom_fichier_sans_extension.split('_')
    return prenom.capitalize(), nom.capitalize()



def compiler_fichier_c(chemin_fichier):
    """
    Compile un fichier C avec gcc en utilisant subprocess.

    Args:
        chemin_fichier (str): Le chemin absolu vers le fichier C à compiler.

    Returns:
        bool: True si la compilation réussie, False sinon.
    """
    nom_fichier_sans_extension = os.path.splitext(chemin_fichier)[0]
    fichier_compilable = nom_fichier_sans_extension + ".out"

    # Compiler le fichier avec gcc
    resultat_compilation = subprocess.run(["gcc", chemin_fichier, "-o", fichier_compilable, "-Wall", "-ansi"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Vérifier si la compilation a réussi
    if resultat_compilation.returncode == 0 and os.path.exists(fichier_compilable):
        return True, fichier_compilable, len(resultat_compilation.stderr.decode().split('\n')) - 1
    else:
        return False, None, len(resultat_compilation.stderr.decode().split('\n')) - 1



def lancer_tests(fichier_compilable):
    """
    Lance les tests sur un fichier compilé.

    Args:
        fichier_compilable (str): Le chemin absolu vers le fichier exécutable à tester.

    Returns:
        int: Le nombre de tests réussis.
    """
    tests = [
        [0, 0],
        [1, 0],
        [0, 1],
        [1, 1],
        [12, 12],
        [12, -43],
        [-1, -52]
    ]
    nb_tests_reussis = 0
    reference_compilable = "reference.out"
    subprocess.run(["gcc", "reference.c", "-o", reference_compilable])
    for test in tests:
        resultat_attendu = subprocess.run(["./" + reference_compilable, str(test[0]), str(test[1])], stdout=subprocess.PIPE).stdout.decode().strip()
        resultat_test = subprocess.run([fichier_compilable, str(test[0]), str(test[1])], stdout=subprocess.PIPE).stdout.decode().strip()
        if resultat_test == resultat_attendu:
            nb_tests_reussis += 1
    os.remove(reference_compilable)
    return nb_tests_reussis



def compter_lignes_documentation(chemin_fichier):
    """
    Compte le nombre de lignes de documentation dans un fichier.

    Args:
        chemin_fichier (str): Le chemin absolu vers le fichier à analyser.

    Returns:
        int: Le nombre de lignes de documentation.
    """
    # Ouvrir le fichier et compter les lignes de documentation
    with open(chemin_fichier, 'r') as f:
        lignes = f.readlines()
        nb_lignes_doc = sum(1 for ligne in lignes if ligne.strip().startswith("/*") or ligne.strip().startswith("//"))
        return nb_lignes_doc


def nettoyer_executables(chemin_dossier_etudiants):
    """
    Nettoie tous les fichiers exécutables (.out) du répertoire des étudiants.

    Args:
        chemin_dossier_etudiants (str): Le chemin absolu vers le dossier contenant les fichiers des étudiants.
    """
    # Récupérer la liste des fichiers des étudiants
    liste_fichiers_etudiants = os.listdir(chemin_dossier_etudiants)

    # Supprimer tous les fichiers exécutables (.out)
    for fichier in liste_fichiers_etudiants:
        if fichier.endswith(".out"):
            chemin_fichier = os.path.join(chemin_dossier_etudiants, fichier)
            os.remove(chemin_fichier)


def generer_fichier_csv(chemin_dossier_etudiants):
    """
    Génère un fichier CSV contenant les informations relatives à chaque étudiant.

    Args:
        chemin_dossier_etudiants (str): Le chemin absolu vers le dossier contenant les fichiers des étudiants.
    """
    # Créer le fichier CSV
    with open('informations_etudiants.csv', 'w', newline='') as csvfile:
        fieldnames = ['Prénom', 'Nom', 'Compilation', 'Warnings', 'Tests Réussis', 'Lignes de Documentation']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Récupérer la liste des fichiers des étudiants
        liste_fichiers_etudiants = os.listdir(chemin_dossier_etudiants)

        # Analyser chaque fichier étudiant
        for fichier in liste_fichiers_etudiants:
            if fichier.endswith(".c"):
                chemin_fichier = os.path.join(chemin_dossier_etudiants, fichier)
                
                # Informations sur l'étudiant
                prenom, nom = extraire_nom_etudiant(fichier)

                # Informations sur la compilation
                compilation_reussie, fichier_compilable, nb_warnings = compiler_fichier_c(chemin_fichier)
                
                # Nombre de tests réussis
                if compilation_reussie:
                    nb_tests_reussis = lancer_tests(fichier_compilable)
                else:
                    nb_tests_reussis = 0

                # Nombre de lignes de documentation
                nb_lignes_doc = compter_lignes_documentation(chemin_fichier)

                # Écrire les informations dans le fichier CSV
                writer.writerow({'Prénom': prenom, 'Nom': nom, 'Compilation': int(compilation_reussie),
                                 'Warnings': nb_warnings, 'Tests Réussis': nb_tests_reussis,
                                 'Lignes de Documentation': nb_lignes_doc})





def main():
    chemin_dossier_etudiants = "eleves_bis"
    generer_fichier_csv(chemin_dossier_etudiants)
    
    # Nettoyer les fichiers exécutables
    nettoyer_executables(chemin_dossier_etudiants)




if __name__ == '__main__':
    main()
