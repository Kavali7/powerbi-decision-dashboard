"""
Validation QA du dataset et des livrables du dashboard.

Ce script vérifie la cohérence structurelle et métier de l'ensemble
du pipeline de données et des visuels générés.

Exécution :
    python scripts/validate_outputs.py

Tous les tests doivent passer avant publication.
"""

import csv
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
CHARTS_DIR = os.path.join(BASE_DIR, "assets", "charts")

passed = 0
failed = 0


def check(description, condition):
    global passed, failed
    if condition:
        print(f"  PASS  {description}")
        passed += 1
    else:
        print(f"  FAIL  {description}")
        failed += 1


def load_csv(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    print("=" * 60)
    print("  Validation QA — Decision Dashboard Showcase")
    print("=" * 60)
    print()

    # ─── 1. Fichiers CSV présents ────────────────────────────────
    print("1. Présence des fichiers CSV")
    raw_files = [
        "dim_calendar.csv", "dim_zone.csv",
        "dim_program_component.csv", "dim_manager.csv",
        "fact_monthly_performance.csv", "fact_budget.csv",
    ]
    for f in raw_files:
        check(f"data/raw/{f} existe", os.path.exists(os.path.join(RAW_DIR, f)))
    check(
        "data/processed/dashboard_input.csv existe",
        os.path.exists(os.path.join(PROCESSED_DIR, "dashboard_input.csv")),
    )
    print()

    # ─── 2. Nombre de lignes ─────────────────────────────────────
    print("2. Nombre de lignes attendues")
    perf = load_csv(os.path.join(RAW_DIR, "fact_monthly_performance.csv"))
    budget = load_csv(os.path.join(RAW_DIR, "fact_budget.csv"))
    dashboard = load_csv(os.path.join(PROCESSED_DIR, "dashboard_input.csv"))

    check(f"fact_monthly_performance.csv = 360 lignes (trouvé: {len(perf)})", len(perf) == 360)
    check(f"fact_budget.csv = 360 lignes (trouvé: {len(budget)})", len(budget) == 360)
    check(f"dashboard_input.csv = 360 lignes (trouvé: {len(dashboard)})", len(dashboard) == 360)
    print()

    # ─── 3. Dimensions ───────────────────────────────────────────
    print("3. Dimensions du dataset")
    dates = sorted(set(r["date_key"] for r in dashboard))
    zones = sorted(set(r["zone_id"] for r in dashboard))
    zone_names = sorted(set(r["zone_name"] for r in dashboard))
    comps = sorted(set(r["component_id"] for r in dashboard))
    managers = sorted(set(r["manager_id"] for r in dashboard))

    check(f"15 mois distincts (trouvé: {len(dates)})", len(dates) == 15)
    check(f"Période commence en 2024-01 (trouvé: {dates[0]})", dates[0] == "2024-01-01")
    check(f"Période finit en 2025-03 (trouvé: {dates[-1]})", dates[-1] == "2025-03-01")
    check(f"6 zones distinctes (trouvé: {len(zones)})", len(zones) == 6)
    check(f"4 composantes distinctes (trouvé: {len(comps)})", len(comps) == 4)
    check(f"6 managers distincts (trouvé: {len(managers)})", len(managers) == 6)

    expected_zones = {"Abidjan-Plateau", "Dakar-Almadies", "Douala-Littoral",
                      "Nairobi-Westlands", "Kinshasa-Gombe", "Casablanca-Anfa"}
    check(f"Zones attendues présentes", set(zone_names) == expected_zones)
    print()

    # ─── 4. Cohérence métier ─────────────────────────────────────
    print("4. Cohérence métier")
    anomalies_act = 0
    anomalies_bud = 0
    alert_count = 0
    zones_en_alerte = set()

    for r in dashboard:
        planned = int(r["planned_activities"])
        completed = int(r["completed_activities"])
        if completed > planned * 1.5:
            anomalies_act += 1

        pb = int(r["planned_budget"]) if r["planned_budget"] else 0
        if pb < 0:
            anomalies_bud += 1

        if int(r["alert_flag"]) == 1:
            alert_count += 1
            zones_en_alerte.add(r["zone_name"])

    check(f"Aucune activité réalisée > 150% du planifié (anomalies: {anomalies_act})", anomalies_act == 0)
    check(f"Aucun budget planifié négatif (anomalies: {anomalies_bud})", anomalies_bud == 0)
    check(f"Alertes présentes dans les données ({alert_count} enregistrements)", alert_count > 0)
    check(f"Alertes ni trop rares ni omniprésentes ({alert_count}/360)", 20 < alert_count < 300)
    check(f"Au moins 2 zones en alerte (trouvé: {len(zones_en_alerte)})", len(zones_en_alerte) >= 2)
    print()

    # ─── 5. Taux calculés cohérents ──────────────────────────────
    print("5. Taux calculés")
    taux_ok = 0
    taux_total = 0
    for r in dashboard:
        planned = int(r["planned_activities"])
        completed = int(r["completed_activities"])
        acr = float(r["activity_completion_rate"])
        expected = round(completed / planned, 4) if planned else 0
        taux_total += 1
        if abs(acr - expected) < 0.001:
            taux_ok += 1

    check(f"activity_completion_rate cohérent ({taux_ok}/{taux_total})", taux_ok == taux_total)

    flag_ok = 0
    for r in dashboard:
        acr = float(r["activity_completion_rate"])
        bar_ = float(r["beneficiary_achievement_rate"]) if r["beneficiary_achievement_rate"] != "" else 1.0
        ber = float(r["budget_execution_rate"])
        rtr = float(r["reporting_on_time_rate"])
        ha = int(r["high_priority_alerts"])
        expected_flag = 1 if (acr < 0.80 or bar_ < 0.80 or ber > 1.05 or rtr < 0.75 or ha >= 2) else 0
        if int(r["alert_flag"]) == expected_flag:
            flag_ok += 1

    check(f"alert_flag cohérent avec les seuils KPI ({flag_ok}/{len(dashboard)})", flag_ok == len(dashboard))
    print()

    # ─── 6. Charts PNG présents ──────────────────────────────────
    print("6. Graphiques générés")
    charts = [
        "01-executive-overview.png",
        "02-performance-by-zone.png",
        "03-budget-vs-results.png",
        "04-alerts-table.png",
        "05-operational-view.png",
    ]
    for c in charts:
        path = os.path.join(CHARTS_DIR, c)
        exists = os.path.exists(path)
        size = os.path.getsize(path) if exists else 0
        check(f"assets/charts/{c} ({size:,} bytes)", exists and size > 10000)
    print()

    # ─── Résumé ──────────────────────────────────────────────────
    print("=" * 60)
    total = passed + failed
    if failed == 0:
        print(f"  ALL {total} CHECKS PASSED")
    else:
        print(f"  {passed}/{total} PASSED — {failed} FAILED")
    print("=" * 60)

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
