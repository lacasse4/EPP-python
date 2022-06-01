# Program EPP-python version 1.0
# Author: Vincent Lacasse (lacasse4@yahoo.com)
# Date: 2022-06-01
# GitHub: https://github.com/lacasse4/EPP-python

# This Python program must be executed from a command line.
# Typical invocation:
#      $ python3 EPP.py -ELE400 evaluations_20211220-164427.csv
# The program reads a csv file previously exported by 'export des évaluations (sans multiligne)'
# from Workshop ÉTS in Moodle. It produces an Excel spreadsheet which allows a teacher to easily
# compute individual student scores following a peer review done with 'Module Atelier' in Moodle.
# This program is functionnaly equivalent to EPP V1.4 written in Java (https://github.com/lacasse4/EPP)

# Note: to run, you may have to install the 'openpyxl' Python library on your computer.
# To do so, run the following command:
#      $ pip install openpyxl

import epp_reader as r
import epp_writer as w
import os
import argparse as ap

if __name__ == '__main__':
    #
    # parse the command line
    #
    parser = ap.ArgumentParser(
        description = 
"""
Ce programme produit un ficher xlsx à partir de l'export des évaluations (.csv).
Le fichier_csv doit provenir de l'export des évaluations (sans multiligne) du Workshop ÉTS.
Lorsque le ficher_xlsx est omis, il portera le même nom que le fichier csv (sauf le suffixe).
Les options -ELE400 et -ELE795 sont mutuellement exclusives. Ne spécifiez qu'une seule d'entre elles.
Les options -min et -max seront ignorées si l'option -ELE400 ou -ELE795 a été spécifiée.
""")
    parser.add_argument('fichier_csv', nargs = 1, help = 'fichier csv à convertir (obligatoire)')
    parser.add_argument('fichier_xlsx', nargs = '?', help = 'fichier xlsx produit (optionnel)')
    parser.add_argument('-ELE400', action='store_true', help = 'min et max sont initialisés à 1 et 5 pour ELE400')
    parser.add_argument('-ELE795', action='store_true', help = 'min et max sont initialisés à 0 et 3 pour ELE795')
    parser.add_argument('-min', nargs = 1, type = int, default = [1], choices = [0, 1], help = 'score minimum pour un aspect d''évaluation')
    parser.add_argument('-max', nargs = 1, type = int, default = [5], choices = [2, 3, 4, 5], help = 'score maximum pour un aspect d''évaluation')
    parser.add_argument('-v', '--verbose', action='store_true', help = 'affiche les données à la console (pour déverminage)')
    
    args = parser.parse_args()
    if args.verbose:
        print("Parametres")
        print("  fichier_csv : " + args.fichier_csv[0])
        print("  fichier_xlsx: " + str(args.fichier_xlsx))
        print("  ELE400      : " + str(args.ELE400))
        print("  ELE795      : " + str(args.ELE795))
        print("  min         : " + str(args.min[0]))
        print("  max         : " + str(args.max[0]))
        print("  verbose     : " + str(args.verbose))
        print()
    
    input_filename = args.fichier_csv[0]
    
    # check if the input csv file exists
    if os.path.exists(input_filename):
        name_without_suffix = os.path.splitext(input_filename)[0] 
        temp_filename   = name_without_suffix + ".tmp"
        # use a specific output file if it was specified on the command line
        if args.fichier_xlsx == None:
            output_filename = name_without_suffix + ".xlsx"
        else:
            output_filename = args.fichier_xlsx
    else:
        raise NameError("Fichier invalide: " + input_filename)
    
    # check options
    min = args.min[0]
    max = args.max[0]
    if args.ELE400:
        min = 1
        max = 5
    elif args.ELE795:
        min = 0
        max = 3
        
    # show calculation method used
    if min == 1 and max == 5:
        msg = "Calculs selon le barême de ELE400 (aspect min = 1, aspect max = 5)"
    elif min == 0 and max == 3:
        msg = "Calculs selon le barême de ELE795 (aspect min = 0, aspect max = 3)"
    else:
        msg = f"Les calculs réalisés avec aspect min = {min} et aspect max = {max}"
    print(msg)
    
    #
    # Read and process the input file
    #
    
    print("Fichier lu: " + input_filename)
    
    # clean csv file
    r.clean_csv(input_filename, temp_filename)

    # read cleaned file into memory (rows)
    rows = r.read_csv(temp_filename)
    os.remove(temp_filename)
    
    # parse rows and build epp data structure
    epp = r.parse(rows)
    epp.compute(min, max)
    
    #
    # Write results in Excel format
    #
    
    if args.verbose:
        print(epp)    
    
    print("Fichier produit: " + output_filename)
    w.write_xlsx(output_filename, epp)
    
    print("Traitement terminé avec succès")