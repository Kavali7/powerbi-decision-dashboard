"""
Génération de données synthétiques pour le dashboard décisionnel.

Ce script produit les fichiers suivants dans data/raw/ :
- dim_calendar.csv
- dim_zone.csv
- dim_program_component.csv
- dim_manager.csv
- fact_monthly_performance.csv
- fact_budget.csv

Exécution :
    python scripts/generate_synthetic_data.py

Toutes les données générées sont fictives et à usage de démonstration uniquement.
"""

import csv
import os
import random

random.seed(42)

# ─── Configuration ──────────────────────────────────────────────────────

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw")

DATE_RANGE = [
    f"{y}-{m:02d}-01"
    for y in [2024, 2025]
    for m in range(1, 13)
    if not (y == 2025 and m > 3)
]

ZONES = {
    "Z01": {"zone_name": "Abidjan-Plateau", "region_group": "Afrique de l'Ouest", "site_count": 5, "population_coverage_estimate": 185000, "zone_priority_level": "High"},
    "Z02": {"zone_name": "Dakar-Almadies", "region_group": "Afrique de l'Ouest", "site_count": 4, "population_coverage_estimate": 142000, "zone_priority_level": "Medium"},
    "Z03": {"zone_name": "Douala-Littoral", "region_group": "Afrique Centrale", "site_count": 6, "population_coverage_estimate": 167000, "zone_priority_level": "High"},
    "Z04": {"zone_name": "Nairobi-Westlands", "region_group": "Afrique de l'Est", "site_count": 4, "population_coverage_estimate": 198000, "zone_priority_level": "High"},
    "Z05": {"zone_name": "Kinshasa-Gombe", "region_group": "Afrique Centrale", "site_count": 3, "population_coverage_estimate": 210000, "zone_priority_level": "Medium"},
    "Z06": {"zone_name": "Casablanca-Anfa", "region_group": "Afrique du Nord", "site_count": 5, "population_coverage_estimate": 155000, "zone_priority_level": "Medium"},
}

COMPONENTS = {
    "C01": {"component_name": "Mobilisation communautaire", "activity_type": "Outreach", "strategic_axis": "Engagement", "unit_of_measure": "Sessions"},
    "C02": {"component_name": "Formation", "activity_type": "Capacity Building", "strategic_axis": "Skills", "unit_of_measure": "Participants"},
    "C03": {"component_name": "Suivi de terrain", "activity_type": "Monitoring", "strategic_axis": "Quality", "unit_of_measure": "Visits"},
    "C04": {"component_name": "Appui ciblé", "activity_type": "Support", "strategic_axis": "Results", "unit_of_measure": "Cases"},
}

MANAGERS = {
    "M01": {"manager_name": "A. Kouamé", "team_name": "Equipe Abidjan", "role": "Zone Manager", "seniority_level": "Senior"},
    "M02": {"manager_name": "S. Diallo", "team_name": "Equipe Dakar", "role": "Zone Manager", "seniority_level": "Senior"},
    "M03": {"manager_name": "R. Mbarga", "team_name": "Equipe Douala", "role": "Zone Manager", "seniority_level": "Mid"},
    "M04": {"manager_name": "J. Kamau", "team_name": "Equipe Nairobi", "role": "Zone Manager", "seniority_level": "Senior"},
    "M05": {"manager_name": "P. Mukendi", "team_name": "Equipe Kinshasa", "role": "Zone Manager", "seniority_level": "Mid"},
    "M06": {"manager_name": "H. Benchekroun", "team_name": "Equipe Casablanca", "role": "Zone Manager", "seniority_level": "Mid"},
}

ZONE_MANAGER_MAP = {"Z01": "M01", "Z02": "M02", "Z03": "M03", "Z04": "M04", "Z05": "M05", "Z06": "M06"}

# Profils de performance par zone (taux de base)
ZONE_PERFORMANCE = {"Z01": 0.90, "Z02": 0.85, "Z03": 0.92, "Z04": 0.88, "Z05": 0.68, "Z06": 0.82}

# Niveaux d'activité par composante
COMP_BASELINES = {
    "C01": {"planned": 12, "benef": 480, "output": 12},
    "C02": {"planned": 8, "benef": 200, "output": 200},
    "C03": {"planned": 15, "benef": 0, "output": 15},
    "C04": {"planned": 10, "benef": 150, "output": 150},
}

BUDGET_BASELINES = {"C01": 2500000, "C02": 1800000, "C03": 2700000, "C04": 1600000}

# Saisonnalité (facteur multiplicatif par mois)
SEASONALITY = {1: 0.88, 2: 0.92, 3: 0.97, 4: 1.00, 5: 1.02, 6: 1.00, 7: 0.95, 8: 0.90, 9: 0.98, 10: 1.03, 11: 1.00, 12: 0.82}


def clamp(val, lo, hi):
    return max(lo, min(hi, val))


def write_csv(filepath, fieldnames, rows):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"  ✓ {os.path.basename(filepath)} : {len(rows)} lignes")


def generate_dim_calendar():
    month_names = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
                   7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
    month_abr = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
                 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
    rows = []
    for d in DATE_RANGE:
        y, m, _ = d.split("-")
        y, m = int(y), int(m)
        rows.append({
            "date_key": d, "year": y, "quarter": f"Q{(m - 1) // 3 + 1}",
            "month_number": m, "month_name": month_names[m],
            "month_label": f"{month_abr[m]} {y}", "year_month": f"{y}-{m:02d}"
        })
    write_csv(os.path.join(OUTPUT_DIR, "dim_calendar.csv"),
              ["date_key", "year", "quarter", "month_number", "month_name", "month_label", "year_month"], rows)


def generate_dim_zone():
    rows = [{"zone_id": k, **v} for k, v in ZONES.items()]
    write_csv(os.path.join(OUTPUT_DIR, "dim_zone.csv"),
              ["zone_id", "zone_name", "region_group", "site_count", "population_coverage_estimate", "zone_priority_level"], rows)


def generate_dim_program_component():
    rows = [{"component_id": k, **v} for k, v in COMPONENTS.items()]
    write_csv(os.path.join(OUTPUT_DIR, "dim_program_component.csv"),
              ["component_id", "component_name", "activity_type", "strategic_axis", "unit_of_measure"], rows)


def generate_dim_manager():
    rows = [{"manager_id": k, **v} for k, v in MANAGERS.items()]
    write_csv(os.path.join(OUTPUT_DIR, "dim_manager.csv"),
              ["manager_id", "manager_name", "team_name", "role", "seniority_level"], rows)


def generate_fact_monthly_performance():
    rows = []
    for date_key in DATE_RANGE:
        month_num = int(date_key.split("-")[1])
        season = SEASONALITY[month_num]
        idx = DATE_RANGE.index(date_key)
        trend = 1.0 + idx * 0.003

        for zone_id in ZONES:
            base = ZONE_PERFORMANCE[zone_id]
            mgr = ZONE_MANAGER_MAP[zone_id]

            for comp_id in COMPONENTS:
                bl = COMP_BASELINES[comp_id]
                rate = clamp(base * season * trend + random.gauss(0, 0.05), 0.40, 1.0)

                if comp_id == "C04" and zone_id == "Z05":
                    rate = max(0.35, rate - idx * 0.015)

                planned = max(4, bl["planned"] + random.randint(-1, 2))
                completed = max(1, round(planned * rate))
                t_benef = max(0, bl["benef"] + random.randint(-20, 29)) if bl["benef"] > 0 else 0
                a_benef = max(0, round(t_benef * clamp(rate + random.gauss(0, 0.05), 0.3, 1.0))) if t_benef > 0 else 0
                t_output = max(1, bl["output"] + random.randint(-1, 2))
                a_output = max(1, round(t_output * clamp(rate + random.gauss(0, 0.04), 0.3, 1.0)))
                rpt_exp = 4
                rpt_sub = random.choice([3, 4, 4, 4]) if rate > 0.75 else random.choice([2, 3, 3, 4])
                rpt_ot = min(rpt_sub, max(1, round(rpt_exp * clamp(rate + random.gauss(0, 0.08), 0.25, 1.0))))
                o_iss = random.randint(1, 3) if rate > 0.80 else random.randint(3, 7)
                c_iss = max(0, round(o_iss * min(1.0, rate + 0.1)))
                alerts = 0 if rate > 0.85 else (random.randint(1, 2) if rate > 0.70 else random.randint(2, 4))

                rows.append({
                    "date_key": date_key, "zone_id": zone_id, "component_id": comp_id, "manager_id": mgr,
                    "planned_activities": planned, "completed_activities": completed,
                    "target_beneficiaries": t_benef, "actual_beneficiaries": a_benef,
                    "target_output_units": t_output, "actual_output_units": a_output,
                    "reports_expected": rpt_exp, "reports_submitted": rpt_sub, "reports_submitted_on_time": rpt_ot,
                    "open_issues": o_iss, "closed_issues": c_iss, "high_priority_alerts": alerts,
                })

    fields = ["date_key", "zone_id", "component_id", "manager_id",
              "planned_activities", "completed_activities", "target_beneficiaries", "actual_beneficiaries",
              "target_output_units", "actual_output_units", "reports_expected", "reports_submitted",
              "reports_submitted_on_time", "open_issues", "closed_issues", "high_priority_alerts"]
    write_csv(os.path.join(OUTPUT_DIR, "fact_monthly_performance.csv"), fields, rows)


def generate_fact_budget():
    rows = []
    for date_key in DATE_RANGE:
        idx = DATE_RANGE.index(date_key)
        for zone_id in ZONES:
            base = ZONE_PERFORMANCE[zone_id]
            for comp_id in COMPONENTS:
                planned = BUDGET_BASELINES[comp_id] + random.randint(-100000, 149999)
                exec_rate = clamp(base + random.gauss(0, 0.06), 0.60, 1.15)
                if comp_id == "C04" and zone_id == "Z05":
                    exec_rate = min(1.25, 0.95 + idx * 0.02 + random.gauss(0, 0.03))
                spent = round(planned * exec_rate)
                committed = round(spent * (1.0 + random.uniform(0.01, 0.05)))
                var_amt = spent - planned
                var_pct = round((var_amt / planned) * 100, 1) if planned else 0

                rows.append({
                    "date_key": date_key, "zone_id": zone_id, "component_id": comp_id,
                    "planned_budget": planned, "spent_budget": spent, "committed_budget": committed,
                    "variance_amount": var_amt, "variance_percent": var_pct,
                })

    fields = ["date_key", "zone_id", "component_id",
              "planned_budget", "spent_budget", "committed_budget", "variance_amount", "variance_percent"]
    write_csv(os.path.join(OUTPUT_DIR, "fact_budget.csv"), fields, rows)


if __name__ == "__main__":
    print("Génération des données synthétiques...")
    print()
    generate_dim_calendar()
    generate_dim_zone()
    generate_dim_program_component()
    generate_dim_manager()
    generate_fact_monthly_performance()
    generate_fact_budget()
    print()
    print("Terminé. Tous les fichiers sont dans data/raw/")
