"""
Préparation du dataset consolidé pour Power BI.

Ce script fusionne les tables dimensionnelles et factuelles,
calcule les indicateurs dérivés, et produit le fichier
dashboard_input.csv prêt à charger dans Power BI.

Exécution :
    python scripts/prepare_dashboard_input.py

Prérequis :
    Les fichiers suivants doivent exister dans data/raw/ :
    - dim_calendar.csv
    - dim_zone.csv
    - dim_program_component.csv
    - dim_manager.csv
    - fact_monthly_performance.csv
    - fact_budget.csv
"""

import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "processed")


def load_csv(filename):
    filepath = os.path.join(RAW_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_as_dict(filename, key_field):
    rows = load_csv(filename)
    return {row[key_field]: row for row in rows}


def main():
    print("Chargement des tables dimensionnelles...")
    cal = load_as_dict("dim_calendar.csv", "date_key")
    zones = load_as_dict("dim_zone.csv", "zone_id")
    comps = load_as_dict("dim_program_component.csv", "component_id")
    mgrs = load_as_dict("dim_manager.csv", "manager_id")

    print("Chargement des tables factuelles...")
    perf = load_csv("fact_monthly_performance.csv")
    budget_rows = load_csv("fact_budget.csv")

    # Index budget par (date_key, zone_id, component_id)
    budget_map = {}
    for b in budget_rows:
        key = (b["date_key"], b["zone_id"], b["component_id"])
        budget_map[key] = b

    print("Fusion et calcul des indicateurs...")
    output_fields = [
        "date_key", "year", "quarter", "month_number", "month_name", "month_label", "year_month",
        "zone_id", "zone_name", "region_group", "site_count", "population_coverage_estimate", "zone_priority_level",
        "component_id", "component_name", "activity_type", "strategic_axis", "unit_of_measure",
        "manager_id", "manager_name", "team_name", "role", "seniority_level",
        "planned_activities", "completed_activities", "target_beneficiaries", "actual_beneficiaries",
        "target_output_units", "actual_output_units",
        "reports_expected", "reports_submitted", "reports_submitted_on_time",
        "open_issues", "closed_issues", "high_priority_alerts",
        "planned_budget", "spent_budget", "committed_budget", "variance_amount", "variance_percent",
        "activity_completion_rate", "beneficiary_achievement_rate", "output_achievement_rate",
        "reporting_on_time_rate", "budget_execution_rate", "alert_flag"
    ]

    output_rows = []
    for p in perf:
        c = cal.get(p["date_key"], {})
        z = zones.get(p["zone_id"], {})
        comp = comps.get(p["component_id"], {})
        m = mgrs.get(p["manager_id"], {})
        bk = (p["date_key"], p["zone_id"], p["component_id"])
        b = budget_map.get(bk, {})

        planned_act = int(p["planned_activities"])
        completed_act = int(p["completed_activities"])
        target_ben = int(p["target_beneficiaries"])
        actual_ben = int(p["actual_beneficiaries"])
        target_out = int(p["target_output_units"])
        actual_out = int(p["actual_output_units"])
        rpt_exp = int(p["reports_expected"])
        rpt_ot = int(p["reports_submitted_on_time"])
        high_alerts = int(p["high_priority_alerts"])
        planned_bud = int(b.get("planned_budget", 0))
        spent_bud = int(b.get("spent_budget", 0))

        acr = round(completed_act / planned_act, 4) if planned_act else 0
        bar_ = round(actual_ben / target_ben, 4) if target_ben > 0 else ""
        oar = round(actual_out / target_out, 4) if target_out else 0
        rtr = round(rpt_ot / rpt_exp, 4) if rpt_exp else 0
        ber = round(spent_bud / planned_bud, 4) if planned_bud else 0

        alert = 1 if (
            acr < 0.80 or
            (bar_ != "" and bar_ < 0.80) or
            ber > 1.05 or
            rtr < 0.75 or
            high_alerts >= 2
        ) else 0

        row = {
            "date_key": p["date_key"],
            "year": c.get("year", ""), "quarter": c.get("quarter", ""),
            "month_number": c.get("month_number", ""), "month_name": c.get("month_name", ""),
            "month_label": c.get("month_label", ""), "year_month": c.get("year_month", ""),
            "zone_id": p["zone_id"],
            "zone_name": z.get("zone_name", ""), "region_group": z.get("region_group", ""),
            "site_count": z.get("site_count", ""), "population_coverage_estimate": z.get("population_coverage_estimate", ""),
            "zone_priority_level": z.get("zone_priority_level", ""),
            "component_id": p["component_id"],
            "component_name": comp.get("component_name", ""), "activity_type": comp.get("activity_type", ""),
            "strategic_axis": comp.get("strategic_axis", ""), "unit_of_measure": comp.get("unit_of_measure", ""),
            "manager_id": p["manager_id"],
            "manager_name": m.get("manager_name", ""), "team_name": m.get("team_name", ""),
            "role": m.get("role", ""), "seniority_level": m.get("seniority_level", ""),
            "planned_activities": planned_act, "completed_activities": completed_act,
            "target_beneficiaries": target_ben, "actual_beneficiaries": actual_ben,
            "target_output_units": target_out, "actual_output_units": actual_out,
            "reports_expected": rpt_exp, "reports_submitted": p["reports_submitted"],
            "reports_submitted_on_time": rpt_ot, "open_issues": p["open_issues"],
            "closed_issues": p["closed_issues"], "high_priority_alerts": high_alerts,
            "planned_budget": b.get("planned_budget", ""), "spent_budget": b.get("spent_budget", ""),
            "committed_budget": b.get("committed_budget", ""), "variance_amount": b.get("variance_amount", ""),
            "variance_percent": b.get("variance_percent", ""),
            "activity_completion_rate": acr, "beneficiary_achievement_rate": bar_,
            "output_achievement_rate": oar, "reporting_on_time_rate": rtr,
            "budget_execution_rate": ber, "alert_flag": alert,
        }
        output_rows.append(row)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, "dashboard_input.csv")
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=output_fields)
        w.writeheader()
        w.writerows(output_rows)

    print(f"\n✓ dashboard_input.csv : {len(output_rows)} lignes")
    print(f"  Fichier créé dans : {output_path}")


if __name__ == "__main__":
    main()
