"""
Génère un PDF de synthèse décisionnelle à partir du dataset.

Ce script produit un document PDF 5 pages :
  - Page 1 : couverture
  - Page 2 : vue dirigeant (KPI + tendance + zones)
  - Page 3 : vue opérationnelle (composantes + responsables)
  - Page 4 : lecture décisionnelle synthétique
  - Page 5 : à propos de la démonstration

Exécution :
    python scripts/generate_pdf_summary.py

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

PAGE_W, PAGE_H = 11.69, 8.27  # A4 paysage


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


def footer(fig, page_num):
    """Pied de page standard."""
    fig.text(0.05, 0.015,
             f"Données synthétiques — démonstration uniquement | Généré le {datetime.now().strftime('%d/%m/%Y')}",
             fontsize=7, color=TEXT_SECONDARY, style="italic")
    fig.text(0.95, 0.015, f"{page_num}/5", ha="right", fontsize=7, color=TEXT_SECONDARY)


# ─── PAGE 1 : Couverture ────────────────────────────────────────────────

def page_cover(pdf, data):
    fig = plt.figure(figsize=(PAGE_W, PAGE_H))
    fig.set_facecolor(BG_COLOR)

    fig.text(0.5, 0.62, "Decision Dashboard Showcase", ha="center",
             fontsize=36, fontweight="bold", color=TEXT_WHITE)
    fig.text(0.5, 0.54, "Démonstration de tableau de bord décisionnel pour le pilotage d'activité",
             ha="center", fontsize=14, color=ACCENT_BLUE)

    # Ligne décorative
    ax = fig.add_axes([0.30, 0.49, 0.40, 0.002])
    ax.set_facecolor(ACCENT_BLUE)
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)

    dates = sorted(set(r["date_key"] for r in data))
    zones = set(r["zone_name"] for r in data)
    comps = set(r["component_name"] for r in data)
    managers = set(r["manager_name"] for r in data)

    info = [
        f"Période : janvier 2024 – mars 2025 ({len(dates)} mois)",
        f"{len(zones)} zones  ·  {len(comps)} composantes  ·  {len(managers)} responsables",
        f"{len(data)} observations",
    ]
    for i, line in enumerate(info):
        fig.text(0.5, 0.42 - i * 0.04, line, ha="center", fontsize=11, color=TEXT_SECONDARY)

    fig.text(0.5, 0.28, "Données synthétiques uniquement", ha="center",
             fontsize=10, fontweight="bold", color=ACCENT_ORANGE)

    fig.text(0.5, 0.08,
             "Ce document illustre une logique de restitution décisionnelle.\nIl ne correspond à aucun client réel.",
             ha="center", fontsize=9, color=TEXT_SECONDARY, style="italic", linespacing=1.6)

    footer(fig, 1)
    pdf.savefig(fig, facecolor=BG_COLOR)
    plt.close(fig)


# ─── PAGE 2 : Vue dirigeant ─────────────────────────────────────────────

def page_executive(pdf, data):
    fig = plt.figure(figsize=(PAGE_W, PAGE_H))
    fig.set_facecolor(BG_COLOR)
    fig.text(0.5, 0.96, "Vue Dirigeant", ha="center", fontsize=18,
             fontweight="bold", color=TEXT_WHITE)
    fig.text(0.5, 0.93, "Synthèse des indicateurs clés de pilotage", ha="center",
             fontsize=10, color=TEXT_SECONDARY)

    # ── KPI globaux ─────────────────────────────────────────────────
    tp = sum(safe_int(r["planned_activities"]) for r in data)
    tc = sum(safe_int(r["completed_activities"]) for r in data)
    acr = tc / tp if tp else 0

    tpb = sum(safe_int(r["planned_budget"]) for r in data)
    tsb = sum(safe_int(r["spent_budget"]) for r in data)
    ber = tsb / tpb if tpb else 0

    tbt = sum(safe_int(r["target_beneficiaries"]) for r in data)
    tba = sum(safe_int(r["actual_beneficiaries"]) for r in data)
    bar = tba / tbt if tbt else 0

    tre = sum(safe_int(r["reports_expected"]) for r in data)
    tro = sum(safe_int(r["reports_submitted_on_time"]) for r in data)
    rtr = tro / tre if tre else 0

    alert_count = sum(1 for r in data if safe_int(r["alert_flag"]) == 1)
    budget_gap = tsb - tpb

    kpis = [
        ("Achèvement", f"{acr:.0%}", ACCENT_GREEN if acr >= 0.80 else ACCENT_RED),
        ("Bénéficiaires", f"{bar:.0%}", ACCENT_GREEN if bar >= 0.80 else ACCENT_RED),
        ("Budget", f"{ber:.0%}", ACCENT_GREEN if ber <= 1.05 else ACCENT_RED),
        ("Reporting", f"{rtr:.0%}", ACCENT_GREEN if rtr >= 0.75 else ACCENT_ORANGE),
        ("Alertes", f"{alert_count}", ACCENT_RED if alert_count > 100 else ACCENT_ORANGE),
        ("Écart budget", f"{budget_gap / 1e6:+.1f}M", ACCENT_RED if budget_gap > 0 else ACCENT_GREEN),
    ]

    for i, (label, value, color) in enumerate(kpis):
        x = 0.06 + i * 0.15
        ax = fig.add_axes([x, 0.76, 0.12, 0.11])
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
    monthly = defaultdict(lambda: {"p": 0, "c": 0})
    for r in data:
        ym = r["date_key"][:7]
        monthly[ym]["p"] += safe_int(r["planned_activities"])
        monthly[ym]["c"] += safe_int(r["completed_activities"])

    months = sorted(monthly.keys())
    rates = [monthly[m]["c"] / monthly[m]["p"] if monthly[m]["p"] else 0 for m in months]

    ax_t = fig.add_axes([0.06, 0.38, 0.55, 0.30])
    ax_t.set_facecolor(CARD_COLOR)
    for sp in ax_t.spines.values():
        sp.set_color(GRID_COLOR)
    ax_t.bar(range(len(months)), rates, color=ACCENT_BLUE, alpha=0.7, width=0.6)
    ax_t.plot(range(len(months)), rates, color=ACCENT_GREEN, linewidth=2, marker="o", markersize=4)
    ax_t.axhline(y=0.80, color=ACCENT_RED, linestyle="--", linewidth=1, alpha=0.6)
    ax_t.set_xticks(range(len(months)))
    ax_t.set_xticklabels([m[5:] for m in months], fontsize=6, color=TEXT_SECONDARY, rotation=45)
    ax_t.set_ylim(0.5, 1.1)
    ax_t.tick_params(axis="y", colors=TEXT_SECONDARY, labelsize=7)
    ax_t.set_title("Tendance mensuelle du taux d'achèvement", fontsize=10, color=TEXT_WHITE, pad=8)

    # ── Classement par zone ─────────────────────────────────────────
    zp = defaultdict(lambda: {"p": 0, "c": 0})
    for r in data:
        zp[r["zone_name"]]["p"] += safe_int(r["planned_activities"])
        zp[r["zone_name"]]["c"] += safe_int(r["completed_activities"])
    zr = {z: zp[z]["c"] / zp[z]["p"] for z in zp}
    sz = sorted(zr, key=zr.get, reverse=True)

    ax_z = fig.add_axes([0.68, 0.38, 0.27, 0.30])
    ax_z.set_facecolor(CARD_COLOR)
    for sp in ax_z.spines.values():
        sp.set_color(GRID_COLOR)
    colors = [ACCENT_GREEN if zr[z] >= 0.80 else ACCENT_RED for z in sz]
    ax_z.barh(range(len(sz)), [zr[z] for z in sz], color=colors, height=0.6)
    ax_z.set_yticks(range(len(sz)))
    ax_z.set_yticklabels(sz, fontsize=7, color=TEXT_WHITE)
    ax_z.axvline(x=0.80, color=ACCENT_RED, linestyle="--", linewidth=1, alpha=0.6)
    ax_z.tick_params(axis="x", colors=TEXT_SECONDARY, labelsize=7)
    ax_z.set_title("Performance par zone", fontsize=10, color=TEXT_WHITE, pad=8)
    ax_z.invert_yaxis()

    # ── Texte de lecture ────────────────────────────────────────────
    zones_alert = sum(1 for z in zr if zr[z] < 0.80)
    reading = [
        "Ce que montre cette vue :",
        f"  · Niveau global d'exécution : {acr:.0%}",
        f"  · Tendance mensuelle sur 15 mois",
        f"  · {zones_alert} zone(s) en dessous du seuil de 80%",
        f"  · Discipline budgétaire : {ber:.0%}",
        f"  · {alert_count} situations d'alerte identifiées",
    ]
    for i, line in enumerate(reading):
        w = "bold" if i == 0 else "normal"
        fig.text(0.06, 0.30 - i * 0.035, line, fontsize=9, color=TEXT_WHITE, fontweight=w)

    footer(fig, 2)
    pdf.savefig(fig, facecolor=BG_COLOR)
    plt.close(fig)


# ─── PAGE 3 : Vue opérationnelle ────────────────────────────────────────

def page_operational(pdf, data):
    fig = plt.figure(figsize=(PAGE_W, PAGE_H))
    fig.set_facecolor(BG_COLOR)
    fig.text(0.5, 0.96, "Vue Opérationnelle", ha="center", fontsize=18,
             fontweight="bold", color=TEXT_WHITE)
    fig.text(0.5, 0.93, "Analyse par composante et par responsable", ha="center",
             fontsize=10, color=TEXT_SECONDARY)

    # ── Performance par composante ──────────────────────────────────
    cp = defaultdict(lambda: {"p": 0, "c": 0, "pb": 0, "sb": 0})
    for r in data:
        c = r["component_name"]
        cp[c]["p"] += safe_int(r["planned_activities"])
        cp[c]["c"] += safe_int(r["completed_activities"])
        cp[c]["pb"] += safe_int(r["planned_budget"])
        cp[c]["sb"] += safe_int(r["spent_budget"])

    ax1 = fig.add_axes([0.06, 0.52, 0.55, 0.32])
    ax1.set_facecolor(CARD_COLOR)
    for sp in ax1.spines.values():
        sp.set_color(GRID_COLOR)

    comps = sorted(cp.keys())
    x = range(len(comps))
    acr_v = [cp[c]["c"] / cp[c]["p"] for c in comps]
    ber_v = [cp[c]["sb"] / cp[c]["pb"] if cp[c]["pb"] else 0 for c in comps]

    w = 0.3
    ax1.bar([i - w / 2 for i in x], acr_v, w, label="Achèvement", color=ACCENT_BLUE, alpha=0.8)
    ax1.bar([i + w / 2 for i in x], ber_v, w, label="Exéc. budgétaire", color=ACCENT_ORANGE, alpha=0.8)
    ax1.axhline(y=0.80, color=ACCENT_RED, linestyle="--", linewidth=1, alpha=0.5)
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(comps, fontsize=7, color=TEXT_WHITE, rotation=15)
    ax1.tick_params(axis="y", colors=TEXT_SECONDARY, labelsize=7)
    ax1.legend(fontsize=7, loc="upper right", facecolor=CARD_COLOR, edgecolor=GRID_COLOR, labelcolor=TEXT_WHITE)
    ax1.set_title("Achèvement vs Budget par composante", fontsize=10, color=TEXT_WHITE, pad=8)
    ax1.set_ylim(0, 1.3)

    # ── Performance par responsable ─────────────────────────────────
    mp = defaultdict(lambda: {"p": 0, "c": 0, "a": 0})
    for r in data:
        m = r["manager_name"]
        mp[m]["p"] += safe_int(r["planned_activities"])
        mp[m]["c"] += safe_int(r["completed_activities"])
        mp[m]["a"] += safe_int(r["alert_flag"])

    ax2 = fig.add_axes([0.68, 0.52, 0.27, 0.32])
    ax2.set_facecolor(CARD_COLOR)
    for sp in ax2.spines.values():
        sp.set_color(GRID_COLOR)

    mgrs = sorted(mp.keys(), key=lambda m: mp[m]["c"] / mp[m]["p"], reverse=True)
    mr = [mp[m]["c"] / mp[m]["p"] for m in mgrs]
    mc = [ACCENT_GREEN if r >= 0.80 else ACCENT_RED for r in mr]
    ax2.barh(range(len(mgrs)), mr, color=mc, height=0.6)
    ax2.set_yticks(range(len(mgrs)))
    ax2.set_yticklabels(mgrs, fontsize=7, color=TEXT_WHITE)
    ax2.axvline(x=0.80, color=ACCENT_RED, linestyle="--", linewidth=1, alpha=0.5)
    ax2.tick_params(axis="x", colors=TEXT_SECONDARY, labelsize=7)
    ax2.set_title("Performance par responsable", fontsize=10, color=TEXT_WHITE, pad=8)
    ax2.invert_yaxis()

    # ── Synthèse reporting par zone ─────────────────────────────────
    zrpt = defaultdict(lambda: {"exp": 0, "ot": 0, "oi": 0, "ci": 0})
    for r in data:
        z = r["zone_name"]
        zrpt[z]["exp"] += safe_int(r["reports_expected"])
        zrpt[z]["ot"] += safe_int(r["reports_submitted_on_time"])
        zrpt[z]["oi"] += safe_int(r["open_issues"])
        zrpt[z]["ci"] += safe_int(r["closed_issues"])

    ax3 = fig.add_axes([0.06, 0.08, 0.89, 0.32])
    ax3.set_facecolor(CARD_COLOR)
    for sp in ax3.spines.values():
        sp.set_visible(False)
    ax3.set_xticks([])
    ax3.set_yticks([])
    ax3.set_title("Synthèse opérationnelle par zone", fontsize=10, color=TEXT_WHITE, pad=8)

    headers = ["Zone", "Reporting à temps", "Problèmes ouverts", "Taux résolution", "Statut"]
    for i, h in enumerate(headers):
        ax3.text(0.02 + i * 0.20, 0.92, h, fontsize=8, fontweight="bold",
                 color=TEXT_WHITE, transform=ax3.transAxes)

    zones = sorted(zrpt.keys())
    for j, z in enumerate(zones):
        y = 0.78 - j * 0.13
        rr = zrpt[z]["ot"] / zrpt[z]["exp"] if zrpt[z]["exp"] else 0
        ti = zrpt[z]["oi"] + zrpt[z]["ci"]
        res = zrpt[z]["ci"] / ti if ti else 0
        ok = rr >= 0.75 and res >= 0.70
        color = ACCENT_GREEN if ok else ACCENT_ORANGE
        status = "✓" if ok else "⚠"

        ax3.text(0.02, y, z, fontsize=8, color=TEXT_WHITE, transform=ax3.transAxes)
        ax3.text(0.22, y, f"{rr:.0%}", fontsize=8, color=color, transform=ax3.transAxes)
        ax3.text(0.42, y, str(zrpt[z]["oi"]), fontsize=8, color=TEXT_WHITE, transform=ax3.transAxes)
        ax3.text(0.62, y, f"{res:.0%}", fontsize=8, color=color, transform=ax3.transAxes)
        ax3.text(0.82, y, status, fontsize=12, color=color, transform=ax3.transAxes)

    fig.text(0.06, 0.42, "Ce que permet cette vue : comparer les composantes, suivre la performance par responsable, "
             "lire le reporting, repérer les problèmes ouverts.", fontsize=9, color=TEXT_SECONDARY, style="italic")

    footer(fig, 3)
    pdf.savefig(fig, facecolor=BG_COLOR)
    plt.close(fig)


# ─── PAGE 4 : Lecture décisionnelle synthétique ─────────────────────────

def page_insights(pdf, data):
    fig = plt.figure(figsize=(PAGE_W, PAGE_H))
    fig.set_facecolor(BG_COLOR)
    fig.text(0.5, 0.96, "Lecture Décisionnelle Synthétique", ha="center",
             fontsize=18, fontweight="bold", color=TEXT_WHITE)

    # ── Calculs ─────────────────────────────────────────────────────
    tp = sum(safe_int(r["planned_activities"]) for r in data)
    tc = sum(safe_int(r["completed_activities"]) for r in data)
    acr = tc / tp if tp else 0
    zp = defaultdict(lambda: {"p": 0, "c": 0})
    for r in data:
        zp[r["zone_name"]]["p"] += safe_int(r["planned_activities"])
        zp[r["zone_name"]]["c"] += safe_int(r["completed_activities"])
    zr = {z: zp[z]["c"] / zp[z]["p"] for z in zp}
    best = max(zr, key=zr.get)
    worst = min(zr, key=zr.get)

    # ── 5 Enseignements (gauche) ────────────────────────────────────
    y = 0.87
    fig.text(0.05, y, "5 enseignements clés", fontsize=13, fontweight="bold", color=ACCENT_BLUE)

    insights = [
        "La performance globale reste lisible, mais hétérogène selon les zones. "
        "Un pilotage par moyenne générale ne suffit pas.",
        "La tendance mensuelle permet de dépasser la photo statique "
        "et d'apprécier la dynamique récente.",
        f"La comparaison entre zones facilite la priorisation : "
        f"{best} ({zr[best]:.0%}) vs {worst} ({zr[worst]:.0%}).",
        "La relation entre résultats et budget doit être lue conjointement "
        "pour apprécier la cohérence des moyens mobilisés.",
        "Les alertes transforment le reporting en outil d'action, "
        "en mettant en avant les situations qui appellent une décision.",
    ]
    for i, txt in enumerate(insights):
        fig.text(0.07, y - 0.06 - i * 0.072, f"{i + 1}.",
                 fontsize=10, fontweight="bold", color=ACCENT_BLUE)
        fig.text(0.10, y - 0.06 - i * 0.072, txt,
                 fontsize=9, color=TEXT_WHITE, wrap=True)

    # ── 3 Vigilances (droite haut) ──────────────────────────────────
    y2 = 0.48
    fig.text(0.05, y2, "3 points de vigilance", fontsize=13, fontweight="bold", color=ACCENT_ORANGE)

    vigilance = [
        f"Surveiller les zones durablement sous les seuils attendus — "
        f"notamment {worst}.",
        "Contrôler les écarts entre dépense engagée et performance obtenue. "
        "Un budget consommé n'est pas un indicateur de performance.",
        "Ne pas traiter toutes les alertes au même niveau. "
        "La hiérarchisation des signaux est centrale.",
    ]
    for i, txt in enumerate(vigilance):
        fig.text(0.07, y2 - 0.055 - i * 0.065, "⚠",
                 fontsize=11, color=ACCENT_ORANGE)
        fig.text(0.10, y2 - 0.055 - i * 0.065, txt,
                 fontsize=9, color=TEXT_WHITE, wrap=True)

    # ── 3 Usages (bas) ─────────────────────────────────────────────
    y3 = 0.18
    fig.text(0.05, y3, "3 usages concrets", fontsize=13, fontweight="bold", color=ACCENT_GREEN)

    usages = [
        "Préparer une réunion mensuelle de pilotage avec une vision déjà structurée.",
        "Appuyer une coordination multi-zones sans multiplier les fichiers.",
        "Produire une synthèse claire pour une direction ou un bailleur.",
    ]
    for i, txt in enumerate(usages):
        fig.text(0.07, y3 - 0.045 - i * 0.045, "→",
                 fontsize=11, color=ACCENT_GREEN)
        fig.text(0.10, y3 - 0.045 - i * 0.045, txt,
                 fontsize=9, color=TEXT_WHITE)

    footer(fig, 4)
    pdf.savefig(fig, facecolor=BG_COLOR)
    plt.close(fig)


# ─── PAGE 5 : À propos de la démonstration ──────────────────────────────

def page_about(pdf, data):
    fig = plt.figure(figsize=(PAGE_W, PAGE_H))
    fig.set_facecolor(BG_COLOR)
    fig.text(0.5, 0.96, "À Propos de Cette Démonstration", ha="center",
             fontsize=18, fontweight="bold", color=TEXT_WHITE)

    y = 0.84
    sections = [
        ("Données synthétiques", ACCENT_ORANGE, [
            "Toutes les données de ce document sont fictives et synthétiques.",
            "Elles ont été générées par un script Python avec une graine reproductible (seed 42).",
            "Elles ne correspondent à aucun client réel, aucun projet réel et aucun résultat réel.",
        ]),
        ("Ce que contient le dépôt", ACCENT_BLUE, [
            "6 fichiers CSV source (4 dimensions + 2 tables de faits) — schéma en étoile.",
            "1 dataset consolidé de 360 observations (6 zones × 4 composantes × 15 mois).",
            "5 scripts Python : génération, préparation, visualisation, validation QA, synthèse PDF.",
            "5 graphiques PNG générés à partir du dataset réel du dépôt.",
            "1 PDF de synthèse décisionnelle (ce document).",
            "Documentation métier complète : cas d'usage, KPI, guide de lecture, choix de conception.",
        ]),
        ("Ce qui n'est pas encore fourni", ACCENT_ORANGE, [
            "Le fichier Power BI (.pbix) n'est pas inclus dans cette version.",
            "Les captures réelles du dashboard Power BI seront ajoutées dans assets/screenshots/.",
            "Le .pbix réel sera construit à partir du dataset fourni lors de la prochaine phase.",
        ]),
        ("Usage prévu", ACCENT_GREEN, [
            "Ce dépôt sert de vitrine professionnelle et de support de prévente.",
            "Il peut être partagé par lien GitHub, par email (PDF joint) ou en rendez-vous.",
            "Il illustre une logique de restitution décisionnelle, pas uniquement un outil.",
        ]),
    ]

    for title, color, lines in sections:
        fig.text(0.08, y, title, fontsize=12, fontweight="bold", color=color)
        for i, line in enumerate(lines):
            fig.text(0.10, y - 0.04 - i * 0.035, f"·  {line}",
                     fontsize=9, color=TEXT_WHITE)
        y -= 0.04 + len(lines) * 0.035 + 0.03

    fig.text(0.5, 0.06,
             "Lecture réalisée à partir d'un jeu de données synthétique conçu à des fins de démonstration.\n"
             "Cette page illustre une logique de restitution décisionnelle, et non l'analyse d'un client réel.",
             ha="center", fontsize=8, color=TEXT_SECONDARY, style="italic", linespacing=1.6)

    footer(fig, 5)
    pdf.savefig(fig, facecolor=BG_COLOR)
    plt.close(fig)


# ─── Main ───────────────────────────────────────────────────────────────

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
        print("  ✓ Page 4 : lecture décisionnelle synthétique")
        page_about(pdf, data)
        print("  ✓ Page 5 : à propos de la démonstration")

    print(f"\nTerminé. PDF sauvegardé : {output_path}")


if __name__ == "__main__":
    main()
