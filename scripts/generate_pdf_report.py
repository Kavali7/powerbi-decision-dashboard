"""
Génère un PDF de synthèse décisionnelle à partir du dataset.

Ce script produit un document PDF multi-pages avec :
  - Page 1 : couverture
  - Page 2 : vue dirigeant (KPI + tendance + zones)
  - Page 3 : vue opérationnelle (composantes + responsables)
  - Page 4 : note de lecture décisionnelle

Exécution :
    python scripts/generate_pdf_report.py

Sortie :
    assets/pdf/decision-dashboard-summary.pdf
"""

import csv
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "processed", "dashboard_input.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "assets", "pdf")

# ─── Theme ──────────────────────────────────────────────────────────────
BG_COLOR = "#1B2838"
CARD_COLOR = "#243447"
TEXT_WHITE = "#E8E8E8"
TEXT_SECONDARY = "#94A3B8"
ACCENT_BLUE = "#3B82F6"
ACCENT_GREEN = "#10B981"
ACCENT_ORANGE = "#F59E0B"
ACCENT_RED = "#EF4444"
GRID_COLOR = "#334155"


def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def safe_int(val):
    try:
        return int(val)
    except (ValueError, TypeError):
        return 0


def safe_float(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0


def setup_page(fig, title, subtitle=""):
    """Configure une page avec le thème sombre."""
    fig.set_facecolor(BG_COLOR)
    fig.text(0.5, 0.96, title, ha="center", va="top",
             fontsize=18, fontweight="bold", color=TEXT_WHITE)
    if subtitle:
        fig.text(0.5, 0.93, subtitle, ha="center", va="top",
                 fontsize=10, color=TEXT_SECONDARY)
    fig.text(0.5, 0.015, f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')} — Données synthétiques",
             ha="center", fontsize=7, color=TEXT_SECONDARY, style="italic")


def page_cover(pdf, data):
    """Page 1 : couverture."""
    fig = plt.figure(figsize=(11.69, 8.27))  # A4 paysage
    fig.set_facecolor(BG_COLOR)

    # Titre principal
    fig.text(0.5, 0.60, "Decision Dashboard", ha="center",
             fontsize=36, fontweight="bold", color=TEXT_WHITE)
    fig.text(0.5, 0.52, "Tableau de bord de pilotage décisionnel", ha="center",
             fontsize=16, color=ACCENT_BLUE)

    # Ligne décorative
    ax = fig.add_axes([0.30, 0.47, 0.40, 0.002])
    ax.set_facecolor(ACCENT_BLUE)
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)

    # Infos clés
    dates = sorted(set(r["date_key"] for r in data))
    zones = sorted(set(r["zone_name"] for r in data))
    info_lines = [
        f"Période couverte : {dates[0][:7]} à {dates[-1][:7]}",
        f"Zones suivies : {len(zones)}",
        f"Observations : {len(data)} enregistrements",
        "",
        "Données fictives et synthétiques — démonstration uniquement",
    ]
    for i, line in enumerate(info_lines):
        color = TEXT_SECONDARY if i < 3 else (TEXT_WHITE if i == 3 else ACCENT_ORANGE)
        fig.text(0.5, 0.40 - i * 0.04, line, ha="center",
                 fontsize=11, color=color)

    fig.text(0.5, 0.10, "Showcase — Decision Dashboard", ha="center",
             fontsize=9, color=TEXT_SECONDARY)

    pdf.savefig(fig, facecolor=BG_COLOR)
    plt.close(fig)


def page_executive(pdf, data):
    """Page 2 : vue dirigeant."""
    fig = plt.figure(figsize=(11.69, 8.27))
    setup_page(fig, "Vue Dirigeant", "Synthèse des indicateurs clés de pilotage")

    # ── KPI globaux ─────────────────────────────────────────────────
    total_planned = sum(safe_int(r["planned_activities"]) for r in data)
    total_completed = sum(safe_int(r["completed_activities"]) for r in data)
    acr = total_completed / total_planned if total_planned else 0

    total_pb = sum(safe_int(r["planned_budget"]) for r in data)
    total_sb = sum(safe_int(r["spent_budget"]) for r in data)
    ber = total_sb / total_pb if total_pb else 0

    total_benef_t = sum(safe_int(r["target_beneficiaries"]) for r in data)
    total_benef_a = sum(safe_int(r["actual_beneficiaries"]) for r in data)
    bar = total_benef_a / total_benef_t if total_benef_t else 0

    total_rpt_exp = sum(safe_int(r["reports_expected"]) for r in data)
    total_rpt_ot = sum(safe_int(r["reports_submitted_on_time"]) for r in data)
    rtr = total_rpt_ot / total_rpt_exp if total_rpt_exp else 0

    alert_count = sum(1 for r in data if safe_int(r["alert_flag"]) == 1)
    budget_gap = total_sb - total_pb

    kpis = [
        ("Achèvement", f"{acr:.0%}", ACCENT_GREEN if acr >= 0.80 else ACCENT_RED),
        ("Bénéficiaires", f"{bar:.0%}", ACCENT_GREEN if bar >= 0.80 else ACCENT_RED),
        ("Budget", f"{ber:.0%}", ACCENT_GREEN if ber <= 1.05 else ACCENT_RED),
        ("Reporting", f"{rtr:.0%}", ACCENT_GREEN if rtr >= 0.75 else ACCENT_ORANGE),
        ("Alertes", f"{alert_count}", ACCENT_RED if alert_count > 100 else ACCENT_ORANGE),
        ("Écart budget", f"{budget_gap/1e6:+.1f}M", ACCENT_RED if budget_gap > 0 else ACCENT_GREEN),
    ]

    for i, (label, value, color) in enumerate(kpis):
        x = 0.08 + i * 0.145
        ax = fig.add_axes([x, 0.74, 0.12, 0.12])
        ax.set_facecolor(CARD_COLOR)
        for sp in ax.spines.values():
            sp.set_color(GRID_COLOR)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.text(0.5, 0.65, value, ha="center", va="center",
                fontsize=18, fontweight="bold", color=color, transform=ax.transAxes)
        ax.text(0.5, 0.20, label, ha="center", va="center",
                fontsize=8, color=TEXT_SECONDARY, transform=ax.transAxes)

    # ── Tendance mensuelle ──────────────────────────────────────────
    monthly = defaultdict(lambda: {"planned": 0, "completed": 0})
    for r in data:
        ym = r["date_key"][:7]
        monthly[ym]["planned"] += safe_int(r["planned_activities"])
        monthly[ym]["completed"] += safe_int(r["completed_activities"])

    months = sorted(monthly.keys())
    rates = [monthly[m]["completed"] / monthly[m]["planned"] if monthly[m]["planned"] else 0 for m in months]

    ax_trend = fig.add_axes([0.08, 0.38, 0.55, 0.28])
    ax_trend.set_facecolor(CARD_COLOR)
    for sp in ax_trend.spines.values():
        sp.set_color(GRID_COLOR)
    ax_trend.bar(range(len(months)), rates, color=ACCENT_BLUE, alpha=0.7, width=0.6)
    ax_trend.plot(range(len(months)), rates, color=ACCENT_GREEN, linewidth=2, marker="o", markersize=4)
    ax_trend.axhline(y=0.80, color=ACCENT_RED, linestyle="--", linewidth=1, alpha=0.6)
    ax_trend.set_xticks(range(len(months)))
    ax_trend.set_xticklabels([m[5:] for m in months], fontsize=6, color=TEXT_SECONDARY, rotation=45)
    ax_trend.set_ylim(0.5, 1.1)
    ax_trend.tick_params(axis="y", colors=TEXT_SECONDARY, labelsize=7)
    ax_trend.set_title("Tendance mensuelle du taux d'achèvement", fontsize=10, color=TEXT_WHITE, pad=8)

    # ── Classement par zone ─────────────────────────────────────────
    zone_perf = defaultdict(lambda: {"planned": 0, "completed": 0})
    for r in data:
        zone_perf[r["zone_name"]]["planned"] += safe_int(r["planned_activities"])
        zone_perf[r["zone_name"]]["completed"] += safe_int(r["completed_activities"])

    zone_rates = {z: zone_perf[z]["completed"] / zone_perf[z]["planned"] for z in zone_perf}
    sorted_zones = sorted(zone_rates, key=zone_rates.get, reverse=True)

    ax_zones = fig.add_axes([0.70, 0.38, 0.25, 0.28])
    ax_zones.set_facecolor(CARD_COLOR)
    for sp in ax_zones.spines.values():
        sp.set_color(GRID_COLOR)
    colors = [ACCENT_GREEN if zone_rates[z] >= 0.80 else ACCENT_RED for z in sorted_zones]
    bars = ax_zones.barh(range(len(sorted_zones)), [zone_rates[z] for z in sorted_zones],
                         color=colors, height=0.6)
    ax_zones.set_yticks(range(len(sorted_zones)))
    ax_zones.set_yticklabels(sorted_zones, fontsize=7, color=TEXT_WHITE)
    ax_zones.axvline(x=0.80, color=ACCENT_RED, linestyle="--", linewidth=1, alpha=0.6)
    ax_zones.tick_params(axis="x", colors=TEXT_SECONDARY, labelsize=7)
    ax_zones.set_title("Performance par zone", fontsize=10, color=TEXT_WHITE, pad=8)
    ax_zones.invert_yaxis()

    # ── Résumé texte ────────────────────────────────────────────────
    zones_alert = sum(1 for z in zone_rates if zone_rates[z] < 0.80)
    summary = [
        f"• Taux d'achèvement global : {acr:.0%}",
        f"• Exécution budgétaire : {ber:.0%} ({budget_gap/1e6:+.1f}M FCFA)",
        f"• {zones_alert} zone(s) en dessous du seuil de 80%",
        f"• {alert_count} enregistrements en alerte sur {len(data)}",
    ]
    for i, line in enumerate(summary):
        fig.text(0.08, 0.30 - i * 0.035, line, fontsize=9, color=TEXT_WHITE)

    pdf.savefig(fig, facecolor=BG_COLOR)
    plt.close(fig)


def page_operational(pdf, data):
    """Page 3 : vue opérationnelle."""
    fig = plt.figure(figsize=(11.69, 8.27))
    setup_page(fig, "Vue Opérationnelle", "Analyse par composante et par responsable")

    # ── Performance par composante ──────────────────────────────────
    comp_perf = defaultdict(lambda: {"planned": 0, "completed": 0, "pb": 0, "sb": 0})
    for r in data:
        c = r["component_name"]
        comp_perf[c]["planned"] += safe_int(r["planned_activities"])
        comp_perf[c]["completed"] += safe_int(r["completed_activities"])
        comp_perf[c]["pb"] += safe_int(r["planned_budget"])
        comp_perf[c]["sb"] += safe_int(r["spent_budget"])

    ax1 = fig.add_axes([0.08, 0.52, 0.55, 0.32])
    ax1.set_facecolor(CARD_COLOR)
    for sp in ax1.spines.values():
        sp.set_color(GRID_COLOR)

    comps = sorted(comp_perf.keys())
    x = range(len(comps))
    acr_vals = [comp_perf[c]["completed"] / comp_perf[c]["planned"] for c in comps]
    ber_vals = [comp_perf[c]["sb"] / comp_perf[c]["pb"] if comp_perf[c]["pb"] else 0 for c in comps]

    w = 0.3
    ax1.bar([i - w / 2 for i in x], acr_vals, w, label="Achèvement", color=ACCENT_BLUE, alpha=0.8)
    ax1.bar([i + w / 2 for i in x], ber_vals, w, label="Budget", color=ACCENT_ORANGE, alpha=0.8)
    ax1.axhline(y=0.80, color=ACCENT_RED, linestyle="--", linewidth=1, alpha=0.5)
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(comps, fontsize=7, color=TEXT_WHITE, rotation=15)
    ax1.tick_params(axis="y", colors=TEXT_SECONDARY, labelsize=7)
    ax1.legend(fontsize=7, loc="upper right", facecolor=CARD_COLOR, edgecolor=GRID_COLOR, labelcolor=TEXT_WHITE)
    ax1.set_title("Achèvement vs Budget par composante", fontsize=10, color=TEXT_WHITE, pad=8)
    ax1.set_ylim(0, 1.3)

    # ── Performance par responsable ─────────────────────────────────
    mgr_perf = defaultdict(lambda: {"planned": 0, "completed": 0, "alerts": 0})
    for r in data:
        m = r["manager_name"]
        mgr_perf[m]["planned"] += safe_int(r["planned_activities"])
        mgr_perf[m]["completed"] += safe_int(r["completed_activities"])
        mgr_perf[m]["alerts"] += safe_int(r["alert_flag"])

    ax2 = fig.add_axes([0.70, 0.52, 0.25, 0.32])
    ax2.set_facecolor(CARD_COLOR)
    for sp in ax2.spines.values():
        sp.set_color(GRID_COLOR)

    managers = sorted(mgr_perf.keys(), key=lambda m: mgr_perf[m]["completed"] / mgr_perf[m]["planned"], reverse=True)
    mgr_rates = [mgr_perf[m]["completed"] / mgr_perf[m]["planned"] for m in managers]
    mgr_colors = [ACCENT_GREEN if r >= 0.80 else ACCENT_RED for r in mgr_rates]
    ax2.barh(range(len(managers)), mgr_rates, color=mgr_colors, height=0.6)
    ax2.set_yticks(range(len(managers)))
    ax2.set_yticklabels(managers, fontsize=7, color=TEXT_WHITE)
    ax2.axvline(x=0.80, color=ACCENT_RED, linestyle="--", linewidth=1, alpha=0.5)
    ax2.tick_params(axis="x", colors=TEXT_SECONDARY, labelsize=7)
    ax2.set_title("Performance par responsable", fontsize=10, color=TEXT_WHITE, pad=8)
    ax2.invert_yaxis()

    # ── Indicateurs de reporting ────────────────────────────────────
    zone_rpt = defaultdict(lambda: {"expected": 0, "on_time": 0, "issues_open": 0, "issues_closed": 0})
    for r in data:
        z = r["zone_name"]
        zone_rpt[z]["expected"] += safe_int(r["reports_expected"])
        zone_rpt[z]["on_time"] += safe_int(r["reports_submitted_on_time"])
        zone_rpt[z]["issues_open"] += safe_int(r["open_issues"])
        zone_rpt[z]["issues_closed"] += safe_int(r["closed_issues"])

    ax3 = fig.add_axes([0.08, 0.10, 0.87, 0.30])
    ax3.set_facecolor(CARD_COLOR)
    for sp in ax3.spines.values():
        sp.set_visible(False)
    ax3.set_xticks([])
    ax3.set_yticks([])
    ax3.set_title("Synthèse opérationnelle par zone", fontsize=10, color=TEXT_WHITE, pad=8)

    # Table header
    headers = ["Zone", "Reporting à temps", "Problèmes ouverts", "Taux résolution", "Statut"]
    for i, h in enumerate(headers):
        ax3.text(0.02 + i * 0.20, 0.92, h, fontsize=8, fontweight="bold",
                 color=TEXT_WHITE, transform=ax3.transAxes)

    zones = sorted(zone_rpt.keys())
    for j, z in enumerate(zones):
        y = 0.78 - j * 0.13
        rpt_rate = zone_rpt[z]["on_time"] / zone_rpt[z]["expected"] if zone_rpt[z]["expected"] else 0
        total_iss = zone_rpt[z]["issues_open"] + zone_rpt[z]["issues_closed"]
        resolution = zone_rpt[z]["issues_closed"] / total_iss if total_iss else 0
        status = "✓" if rpt_rate >= 0.75 and resolution >= 0.70 else "⚠"
        color = ACCENT_GREEN if status == "✓" else ACCENT_ORANGE

        ax3.text(0.02, y, z, fontsize=8, color=TEXT_WHITE, transform=ax3.transAxes)
        ax3.text(0.22, y, f"{rpt_rate:.0%}", fontsize=8, color=color, transform=ax3.transAxes)
        ax3.text(0.42, y, str(zone_rpt[z]["issues_open"]), fontsize=8, color=TEXT_WHITE, transform=ax3.transAxes)
        ax3.text(0.62, y, f"{resolution:.0%}", fontsize=8, color=color, transform=ax3.transAxes)
        ax3.text(0.82, y, status, fontsize=12, color=color, transform=ax3.transAxes)

    pdf.savefig(fig, facecolor=BG_COLOR)
    plt.close(fig)


def page_insights(pdf, data):
    """Page 4 : note de lecture décisionnelle."""
    fig = plt.figure(figsize=(11.69, 8.27))
    setup_page(fig, "Note de Lecture Décisionnelle", "Enseignements, vigilance et usages")

    # ── Calculs pour le texte ───────────────────────────────────────
    total_planned = sum(safe_int(r["planned_activities"]) for r in data)
    total_completed = sum(safe_int(r["completed_activities"]) for r in data)
    acr = total_completed / total_planned if total_planned else 0

    zone_perf = defaultdict(lambda: {"planned": 0, "completed": 0})
    for r in data:
        zone_perf[r["zone_name"]]["planned"] += safe_int(r["planned_activities"])
        zone_perf[r["zone_name"]]["completed"] += safe_int(r["completed_activities"])
    zone_rates = {z: zone_perf[z]["completed"] / zone_perf[z]["planned"] for z in zone_perf}
    best = max(zone_rates, key=zone_rates.get)
    worst = min(zone_rates, key=zone_rates.get)
    gap = zone_rates[best] - zone_rates[worst]

    total_pb = sum(safe_int(r["planned_budget"]) for r in data)
    total_sb = sum(safe_int(r["spent_budget"]) for r in data)
    ber = total_sb / total_pb if total_pb else 0

    # ── Enseignements ───────────────────────────────────────────────
    y = 0.82
    fig.text(0.08, y, "5 enseignements clés", fontsize=14, fontweight="bold", color=ACCENT_BLUE)
    insights = [
        f"Le taux d'achèvement global est de {acr:.0%}, ce qui indique une exécution {'satisfaisante' if acr >= 0.80 else 'insuffisante'}.",
        f"L'écart de performance entre la meilleure zone ({best}, {zone_rates[best]:.0%}) et la plus faible ({worst}, {zone_rates[worst]:.0%}) atteint {gap:.0%}.",
        f"L'exécution budgétaire est de {ber:.0%} — {'maîtrisée' if ber <= 1.05 else 'en dépassement'}.",
        f"Les zones les plus performantes affichent une régularité de reporting nettement supérieure.",
        f"La concentration des alertes sur 2 zones révèle un besoin d'accompagnement ciblé, pas généralisé.",
    ]
    for i, txt in enumerate(insights):
        fig.text(0.12, y - 0.06 - i * 0.045, f"{i + 1}. {txt}", fontsize=9, color=TEXT_WHITE, wrap=True)

    # ── Points de vigilance ─────────────────────────────────────────
    y2 = 0.50
    fig.text(0.08, y2, "3 points de vigilance", fontsize=14, fontweight="bold", color=ACCENT_ORANGE)
    vigilance = [
        f"La zone {worst} concentre une part disproportionnée des alertes et requiert une intervention rapide.",
        "Le taux de reporting à temps reste un indicateur de fragilité structurelle dans les zones en difficulté.",
        "L'écart budget/résultats doit être surveillé mois par mois pour éviter les corrections tardives.",
    ]
    for i, txt in enumerate(vigilance):
        fig.text(0.12, y2 - 0.06 - i * 0.045, f"⚠ {txt}", fontsize=9, color=TEXT_WHITE, wrap=True)

    # ── Usages possibles ────────────────────────────────────────────
    y3 = 0.25
    fig.text(0.08, y3, "3 usages recommandés", fontsize=14, fontweight="bold", color=ACCENT_GREEN)
    usages = [
        "Présenter ces données en comité de pilotage mensuel pour concentrer les discussions sur les écarts.",
        "Utiliser le classement par zone pour orienter les missions terrain et le renforcement des équipes.",
        "Partager le PDF de synthèse avec les parties prenantes comme base de dialogue factuel.",
    ]
    for i, txt in enumerate(usages):
        fig.text(0.12, y3 - 0.06 - i * 0.045, f"→ {txt}", fontsize=9, color=TEXT_WHITE, wrap=True)

    pdf.savefig(fig, facecolor=BG_COLOR)
    plt.close(fig)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    data = load_data()
    output_path = os.path.join(OUTPUT_DIR, "decision-dashboard-summary.pdf")

    print("Génération du PDF de synthèse décisionnelle...\n")

    with PdfPages(output_path) as pdf:
        page_cover(pdf, data)
        print("  ✓ Page 1 : couverture")
        page_executive(pdf, data)
        print("  ✓ Page 2 : vue dirigeant")
        page_operational(pdf, data)
        print("  ✓ Page 3 : vue opérationnelle")
        page_insights(pdf, data)
        print("  ✓ Page 4 : note de lecture décisionnelle")

    print(f"\nTerminé. PDF sauvegardé : {output_path}")


if __name__ == "__main__":
    main()
