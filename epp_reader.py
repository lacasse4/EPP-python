import csv
import epp_model as m

""" Static functions to read and parse the CSV file produced by Workshop ETS (sans multiligne)
    It is assumed that the file read in the context of the peer review is produced by the
    Module Atelier in Moodle. WorkshopETS "Export des evaluations (sans multiligne)" button
    must be used. The file can be exported once all students have done their evaluations,
    this either in:
        - Phase de notation des évaluations, or
        - Phase fermée
    
    Note that elements in the CSV file are actually separated by semicolons (";"). 
    
    As of fall of 2021, it is also possible for a teacher to override the note
    attributed to a student (usefull when there is a fraude tentative). This program
    will take the overriden note into account.
    
    Prior to using the read_csv() function, the clean_csv() function shall be used to
    produce an temporary file. clean_csv() was added because some non-printable
    characters are sometimes present in the original file outputed by "Export des evaluations".
    
    For reference, here is an excerpt of the CSV file expected.
    
Groupe;Nom_évalué;Prenom_évalué;Courriel_évalué;Bareme;Note_aspect;Note_calc;Note_modif;Note;MNG;Facteur;Commentaires;Nom_évaluateur;Prenom_évaluateur;Commentaires_generaux
EQUIPE1_ELE795;etudiant12;etudiant12;etudiant12@etsmtl.ca;"Organisation du travail d’équipe";3;50;60;60;46,25;1,297297;Autoévaluation;etudiant12;etudiant12;"Commentaire general&nbsp; Autoévaluation"
EQUIPE1_ELE795;etudiant12;etudiant12;etudiant12@etsmtl.ca;"Composition avec les différences individuelles";3;50;60;60;46,25;1,297297;Autoévaluation;etudiant12;etudiant12;"Commentaire general&nbsp; Autoévaluation"
EQUIPE1_ELE795;etudiant12;etudiant12;etudiant12@etsmtl.ca;"Aptitude à proposer des solutions";3;50;60;60;46,25;1,297297;Autoévaluation;etudiant12;etudiant12;"Commentaire general&nbsp; Autoévaluation"
EQUIPE1_ELE795;etudiant12;etudiant12;etudiant12@etsmtl.ca;"Esprit d’équipe";3;50;60;60;46,25;1,297297;Autoévaluation;etudiant12;etudiant12;"Commentaire general&nbsp; Autoévaluation"
EQUIPE1_ELE795;etudiant12;etudiant12;etudiant12@etsmtl.ca;Présence;3;50;60;60;46,25;1,297297;Autoévaluation;etudiant12;etudiant12;"Commentaire general&nbsp; Autoévaluation"
EQUIPE1_ELE795;etudiant12;etudiant12;etudiant12@etsmtl.ca;"Quantité de travail";3;50;60;60;46,25;1,297297;Autoévaluation;etudiant12;etudiant12;"Commentaire general&nbsp; Autoévaluation"
EQUIPE1_ELE795;etudiant12;etudiant12;etudiant12@etsmtl.ca;"Qualité du travail";3;50;60;60;46,25;1,297297;Autoévaluation;etudiant12;etudiant12;"Commentaire general&nbsp; Autoévaluation"
EQUIPE1_ELE795;etudiant12;etudiant12;etudiant12@etsmtl.ca;"Organisation du travail d’équipe";3;50;60;60;46,25;1,297297;"Étudiant13 évalue Étudiant12";etudiant13;etudiant13;"Commentaire generalÉtudiant13 évalue Étudiant12"
EQUIPE1_ELE795;etudiant12;etudiant12;etudiant12@etsmtl.ca;"Composition avec les différences individuelles";3;50;60;60;46,25;1,297297;"Étudiant13 évalue Étudiant12";etudiant13;etudiant13;"Commentaire generalÉtudiant13 évalue Étudiant12"
EQUIPE1_ELE795;etudiant12;etudiant12;etudiant12@etsmtl.ca;"Aptitude à proposer des solutions";3;50;60;60;46,25;1,297297;"Étudiant13 évalue Étudiant12";etudiant13;etudiant13;"Commentaire generalÉtudiant13 évalue Étudiant12"
EQUIPE1_ELE795;etudiant12;etudiant12;etudiant12@etsmtl.ca;"Esprit d’équipe";3;50;60;60;46,25;1,297297;"Étudiant13 évalue Étudiant12";etudiant13;etudiant13;"Commentaire generalÉtudiant13 évalue Étudiant12"
EQUIPE1_ELE795;etudiant12;etudiant12;etudiant12@etsmtl.ca;Présence;3;50;60;60;46,25;1,297297;"Étudiant13 évalue Étudiant12";etudiant13;etudiant13;"Commentaire generalÉtudiant13 évalue Étudiant12"
EQUIPE1_ELE795;etudiant12;etudiant12;etudiant12@etsmtl.ca;"Quantité de travail";3;50;60;60;46,25;1,297297;"Étudiant13 évalue Étudiant12";etudiant13;etudiant13;"Commentaire generalÉtudiant13 évalue Étudiant12"
EQUIPE1_ELE795;etudiant12;etudiant12;etudiant12@etsmtl.ca;"Qualité du travail";3;50;60;60;46,25;1,297297;"Étudiant13 évalue Étudiant12";etudiant13;etudiant13;"Commentaire generalÉtudiant13 évalue Étudiant12"
EQUIPE1_ELE795;etudiant12;etudiant12;etudiant12@etsmtl.ca;"Organisation du travail d’équipe";3;50;60;60;46,25;1,297297;"Étudiant14 évalue Étudiant12";etudiant14;etudiant14;"Commentaire general&nbsp;Étudiant14 évalue Étudiant12"
EQUIPE1_ELE795;etudiant12;etudiant12;etudiant12@etsmtl.ca;"Composition avec les différences individuelles";3;50;60;60;46,25;1,297297;"Étudiant14 évalue Étudiant12";etudiant14;etudiant14;"Commentaire general&nbsp;Étudiant14 évalue Étudiant12"
EQUIPE1_ELE795;etudiant12;etudiant12;etudiant12@etsmtl.ca;"Aptitude à proposer des solutions";3;50;60;60;46,25;1,297297;"Étudiant14 évalue Étudiant12";etudiant14;etudiant14;"Commentaire general&nbsp;Étudiant14 évalue Étudiant12"
EQUIPE1_ELE795;etudiant12;etudiant12;etudiant12@etsmtl.ca;"Esprit d’équipe";3;50;60;60;46,25;1,297297;"Étudiant14 évalue Étudiant12";etudiant14;etudiant14;"Commentaire general&nbsp;Étudiant14 évalue Étudiant12"
EQUIPE1_ELE795;etudiant12;etudiant12;etudiant12@etsmtl.ca;Présence;3;50;60;60;46,25;1,297297;"Étudiant14 évalue Étudiant12";etudiant14;etudiant14;"Commentaire general&nbsp;Étudiant14 évalue Étudiant12"
EQUIPE1_ELE795;etudiant12;etudiant12;etudiant12@etsmtl.ca;"Quantité de travail";3;50;60;60;46,25;1,297297;"Étudiant14 évalue Étudiant12";etudiant14;etudiant14;"Commentaire general&nbsp;Étudiant14 évalue Étudiant12"
EQUIPE1_ELE795;etudiant12;etudiant12;etudiant12@etsmtl.ca;"Qualité du travail";3;50;60;60;46,25;1,297297;"Étudiant14 évalue Étudiant12";etudiant14;etudiant14;"Commentaire general&nbsp;Étudiant14 évalue Étudiant12"
EQUIPE1_ELE795;etudiant12;etudiant12;etudiant12@etsmtl.ca;"Organisation du travail d’équipe";1;50;60;60;46,25;1,297297;"Étudiant15 évalue Étudiant12 (fraude)";etudiant15;etudiant15;"Commentaire generalÉtudiant15 évalue Étudiant12 (fraude)"
EQUIPE1_ELE795;etudiant12;etudiant12;etudiant12@etsmtl.ca;"Composition avec les différences individuelles";1;50;60;60;46,25;1,297297;"Étudiant15 évalue Étudiant12 (fraude)";etudiant15;etudiant15;"Commentaire generalÉtudiant15 évalue Étudiant12 (fraude)"
EQUIPE1_ELE795;etudiant12;etudiant12;etudiant12@etsmtl.ca;"Aptitude à proposer des solutions";1;50;60;60;46,25;1,297297;"Étudiant15 évalue Étudiant12 (fraude)";etudiant15;etudiant15;"Commentaire generalÉtudiant15 évalue Étudiant12 (fraude)"
EQUIPE1_ELE795;etudiant12;etudiant12;etudiant12@etsmtl.ca;"Esprit d’équipe";1;50;60;60;46,25;1,297297;"Étudiant15 évalue Étudiant12 (fraude)";etudiant15;etudiant15;"Commentaire generalÉtudiant15 évalue Étudiant12 (fraude)"
EQUIPE1_ELE795;etudiant12;etudiant12;etudiant12@etsmtl.ca;Présence;1;50;60;60;46,25;1,297297;"Étudiant15 évalue Étudiant12 (fraude)";etudiant15;etudiant15;"Commentaire generalÉtudiant15 évalue Étudiant12 (fraude)"
EQUIPE1_ELE795;etudiant12;etudiant12;etudiant12@etsmtl.ca;"Quantité de travail";1;50;60;60;46,25;1,297297;"Étudiant15 évalue Étudiant12 (fraude)";etudiant15;etudiant15;"Commentaire generalÉtudiant15 évalue Étudiant12 (fraude)"
EQUIPE1_ELE795;etudiant12;etudiant12;etudiant12@etsmtl.ca;"Qualité du travail";1;50;60;60;46,25;1,297297;"Étudiant15 évalue Étudiant12 (fraude)";etudiant15;etudiant15;"Commentaire generalÉtudiant15 évalue Étudiant12 (fraude)"
EQUIPE1_ELE795;etudiant13;etudiant13;etudiant13@etsmtl.ca;"Organisation du travail d’équipe";4;75;0;75;46,25;1,621622;"Étudiant12 évalue Étudiant13";etudiant12;etudiant12;"Commentaire general&nbsp;Étudiant12 évalue Étudiant13"
EQUIPE1_ELE795;etudiant13;etudiant13;etudiant13@etsmtl.ca;"Composition avec les différences individuelles";4;75;0;75;46,25;1,621622;"Étudiant12 évalue Étudiant13";etudiant12;etudiant12;"Commentaire general&nbsp;Étudiant12 évalue Étudiant13"
EQUIPE1_ELE795;etudiant13;etudiant13;etudiant13@etsmtl.ca;"Aptitude à proposer des solutions";4;75;0;75;46,25;1,621622;"Étudiant12 évalue Étudiant13";etudiant12;etudiant12;"Commentaire general&nbsp;Étudiant12 évalue Étudiant13"
EQUIPE1_ELE795;etudiant13;etudiant13;etudiant13@etsmtl.ca;"Esprit d’équipe";4;75;0;75;46,25;1,621622;"Étudiant12 évalue Étudiant13";etudiant12;etudiant12;"Commentaire general&nbsp;Étudiant12 évalue Étudiant13"
EQUIPE1_ELE795;etudiant13;etudiant13;etudiant13@etsmtl.ca;Présence;4;75;0;75;46,25;1,621622;"Étudiant12 évalue Étudiant13";etudiant12;etudiant12;"Commentaire general&nbsp;Étudiant12 évalue Étudiant13"
EQUIPE1_ELE795;etudiant13;etudiant13;etudiant13@etsmtl.ca;"Quantité de travail";4;75;0;75;46,25;1,621622;"Étudiant12 évalue Étudiant13";etudiant12;etudiant12;"Commentaire general&nbsp;Étudiant12 évalue Étudiant13"
...
"""
    
def read_csv(filename: str) -> list:
    """ read a csv file and return a list of dictionaries """
    
    in_file = open(filename)
    csv_reader = csv.DictReader(in_file, delimiter=";")
    
    rows = []
    for row in csv_reader:
        rows.append(row)
    
    in_file.close()
    return rows


def clean_csv(in_file: str, out_file: str) -> None:
    """ remove non-printable characters from in_file and write result to out_file """
    
    with open(in_file, "rt") as f:
        in_lines = f.readlines()
    
    out_lines = []
    for in_line in in_lines:
        # from https://stackoverflow.com/questions/92438/stripping-non-printable-characters-from-a-string-in-python
        out_line = ''.join(c for c in in_line if c.isprintable())
        out_lines.append(out_line + '\n')
        
    with open(out_file, "wt") as f:
        f.writelines(out_lines)
    

def get_empty_dict(row: dict) -> dict:
    """ returns an empty dictionary with same key entries as row """
    
    empty = {}
    keys = row.keys();
    for key in keys:
        empty[key] = ""
    
    return empty
     
        
def parse(rows: list) -> m.EPP:
    """ parse rows and create an EPP data structure.
    rows is an array of dictionnary. Each individual row is a line
    from the CSV file in the form of a dictionnary. """
    
    last = get_empty_dict(rows[0])
    epp = m.EPP()
    
    for row in rows:
        team_added = False
        evaluated_added = False
        
        # detect team changes in csv file
        if last["Groupe"] != row["Groupe"]:
            last["Groupe"] = row["Groupe"]
            team = m.Team(row["Groupe"])
            epp.append(team)
            team_added = True
            
        # detect evaluated student change in csv file
        if team_added \
        or last["Nom_évalué"] != row["Nom_évalué"] \
        or last["Prenom_évalué"] != row["Prenom_évalué"]:
            last["Nom_évalué"] = row["Nom_évalué"]
            last["Prenom_évalué"] = row["Prenom_évalué"]
            evaluated = m.Evaluated(row["Nom_évalué"], row["Prenom_évalué"], row["Courriel_évalué"])
            team.append(evaluated)
            evaluated_added = True
            
        # detect an evaluator student change is csv file
        if team_added \
        or evaluated_added \
        or last["Nom_évaluateur"] != row["Nom_évaluateur"] \
        or last["Prenom_évaluateur"] != row["Prenom_évaluateur"]:
            last["Nom_évaluateur"] = row["Nom_évaluateur"]
            last["Prenom_évaluateur"] = row["Prenom_évaluateur"]
            evaluator = m.Evaluator(row["Nom_évaluateur"], row["Prenom_évaluateur"])
            evaluated.append(evaluator)
            
        # use the overridden note as the aspect score if the overridden note is not 0
        # otherwise use aspect score as is.
        modified_note = float(row["Note_modif"])
        if modified_note > 0.0:
            evaluated.modify(modified_note)
        else:
            evaluator.append(int(row["Note_aspect"]))
            
    return epp