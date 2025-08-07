# csv excerpt
# LOCALITE,Code Postal ,NOM,POPULATION,SUPERFICIE,LOCTYPE,PROVINCE
# AISEAU-PRESLES ,6250,Commune d'Aiseau-Presles,10978,2300,Commune,Hainaut
# AMAY ,4540,Commune d'Amay,14531,2760,Commune/Village,Liège

import csv
from pathlib import Path

DEPARTMENT_NAME_TO_CODE = {
    "Province du Luxembourg": "80000",
    "Province de Liège": "60000",
    "Province du Brabant flamand": "70000",
    "Province d'Anvers": "20000",
    "Province de Flandre occidentale": "30000",
    "Province du Brabant wallon": "20002",
    "Province de Namur": "90000",
    "Province du Hainaut": "50000",
    "Province de Flandre orientale": "40000",
}


def get_province_code(province_partial_name):
    for province, code in DEPARTMENT_NAME_TO_CODE.items():
        if province_partial_name in province:
            return code
    raise ValueError(f"Province {province_partial_name} not found")


script_dir = Path(__file__).parent
file_path = script_dir / "be_communes.csv"

COMMUNES = []

with open(file_path, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=",")
    for row in reader:
        COMMUNES.append(
            {
                "code": row["Code Postal"].strip(),
                "nom": row["NOM"].strip(),
                "population": row["POPULATION"],
                "departement": get_province_code(row["PROVINCE"].strip()),
                "codesPostaux": [row["Code Postal"].strip()],
            }
        )
