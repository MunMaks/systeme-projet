"""
22 mars 2024, Copyright MUNAITPASOV Maksat
Universite Gustave Eiffel

pylint src/main.py

--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)
"""

import os
import csv
import subprocess
import glob
import logging

class GestionEtudiants:
    """
    Class pour gerer le devoir des etudiants
    """

    def __init__(self, chemin_dossier_etudiants: str):
        """
        Initialisation des parametres

        Args:
            self.chemin_dossier_etudiants (str):
                Le chemin absolu vers le dossier contenant les fichiers des etudiants.
        """
        self.chemin_dossier_etudiants = chemin_dossier_etudiants


    def generer_fichier_csv(self) -> None:
        """
        Genere un fichier CSV contenant les informations relatives a chaque etudiant.

        Args:
            self.chemin_dossier_etudiants (str):
                Le chemin absolu vers le dossier contenant les fichiers des etudiants.
        """

        # creation du fichier CSV
        with open('informations_etudiants.csv', 'w', newline='') as csvfile:
            fieldnames = ['Prenom', 'Nom', 'Compilation', 'Warnings',\
                            'Tests Reussis', 'Note de Qualite',\
                            'Note de Compilation', 'Note Finale']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # recuperer la liste des fichiers des etudiants
            for fichier in os.listdir(self.chemin_dossier_etudiants):
                if fichier.endswith(".c"):

                    # tous les calculs nécessaires pour un fichier d'étudiant
                    resultats = self.calculs(fichier)

                    # ecrire les informations dans le fichier CSV d'après le dictionnaire
                    writer.writerow({'Prenom': resultats['prenom'], 'Nom': resultats['nom'],
                                     'Compilation': int(resultats['compilation_reussie']),
                                     'Warnings': resultats['nb_warnings'],
                                     'Tests Reussis': resultats['nb_tests_reussis'],
                                     'Note de Qualite': resultats['note_doc'],
                                     'Note de Compilation': resultats['note_compilation'],
                                     'Note Finale': resultats['note_finale']})


    def calculs(self, fichier: str) -> dict:
        """
        Effectue les calculs pour chaque étudiant.

        Args:
            fichier (str): Nom du fichier étudiant.

        Returns:
            dict: Dictionnaire contenant les résultats des calculs.
        """
        chemin_fichier = os.path.join(self.chemin_dossier_etudiants, fichier)

        prenom, nom = self.extraire_nom_etudiant(fichier)

        compilation_reussie, fichier_executable, nb_warnings = \
            self.compiler_fichier_c(chemin_fichier)

        nb_lignes_doc = self.compter_lignes_documentation(chemin_fichier)

        nb_tests_reussis = self.lancer_tests(fichier_executable) if compilation_reussie else 0


        # calcul des notes
        note_doc = round(nb_lignes_doc * (2 / 3), 2) if nb_lignes_doc < 4 else 2.0

        note_compilation = ((compilation_reussie * 3) - (nb_warnings * 0.5)) \
            if (((compilation_reussie * 3) - (nb_warnings * 0.5)) > 0) else 0

        note_finale = round(note_compilation + note_doc + (nb_tests_reussis * (5 / 7)), 2)

        return {'prenom': prenom, 'nom' : nom,
                'compilation_reussie': compilation_reussie, 'nb_warnings': nb_warnings,
                'nb_tests_reussis': nb_tests_reussis, 'note_doc': note_doc,
                'note_compilation': note_compilation, 'note_finale': note_finale}


    def nettoyer_executables(self) -> None:
        """
        Nettoie tous les fichiers executables (.out) du repertoire des etudiants.

        Args:
            self.chemin_dossier_etudiants (str):
                Le chemin absolu vers le dossier contenant les fichiers des etudiants.
        """

        chemin_fichiers_executables = os.path.join(self.chemin_dossier_etudiants, "*.out")

        # recuperer la liste des fichiers executables
        fichiers_executables = glob.glob(chemin_fichiers_executables)

        # supprimer les fichiers executables
        for fichier in fichiers_executables:
            try:
                os.remove(fichier)
            except OSError as err:  # expliqué dans le README.MD ligne 43
                logging.error("Erreur lors de la suppression du\
                               fichier executable : %s", err)


    @staticmethod
    def extraire_nom_etudiant(nom_fichier: str) -> tuple:
        """
        Extrait le prenom et le nom de l'etudiant a partir du nom du fichier.

        Args:
            nom_fichier (str): Le nom du fichier contenant le prenom et le nom de l'etudiant.

        Returns:
            tuple: Un tuple contenant le prenom et le nom de l'etudiant.
        """
        nom_fichier_sans_extension = os.path.splitext(nom_fichier)[0]
        prenom, nom = nom_fichier_sans_extension.split('_')
        return prenom.capitalize(), nom.capitalize()


    @staticmethod
    def compiler_fichier_c(chemin_fichier: str) -> tuple:
        """
        Compile un fichier C avec gcc et des flags en utilisant subprocess.

        Args:
            chemin_fichier (str):
                Le chemin absolu vers le fichier C a compiler.

        Returns:
            tuple: Un tuple contenant trois elements :
                - Un booleen indiquant si la compilation a reussi.
                - Le chemin absolu vers le fichier compile (si la compilation a reussi).
                - Le nombre de warnings emis par le compilateur lors de la compilation.

        """
        nom_fichier_sans_extension = os.path.splitext(chemin_fichier)[0]
        fichier_executable = nom_fichier_sans_extension + ".out"

        # compiler le fichier avec gcc
        resultat_compilation = subprocess.run( \
            ["gcc", "-Wall", "-ansi", chemin_fichier, "-o", fichier_executable], \
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)

        # la compilation a reussi
        if resultat_compilation.returncode == 0 and os.path.exists(fichier_executable):
            return True, fichier_executable, \
                len(resultat_compilation.stderr.decode().split('\n')) - 1

        # la compilation a rate
        return False, None, len(resultat_compilation.stderr.decode().split('\n')) - 1


    @staticmethod
    def compter_lignes_documentation(chemin_fichier: str) -> int:
        """
        Compte le nombre de lignes de documentation dans un fichier.

        Args:
            chemin_fichier (str):
                Le chemin absolu vers le fichier a analyser.

        Returns:
            int: Le nombre de lignes de documentation.
        """
        # Ouvrir le fichier et compter les lignes de documentation
        with open(chemin_fichier, 'r') as file:
            lignes = file.readlines()
            nb_lignes_doc = sum(1 for ligne in lignes if "/*" in ligne or "//" in ligne)
            return nb_lignes_doc


    @staticmethod
    def lancer_tests(fichier_executable: str) -> int:
        """
        Lance les tests sur un fichier compile.

        Args:
            fichier_executable (str):
                Le chemin absolu vers le fichier executable a tester.

        Returns:
            int: Le nombre de tests reussis.
        """
        tests = [[0, 0], [1, 0], [0, 1], [1, 1],
                [12, 12], [12, -43], [-1, -52]]

        nb_tests_reussis = 0
        for test in tests:
            resultat_attendu = test[0] + test[1]

            resultat_test = subprocess.run( \
                ["./" + fichier_executable, str(test[0]), str(test[1])], \
                stdout=subprocess.PIPE, check=False).stdout.decode().strip()

            if int(resultat_test.split()[-1]) == resultat_attendu:
                nb_tests_reussis += 1

        return nb_tests_reussis



def main() -> None:
    """
        Main function
    """
    chemin_dossier_etudiants = "eleves_bis"

    gestionetudiants = GestionEtudiants(chemin_dossier_etudiants)
    gestionetudiants.generer_fichier_csv()
    gestionetudiants.nettoyer_executables()


if __name__ == '__main__':
    main()
