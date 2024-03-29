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


class GestionEtudiants:
    """
    Class pour gerer le devoir des etudiants
    """

    def __init__(self, chemin_dossier_etudiants):
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
                    chemin_fichier = os.path.join(self.chemin_dossier_etudiants, fichier)


                    prenom_nom = self.extraire_nom_etudiant(fichier)


                    compilation_reussie, fichier_compilable, nb_warnings =\
                        self.compiler_fichier_c(chemin_fichier)

                    nb_lignes_doc = self.compter_lignes_documentation(chemin_fichier)


                    nb_tests_reussis = self.lancer_tests(fichier_compilable)\
                        if compilation_reussie else 0


                    note_doc = round(nb_lignes_doc * (2/3), 2) if nb_lignes_doc < 4 else 2.0

                    note_compilation = ((compilation_reussie * 3) - (nb_warnings * 0.5))\
                        if (((compilation_reussie * 3) - (nb_warnings * 0.5)) > 0) else 0

                    note_finale = round(note_compilation + note_doc + (nb_tests_reussis * (5/7)), 2)

                    # ecrire les informations dans le fichier CSV
                    writer.writerow({'Prenom': prenom_nom[0], 'Nom': prenom_nom[1], \
                        'Compilation': int(compilation_reussie), 'Warnings': nb_warnings,\
                        'Tests Reussis': nb_tests_reussis, 'Note de Qualite': note_doc,
                        'Note de Compilation' : note_compilation, 'Note Finale': note_finale})


    def nettoyer_executables(self) -> None:
        """
        Nettoie tous les fichiers executables (.out) du repertoire des etudiants.

        Args:
            self.chemin_dossier_etudiants (str):
            Le chemin absolu vers le dossier contenant les fichiers des etudiants.
        """
        # Recuperer la liste des fichiers des etudiants
        liste_fichiers_etudiants = os.listdir(self.chemin_dossier_etudiants)

        # Supprimer tous les fichiers executables (.out)
        for fichier in liste_fichiers_etudiants:
            if fichier.endswith(".out"):
                chemin_fichier = os.path.join(self.chemin_dossier_etudiants, fichier)
                os.remove(chemin_fichier)

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
    def compiler_fichier_c(chemin_fichier) -> tuple:
        """
        Compile un fichier C avec gcc et des flags en utilisant subprocess.

        Args:
            chemin_fichier (str): Le chemin absolu vers le fichier C a compiler.

        Returns:
            bool: True si la compilation reussie, False sinon.
        """
        nom_fichier_sans_extension = os.path.splitext(chemin_fichier)[0]
        fichier_compilable = nom_fichier_sans_extension + ".out"

        # compiler le fichier avec gcc
        resultat_compilation = subprocess.run( \
            ["gcc", "-Wall", "-ansi", chemin_fichier, "-o", fichier_compilable], \
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)

        # la compilation a reussi
        if resultat_compilation.returncode == 0 and os.path.exists(fichier_compilable):
            return True, fichier_compilable, \
                len(resultat_compilation.stderr.decode().split('\n')) - 1

        # la compilation a rate
        return False, None, len(resultat_compilation.stderr.decode().split('\n')) - 1

    @staticmethod
    def compter_lignes_documentation(chemin_fichier) -> int:
        """
        Compte le nombre de lignes de documentation dans un fichier.

        Args:
            chemin_fichier (str): Le chemin absolu vers le fichier a analyser.

        Returns:
            int: Le nombre de lignes de documentation.
        """
        # Ouvrir le fichier et compter les lignes de documentation
        with open(chemin_fichier, 'r') as file:
            lignes = file.readlines()
            nb_lignes_doc = sum(1 for ligne in lignes if "/*" in ligne or "//" in ligne)
            return nb_lignes_doc

    @staticmethod
    def lancer_tests(fichier_compilable: str) -> int:
        """
        Lance les tests sur un fichier compile.

        Args:
            fichier_compilable (str): Le chemin absolu vers le fichier executable a tester.

        Returns:
            int: Le nombre de tests reussis.
        """
        tests = [[0, 0], [1, 0], [0, 1], [1, 1],
                [12, 12], [12, -43], [-1, -52]]

        nb_tests_reussis = 0
        for test in tests:
            resultat_attendu = test[0] + test[1]

            resultat_test = subprocess.run( \
                ["./" + fichier_compilable, str(test[0]), str(test[1])], \
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
