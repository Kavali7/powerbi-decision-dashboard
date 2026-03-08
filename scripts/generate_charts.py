"""
Génération de 5 graphiques réels à partir des données CSV du dashboard.
Les graphiques imitent le style Power BI sombre et professionnel.
Sauvegardés dans assets/charts/ pour validation avant remplacement.
"""
import csv
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from collections import defaultdict

# ─── Configuration ──────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "processed", "dashboard_input.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "assets", "charts")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Couleurs Power BI dark theme
BG_COLOR = '#1B2838'
CARD_BG = '#243447'
TEXT_COLOR = '#E8E8E8'
ACCENT_BLUE = '#4FC3F7'
ACCENT_ORANGE = '#FFB74D'
ACCENT_GREEN = '#66BB6A'
ACCENT_RED = '#EF5350'
ACCENT_PURPLE = '#AB47BC'
ACCENT_TEAL = '#26A69A'
GRID_COLOR = '#2C3E50'
SUBTITLE_COLOR = '#90A4AE'

ZONE_COLORS = {
    'Douala-Littoral': ACCENT_GREEN,
    'Abidjan-Plateau': ACCENT_BLUE,
    'Nairobi-Westlands': ACCENT_TEAL,
    'Dakar-Almadies': ACCENT_ORANGE,
    'Casablanca-Anfa': ACCENT_PURPLE,
    'Kinshasa-Gombe': ACCENT_RED,
}


def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def safe_float(val, default=0.0):
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def safe_int(val, default=0):
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return default


def setup_figure(figsize=(16, 9)):
    fig = plt.figure(figsize=figsize, facecolor=BG_COLOR)
    return fig


# ─── CHART 1: Executive Overview ────────────────────────────────────────
def chart_01_executive_overview(data):
    fig = setup_figure((16, 10))
    
    # Calculs globaux
    total_planned = sum(safe_int(r['planned_activities']) for r in data)
    total_completed = sum(safe_int(r['completed_activities']) for r in data)
    total_target_ben = sum(safe_int(r['target_beneficiaries']) for r in data)
    total_actual_ben = sum(safe_int(r['actual_beneficiaries']) for r in data)
    total_planned_bud = sum(safe_int(r['planned_budget']) for r in data)
    total_spent_bud = sum(safe_int(r['spent_budget']) for r in data)
    total_rpt_exp = sum(safe_int(r['reports_expected']) for r in data)
    total_rpt_ot = sum(safe_int(r['reports_submitted_on_time']) for r in data)
    
    acr = total_completed / total_planned if total_planned else 0
    bar_ = total_actual_ben / total_target_ben if total_target_ben else 0
    ber = total_spent_bud / total_planned_bud if total_planned_bud else 0
    rtr = total_rpt_ot / total_rpt_exp if total_rpt_exp else 0
    budget_gap = total_spent_bud - total_planned_bud
    
    zones_alerte = set()
    for r in data:
        if safe_int(r['alert_flag']) == 1:
            zones_alerte.add(r['zone_name'])
    
    # Titre
    fig.text(0.5, 0.96, 'Tableau de Bord Décisionnel — Suivi de Programme',
             ha='center', va='top', fontsize=18, fontweight='bold', color=TEXT_COLOR)
    fig.text(0.5, 0.93, 'Aperçu exécutif · Données synthétiques de démonstration',
             ha='center', va='top', fontsize=10, color=SUBTITLE_COLOR)
    
    # KPI Cards
    kpis = [
        (f'{acr:.0%}', 'Activités\nachevées', ACCENT_GREEN if acr >= 0.8 else ACCENT_RED),
        (f'{bar_:.0%}', 'Bénéficiaires\natteints', ACCENT_GREEN if bar_ >= 0.8 else ACCENT_RED),
        (f'{ber:.0%}', 'Exécution\nbudgétaire', ACCENT_GREEN if 0.85 <= ber <= 1.05 else ACCENT_ORANGE),
        (f'{rtr:.0%}', 'Reporting\nà temps', ACCENT_GREEN if rtr >= 0.75 else ACCENT_RED),
        (f'{len(zones_alerte)}', 'Zones\nen alerte', ACCENT_RED if len(zones_alerte) > 2 else ACCENT_GREEN),
        (f'{budget_gap/1e6:+.1f}M', 'Écart\nbudgétaire', ACCENT_RED if budget_gap > 0 else ACCENT_GREEN),
    ]
    
    for i, (val, label, color) in enumerate(kpis):
        ax = fig.add_axes([0.03 + i * 0.157, 0.78, 0.14, 0.12])
        ax.set_facecolor(CARD_BG)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.text(0.5, 0.7, val, ha='center', va='center', fontsize=22, fontweight='bold', color=color, transform=ax.transAxes)
        ax.text(0.5, 0.2, label, ha='center', va='center', fontsize=8, color=SUBTITLE_COLOR, transform=ax.transAxes)
    
    # Tendance mensuelle
    ax2 = fig.add_axes([0.06, 0.40, 0.55, 0.32])
    ax2.set_facecolor(BG_COLOR)
    
    monthly = defaultdict(lambda: {'planned': 0, 'completed': 0})
    for r in data:
        ym = r['year_month']
        monthly[ym]['planned'] += safe_int(r['planned_activities'])
        monthly[ym]['completed'] += safe_int(r['completed_activities'])
    
    months_sorted = sorted(monthly.keys())
    planned_vals = [monthly[m]['planned'] for m in months_sorted]
    completed_vals = [monthly[m]['completed'] for m in months_sorted]
    x = range(len(months_sorted))
    labels_short = [m[-2:] + '/' + m[2:4] for m in months_sorted]
    
    ax2.bar(x, planned_vals, color=ACCENT_BLUE, alpha=0.35, width=0.6, label='Planifié')
    ax2.plot(x, completed_vals, color=ACCENT_ORANGE, marker='o', markersize=5, linewidth=2, label='Réalisé')
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels_short, rotation=45, fontsize=7, color=SUBTITLE_COLOR)
    ax2.set_ylabel('Nombre d\'activités', color=SUBTITLE_COLOR, fontsize=9)
    ax2.tick_params(colors=SUBTITLE_COLOR, labelsize=8)
    ax2.legend(fontsize=8, loc='upper left', facecolor=CARD_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
    ax2.set_title('Tendance mensuelle des activités', color=TEXT_COLOR, fontsize=11, pad=10)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['bottom'].set_color(GRID_COLOR)
    ax2.spines['left'].set_color(GRID_COLOR)
    ax2.set_axisbelow(True)
    ax2.yaxis.grid(True, color=GRID_COLOR, alpha=0.3)
    
    # Comparaison par zone (barres horizontales)
    ax3 = fig.add_axes([0.68, 0.40, 0.28, 0.32])
    ax3.set_facecolor(BG_COLOR)
    
    zone_perf = defaultdict(lambda: {'planned': 0, 'completed': 0})
    for r in data:
        zn = r['zone_name']
        zone_perf[zn]['planned'] += safe_int(r['planned_activities'])
        zone_perf[zn]['completed'] += safe_int(r['completed_activities'])
    
    zone_rates = {z: d['completed'] / d['planned'] if d['planned'] else 0 for z, d in zone_perf.items()}
    sorted_zones = sorted(zone_rates.items(), key=lambda x: x[1])
    z_names = [z[0] for z in sorted_zones]
    z_vals = [z[1] for z in sorted_zones]
    z_colors = [ZONE_COLORS.get(z, ACCENT_BLUE) for z in z_names]
    
    bars = ax3.barh(z_names, z_vals, color=z_colors, height=0.6, alpha=0.85)
    for bar, val in zip(bars, z_vals):
        ax3.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                f'{val:.0%}', va='center', fontsize=9, color=TEXT_COLOR, fontweight='bold')
    ax3.set_xlim(0, 1.15)
    ax3.axvline(x=0.8, color=ACCENT_RED, linestyle='--', alpha=0.4, linewidth=1)
    ax3.set_title('Performance par zone', color=TEXT_COLOR, fontsize=11, pad=10)
    ax3.tick_params(colors=SUBTITLE_COLOR, labelsize=8)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.spines['bottom'].set_color(GRID_COLOR)
    ax3.spines['left'].set_color(GRID_COLOR)
    ax3.xaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    
    # Budget vs résultats par zone
    ax4 = fig.add_axes([0.06, 0.04, 0.55, 0.28])
    ax4.set_facecolor(BG_COLOR)
    
    zone_budget = defaultdict(lambda: {'planned': 0, 'spent': 0})
    for r in data:
        zn = r['zone_name']
        zone_budget[zn]['planned'] += safe_int(r['planned_budget'])
        zone_budget[zn]['spent'] += safe_int(r['spent_budget'])
    
    z_names_b = sorted(zone_budget.keys())
    x_b = range(len(z_names_b))
    planned_b = [zone_budget[z]['planned'] / 1e6 for z in z_names_b]
    spent_b = [zone_budget[z]['spent'] / 1e6 for z in z_names_b]
    w = 0.35
    
    ax4.bar([i - w/2 for i in x_b], planned_b, w, color=ACCENT_BLUE, alpha=0.7, label='Budget planifié')
    ax4.bar([i + w/2 for i in x_b], spent_b, w, color=ACCENT_ORANGE, alpha=0.7, label='Budget dépensé')
    ax4.set_xticks(x_b)
    ax4.set_xticklabels([z.split('-')[0] for z in z_names_b], fontsize=8, color=SUBTITLE_COLOR)
    ax4.set_ylabel('Budget (millions)', color=SUBTITLE_COLOR, fontsize=9)
    ax4.tick_params(colors=SUBTITLE_COLOR, labelsize=8)
    ax4.legend(fontsize=8, loc='upper right', facecolor=CARD_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
    ax4.set_title('Budget planifié vs dépensé par zone', color=TEXT_COLOR, fontsize=11, pad=10)
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)
    ax4.spines['bottom'].set_color(GRID_COLOR)
    ax4.spines['left'].set_color(GRID_COLOR)
    ax4.set_axisbelow(True)
    ax4.yaxis.grid(True, color=GRID_COLOR, alpha=0.3)
    
    # Mini table d'alertes
    ax5 = fig.add_axes([0.68, 0.04, 0.28, 0.28])
    ax5.set_facecolor(CARD_BG)
    ax5.set_title('Alertes prioritaires', color=TEXT_COLOR, fontsize=11, pad=10)
    
    alert_rows = []
    zone_alert_count = defaultdict(int)
    for r in data:
        if safe_int(r['alert_flag']) == 1:
            zone_alert_count[r['zone_name']] += 1
    
    sorted_alerts = sorted(zone_alert_count.items(), key=lambda x: x[1], reverse=True)[:6]
    
    for spine in ax5.spines.values():
        spine.set_visible(False)
    ax5.set_xticks([])
    ax5.set_yticks([])
    
    ax5.text(0.05, 0.92, 'Zone', fontsize=9, fontweight='bold', color=SUBTITLE_COLOR, transform=ax5.transAxes)
    ax5.text(0.65, 0.92, 'Alertes', fontsize=9, fontweight='bold', color=SUBTITLE_COLOR, transform=ax5.transAxes)
    
    for i, (zone, count) in enumerate(sorted_alerts):
        y = 0.80 - i * 0.13
        short_name = zone.split('-')[0] if len(zone) > 12 else zone
        color = ACCENT_RED if count > 40 else (ACCENT_ORANGE if count > 20 else ACCENT_GREEN)
        ax5.text(0.05, y, short_name, fontsize=9, color=TEXT_COLOR, transform=ax5.transAxes)
        ax5.text(0.65, y, str(count), fontsize=11, fontweight='bold', color=color, transform=ax5.transAxes)
        level = 'Critique' if count > 40 else ('Modéré' if count > 20 else 'Faible')
        ax5.text(0.80, y, level, fontsize=8, color=color, transform=ax5.transAxes)
    
    plt.savefig(os.path.join(OUTPUT_DIR, '01-executive-overview-mockup.png'), 
                facecolor=BG_COLOR, dpi=150, bbox_inches='tight', pad_inches=0.3)
    plt.close()
    print("  ✓ 01-executive-overview-mockup.png")


# ─── CHART 2: Performance by Zone ───────────────────────────────────────
def chart_02_performance_by_zone(data):
    fig = setup_figure((16, 9))
    
    fig.text(0.5, 0.96, 'Performance par Zone', ha='center', va='top',
             fontsize=18, fontweight='bold', color=TEXT_COLOR)
    fig.text(0.5, 0.93, 'Taux d\'achèvement des activités par zone · Jan 2024 – Mar 2025',
             ha='center', va='top', fontsize=10, color=SUBTITLE_COLOR)
    
    # Données par zone
    zone_data = defaultdict(lambda: {'planned': 0, 'completed': 0, 'benef_target': 0, 'benef_actual': 0,
                                      'budget_planned': 0, 'budget_spent': 0, 'rpt_exp': 0, 'rpt_ot': 0})
    for r in data:
        zn = r['zone_name']
        zone_data[zn]['planned'] += safe_int(r['planned_activities'])
        zone_data[zn]['completed'] += safe_int(r['completed_activities'])
        zone_data[zn]['benef_target'] += safe_int(r['target_beneficiaries'])
        zone_data[zn]['benef_actual'] += safe_int(r['actual_beneficiaries'])
        zone_data[zn]['budget_planned'] += safe_int(r['planned_budget'])
        zone_data[zn]['budget_spent'] += safe_int(r['spent_budget'])
        zone_data[zn]['rpt_exp'] += safe_int(r['reports_expected'])
        zone_data[zn]['rpt_ot'] += safe_int(r['reports_submitted_on_time'])
    
    zone_rates = {}
    for z, d in zone_data.items():
        zone_rates[z] = {
            'acr': d['completed'] / d['planned'] if d['planned'] else 0,
            'bar': d['benef_actual'] / d['benef_target'] if d['benef_target'] else 0,
            'ber': d['budget_spent'] / d['budget_planned'] if d['budget_planned'] else 0,
            'rtr': d['rpt_ot'] / d['rpt_exp'] if d['rpt_exp'] else 0,
        }
    
    sorted_zones = sorted(zone_rates.items(), key=lambda x: x[1]['acr'], reverse=True)
    
    # Barres horizontales principales
    ax = fig.add_axes([0.06, 0.10, 0.42, 0.75])
    ax.set_facecolor(BG_COLOR)
    
    z_names = [z[0] for z in sorted_zones]
    z_vals = [z[1]['acr'] for z in sorted_zones]
    z_colors = [ZONE_COLORS.get(z, ACCENT_BLUE) for z in z_names]
    
    y_pos = range(len(z_names))
    bars = ax.barh(y_pos, z_vals, color=z_colors, height=0.6, alpha=0.85)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(z_names, fontsize=10, color=TEXT_COLOR)
    ax.set_xlim(0, 1.15)
    ax.axvline(x=0.8, color=ACCENT_RED, linestyle='--', alpha=0.5, linewidth=1, label='Seuil 80%')
    
    for bar, val in zip(bars, z_vals):
        ax.text(bar.get_width() + 0.015, bar.get_y() + bar.get_height()/2,
                f'{val:.0%}', va='center', fontsize=12, color=TEXT_COLOR, fontweight='bold')
    
    ax.set_title('Taux d\'achèvement des activités', color=TEXT_COLOR, fontsize=12, pad=10)
    ax.xaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    ax.tick_params(colors=SUBTITLE_COLOR, labelsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(GRID_COLOR)
    ax.spines['left'].set_color(GRID_COLOR)
    ax.legend(fontsize=8, facecolor=CARD_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
    
    # Tableau récapitulatif à droite
    ax2 = fig.add_axes([0.54, 0.10, 0.42, 0.75])
    ax2.set_facecolor(CARD_BG)
    for spine in ax2.spines.values():
        spine.set_visible(False)
    ax2.set_xticks([])
    ax2.set_yticks([])
    
    headers = ['Zone', 'Activités', 'Bénéfic.', 'Budget', 'Reporting']
    col_x = [0.02, 0.28, 0.45, 0.62, 0.80]
    
    for j, h in enumerate(headers):
        ax2.text(col_x[j], 0.94, h, fontsize=9, fontweight='bold', color=SUBTITLE_COLOR, transform=ax2.transAxes)
    
    ax2.axhline(y=0.92, xmin=0.01, xmax=0.99, color=GRID_COLOR, linewidth=0.5, transform=ax2.transAxes)
    
    for i, (zone, rates) in enumerate(sorted_zones):
        y = 0.85 - i * 0.13
        short = zone.split('-')[0] if len(zone) > 10 else zone
        ax2.text(col_x[0], y, short, fontsize=9, color=TEXT_COLOR, transform=ax2.transAxes)
        
        vals = [rates['acr'], rates['bar'], rates['ber'], rates['rtr']]
        for j, v in enumerate(vals):
            if j == 2:
                color = ACCENT_GREEN if 0.85 <= v <= 1.05 else ACCENT_ORANGE
            else:
                color = ACCENT_GREEN if v >= 0.80 else ACCENT_RED
            ax2.text(col_x[j+1], y, f'{v:.0%}', fontsize=10, fontweight='bold', color=color, transform=ax2.transAxes)
    
    ax2.text(0.5, 0.02, 'Vert = conforme · Rouge = en alerte · Orange = à surveiller',
             ha='center', fontsize=8, color=SUBTITLE_COLOR, transform=ax2.transAxes, style='italic')
    
    plt.savefig(os.path.join(OUTPUT_DIR, '02-performance-by-zone-mockup.png'),
                facecolor=BG_COLOR, dpi=150, bbox_inches='tight', pad_inches=0.3)
    plt.close()
    print("  ✓ 02-performance-by-zone-mockup.png")


# ─── CHART 3: Budget vs Results ─────────────────────────────────────────
def chart_03_budget_vs_results(data):
    fig = setup_figure((16, 9))
    
    fig.text(0.5, 0.96, 'Budget vs Résultats', ha='center', va='top',
             fontsize=18, fontweight='bold', color=TEXT_COLOR)
    fig.text(0.5, 0.93, 'Cohérence entre dépense et performance · Jan 2024 – Mar 2025',
             ha='center', va='top', fontsize=10, color=SUBTITLE_COLOR)
    
    zone_data = defaultdict(lambda: {'planned_bud': 0, 'spent_bud': 0, 'planned_act': 0, 'completed_act': 0})
    for r in data:
        zn = r['zone_name']
        zone_data[zn]['planned_bud'] += safe_int(r['planned_budget'])
        zone_data[zn]['spent_bud'] += safe_int(r['spent_budget'])
        zone_data[zn]['planned_act'] += safe_int(r['planned_activities'])
        zone_data[zn]['completed_act'] += safe_int(r['completed_activities'])
    
    z_names = sorted(zone_data.keys())
    
    # Grouped bars
    ax = fig.add_axes([0.06, 0.42, 0.55, 0.45])
    ax.set_facecolor(BG_COLOR)
    
    x = range(len(z_names))
    w = 0.35
    planned_b = [zone_data[z]['planned_bud'] / 1e6 for z in z_names]
    spent_b = [zone_data[z]['spent_bud'] / 1e6 for z in z_names]
    
    ax.bar([i - w/2 for i in x], planned_b, w, color=ACCENT_BLUE, alpha=0.75, label='Budget planifié')
    ax.bar([i + w/2 for i in x], spent_b, w, color=ACCENT_ORANGE, alpha=0.75, label='Budget dépensé')
    
    ax.set_xticks(x)
    ax.set_xticklabels([z.split('-')[0] for z in z_names], fontsize=9, color=SUBTITLE_COLOR)
    ax.set_ylabel('Millions (XOF)', color=SUBTITLE_COLOR, fontsize=9)
    ax.legend(fontsize=8, facecolor=CARD_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
    ax.set_title('Budget par zone', color=TEXT_COLOR, fontsize=12, pad=10)
    ax.tick_params(colors=SUBTITLE_COLOR)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(GRID_COLOR)
    ax.spines['left'].set_color(GRID_COLOR)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color=GRID_COLOR, alpha=0.3)
    
    # Scatter: Budget exec rate vs Activity completion rate
    ax2 = fig.add_axes([0.68, 0.42, 0.28, 0.45])
    ax2.set_facecolor(BG_COLOR)
    
    for z in z_names:
        d = zone_data[z]
        ber = d['spent_bud'] / d['planned_bud'] if d['planned_bud'] else 0
        acr = d['completed_act'] / d['planned_act'] if d['planned_act'] else 0
        color = ZONE_COLORS.get(z, ACCENT_BLUE)
        ax2.scatter(ber, acr, color=color, s=150, zorder=5, edgecolors='white', linewidth=1)
        ax2.annotate(z.split('-')[0], (ber, acr), textcoords="offset points", xytext=(8, 5),
                    fontsize=8, color=TEXT_COLOR)
    
    ax2.axhline(y=0.8, color=ACCENT_RED, linestyle='--', alpha=0.3, linewidth=1)
    ax2.axvline(x=1.0, color=ACCENT_ORANGE, linestyle='--', alpha=0.3, linewidth=1)
    ax2.set_xlabel('Taux exécution budgétaire', color=SUBTITLE_COLOR, fontsize=9)
    ax2.set_ylabel('Taux achèvement activités', color=SUBTITLE_COLOR, fontsize=9)
    ax2.set_title('Exécution vs Performance', color=TEXT_COLOR, fontsize=11, pad=10)
    ax2.tick_params(colors=SUBTITLE_COLOR, labelsize=8)
    ax2.xaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    ax2.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['bottom'].set_color(GRID_COLOR)
    ax2.spines['left'].set_color(GRID_COLOR)
    
    # KPI cards en bas
    total_planned = sum(zone_data[z]['planned_bud'] for z in z_names)
    total_spent = sum(zone_data[z]['spent_bud'] for z in z_names)
    variance = total_spent - total_planned
    exec_rate = total_spent / total_planned if total_planned else 0
    
    kpis = [
        (f'{total_planned/1e9:.2f} Mrd', 'Budget total planifié', ACCENT_BLUE),
        (f'{total_spent/1e9:.2f} Mrd', 'Budget total dépensé', ACCENT_ORANGE),
        (f'{exec_rate:.0%}', 'Taux d\'exécution global', ACCENT_GREEN if 0.85 <= exec_rate <= 1.05 else ACCENT_RED),
        (f'{variance/1e6:+.0f}M', 'Écart budgétaire global', ACCENT_RED if variance > 0 else ACCENT_GREEN),
    ]
    
    for i, (val, label, color) in enumerate(kpis):
        ax_k = fig.add_axes([0.03 + i * 0.24, 0.06, 0.22, 0.25])
        ax_k.set_facecolor(CARD_BG)
        for spine in ax_k.spines.values():
            spine.set_visible(False)
        ax_k.set_xticks([])
        ax_k.set_yticks([])
        ax_k.text(0.5, 0.65, val, ha='center', va='center', fontsize=20, fontweight='bold', color=color, transform=ax_k.transAxes)
        ax_k.text(0.5, 0.25, label, ha='center', va='center', fontsize=8, color=SUBTITLE_COLOR, transform=ax_k.transAxes)
    
    plt.savefig(os.path.join(OUTPUT_DIR, '03-budget-vs-results-mockup.png'),
                facecolor=BG_COLOR, dpi=150, bbox_inches='tight', pad_inches=0.3)
    plt.close()
    print("  ✓ 03-budget-vs-results-mockup.png")


# ─── CHART 4: Alerts Table ──────────────────────────────────────────────
def chart_04_alerts_table(data):
    fig = setup_figure((16, 9))
    
    fig.text(0.5, 0.96, 'Alertes de Pilotage', ha='center', va='top',
             fontsize=18, fontweight='bold', color=TEXT_COLOR)
    fig.text(0.5, 0.93, 'Points d\'attention par zone et composante',
             ha='center', va='top', fontsize=10, color=SUBTITLE_COLOR)
    
    # Summary cards
    total_alerts = sum(1 for r in data if safe_int(r['alert_flag']) == 1)
    total_records = len(data)
    alert_rate = total_alerts / total_records if total_records else 0
    zones_en_alerte = len(set(r['zone_name'] for r in data if safe_int(r['alert_flag']) == 1))
    high_priority = sum(safe_int(r['high_priority_alerts']) for r in data)
    
    cards = [
        (str(total_alerts), f'Enregistrements\nen alerte / {total_records}', ACCENT_RED),
        (f'{alert_rate:.0%}', 'Taux\nd\'alerte global', ACCENT_ORANGE),
        (str(zones_en_alerte), 'Zones\nconcernées', ACCENT_RED if zones_en_alerte > 3 else ACCENT_ORANGE),
        (str(high_priority), 'Alertes\nhaute priorité', ACCENT_RED),
    ]
    
    for i, (val, label, color) in enumerate(cards):
        ax = fig.add_axes([0.03 + i * 0.24, 0.80, 0.22, 0.10])
        ax.set_facecolor(CARD_BG)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.text(0.3, 0.5, val, ha='center', va='center', fontsize=24, fontweight='bold', color=color, transform=ax.transAxes)
        ax.text(0.7, 0.5, label, ha='center', va='center', fontsize=8, color=SUBTITLE_COLOR, transform=ax.transAxes)
    
    # Alerts by zone x component
    zone_comp_alerts = defaultdict(lambda: defaultdict(int))
    for r in data:
        if safe_int(r['alert_flag']) == 1:
            zone_comp_alerts[r['zone_name']][r['component_name']] += 1
    
    # Heatmap
    ax2 = fig.add_axes([0.06, 0.08, 0.55, 0.65])
    ax2.set_facecolor(BG_COLOR)
    
    zones_list = sorted(zone_comp_alerts.keys(), key=lambda z: sum(zone_comp_alerts[z].values()), reverse=True)
    comps_list = sorted(set(r['component_name'] for r in data))
    
    cell_data = []
    for z in zones_list:
        row = [zone_comp_alerts[z].get(c, 0) for c in comps_list]
        cell_data.append(row)
    
    for i, z in enumerate(zones_list):
        for j, c in enumerate(comps_list):
            val = zone_comp_alerts[z].get(c, 0)
            if val > 10:
                color = ACCENT_RED
                alpha = 0.7
            elif val > 5:
                color = ACCENT_ORANGE
                alpha = 0.5
            elif val > 0:
                color = ACCENT_ORANGE
                alpha = 0.25
            else:
                color = ACCENT_GREEN
                alpha = 0.15
            
            rect = plt.Rectangle((j, len(zones_list) - 1 - i), 1, 1, facecolor=color, alpha=alpha, edgecolor=GRID_COLOR, linewidth=0.5)
            ax2.add_patch(rect)
            ax2.text(j + 0.5, len(zones_list) - 0.5 - i, str(val) if val > 0 else '-',
                    ha='center', va='center', fontsize=11, fontweight='bold',
                    color=TEXT_COLOR if val > 0 else SUBTITLE_COLOR)
    
    ax2.set_xlim(0, len(comps_list))
    ax2.set_ylim(0, len(zones_list))
    ax2.set_xticks([j + 0.5 for j in range(len(comps_list))])
    short_comps = [c[:15] + '...' if len(c) > 15 else c for c in comps_list]
    ax2.set_xticklabels(short_comps, fontsize=8, color=SUBTITLE_COLOR, rotation=30, ha='right')
    ax2.set_yticks([i + 0.5 for i in range(len(zones_list))])
    ax2.set_yticklabels(reversed(zones_list), fontsize=9, color=TEXT_COLOR)
    ax2.set_title('Nombre d\'alertes par zone et composante', color=TEXT_COLOR, fontsize=12, pad=10)
    ax2.tick_params(length=0)
    for spine in ax2.spines.values():
        spine.set_color(GRID_COLOR)
    
    # Top alerts detail
    ax3 = fig.add_axes([0.66, 0.08, 0.30, 0.65])
    ax3.set_facecolor(CARD_BG)
    for spine in ax3.spines.values():
        spine.set_visible(False)
    ax3.set_xticks([])
    ax3.set_yticks([])
    
    ax3.text(0.5, 0.97, 'Détail des alertes par indicateur', ha='center', fontsize=10,
             fontweight='bold', color=TEXT_COLOR, transform=ax3.transAxes)
    
    alert_types = defaultdict(int)
    for r in data:
        acr = safe_float(r['activity_completion_rate'])
        bar_ = safe_float(r['beneficiary_achievement_rate']) if r['beneficiary_achievement_rate'] != '' else 1.0
        ber = safe_float(r['budget_execution_rate'])
        rtr = safe_float(r['reporting_on_time_rate'])
        ha = safe_int(r['high_priority_alerts'])
        
        if acr < 0.80: alert_types['Activités < 80%'] += 1
        if bar_ < 0.80: alert_types['Bénéficiaires < 80%'] += 1
        if ber > 1.05: alert_types['Budget > 105%'] += 1
        if rtr < 0.75: alert_types['Reporting < 75%'] += 1
        if ha >= 2: alert_types['Alertes haute priorité'] += 1
    
    sorted_types = sorted(alert_types.items(), key=lambda x: x[1], reverse=True)
    
    for i, (atype, count) in enumerate(sorted_types):
        y = 0.88 - i * 0.14
        ax3.text(0.08, y, atype, fontsize=9, color=TEXT_COLOR, transform=ax3.transAxes)
        ax3.text(0.85, y, str(count), fontsize=12, fontweight='bold', color=ACCENT_RED, transform=ax3.transAxes)
        # Mini bar
        bar_width = min(0.7, count / max(c for _, c in sorted_types) * 0.7)
        rect = plt.Rectangle((0.08, y - 0.04), bar_width, 0.03, facecolor=ACCENT_RED, alpha=0.3, transform=ax3.transAxes)
        ax3.add_patch(rect)
    
    plt.savefig(os.path.join(OUTPUT_DIR, '04-alerts-table-mockup.png'),
                facecolor=BG_COLOR, dpi=150, bbox_inches='tight', pad_inches=0.3)
    plt.close()
    print("  ✓ 04-alerts-table-mockup.png")


# ─── CHART 5: Operational View ──────────────────────────────────────────
def chart_05_operational_view(data):
    fig = setup_figure((16, 10))
    
    fig.text(0.5, 0.97, 'Vue Opérationnelle', ha='center', va='top',
             fontsize=18, fontweight='bold', color=TEXT_COLOR)
    fig.text(0.5, 0.94, 'Détail par composante et responsable · Jan 2024 – Mar 2025',
             ha='center', va='top', fontsize=10, color=SUBTITLE_COLOR)
    
    # Performance par composante
    comp_data = defaultdict(lambda: {'planned': 0, 'completed': 0})
    for r in data:
        cn = r['component_name']
        comp_data[cn]['planned'] += safe_int(r['planned_activities'])
        comp_data[cn]['completed'] += safe_int(r['completed_activities'])
    
    ax = fig.add_axes([0.06, 0.52, 0.42, 0.36])
    ax.set_facecolor(BG_COLOR)
    
    c_names = sorted(comp_data.keys())
    x = range(len(c_names))
    w = 0.35
    planned_c = [comp_data[c]['planned'] for c in c_names]
    completed_c = [comp_data[c]['completed'] for c in c_names]
    
    ax.bar([i - w/2 for i in x], planned_c, w, color=ACCENT_BLUE, alpha=0.7, label='Planifié')
    ax.bar([i + w/2 for i in x], completed_c, w, color=ACCENT_GREEN, alpha=0.7, label='Réalisé')
    
    short_names = [c[:12] + '...' if len(c) > 12 else c for c in c_names]
    ax.set_xticks(x)
    ax.set_xticklabels(short_names, fontsize=8, color=SUBTITLE_COLOR, rotation=15)
    ax.set_ylabel('Nombre d\'activités', color=SUBTITLE_COLOR, fontsize=9)
    ax.legend(fontsize=8, facecolor=CARD_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
    ax.set_title('Activités par composante', color=TEXT_COLOR, fontsize=12, pad=10)
    ax.tick_params(colors=SUBTITLE_COLOR, labelsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(GRID_COLOR)
    ax.spines['left'].set_color(GRID_COLOR)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color=GRID_COLOR, alpha=0.3)
    
    # Performance par responsable
    mgr_data = defaultdict(lambda: {'planned': 0, 'completed': 0})
    for r in data:
        mn = r['manager_name']
        mgr_data[mn]['planned'] += safe_int(r['planned_activities'])
        mgr_data[mn]['completed'] += safe_int(r['completed_activities'])
    
    mgr_rates = {m: d['completed'] / d['planned'] if d['planned'] else 0 for m, d in mgr_data.items()}
    sorted_mgrs = sorted(mgr_rates.items(), key=lambda x: x[1])
    
    ax2 = fig.add_axes([0.55, 0.52, 0.40, 0.36])
    ax2.set_facecolor(BG_COLOR)
    
    m_names = [m[0] for m in sorted_mgrs]
    m_vals = [m[1] for m in sorted_mgrs]
    m_colors = [ACCENT_GREEN if v >= 0.85 else (ACCENT_ORANGE if v >= 0.75 else ACCENT_RED) for v in m_vals]
    
    bars = ax2.barh(m_names, m_vals, color=m_colors, height=0.5, alpha=0.85)
    ax2.axvline(x=0.8, color=ACCENT_RED, linestyle='--', alpha=0.4, linewidth=1)
    
    for bar, val in zip(bars, m_vals):
        ax2.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                f'{val:.0%}', va='center', fontsize=10, color=TEXT_COLOR, fontweight='bold')
    
    ax2.set_xlim(0, 1.1)
    ax2.set_title('Performance par responsable', color=TEXT_COLOR, fontsize=12, pad=10)
    ax2.xaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    ax2.tick_params(colors=SUBTITLE_COLOR, labelsize=9)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['bottom'].set_color(GRID_COLOR)
    ax2.spines['left'].set_color(GRID_COLOR)
    
    # Reporting (donut)
    ax3 = fig.add_axes([0.06, 0.06, 0.25, 0.36])
    ax3.set_facecolor(BG_COLOR)
    
    total_rpt_exp = sum(safe_int(r['reports_expected']) for r in data)
    total_rpt_sub = sum(safe_int(r['reports_submitted']) for r in data)
    total_rpt_ot = sum(safe_int(r['reports_submitted_on_time']) for r in data)
    rpt_late = total_rpt_sub - total_rpt_ot
    rpt_missing = total_rpt_exp - total_rpt_sub
    
    sizes = [total_rpt_ot, rpt_late, rpt_missing]
    labels_d = ['À temps', 'En retard', 'Non soumis']
    colors_d = [ACCENT_GREEN, ACCENT_ORANGE, ACCENT_RED]
    
    wedges, texts, autotexts = ax3.pie(sizes, labels=labels_d, colors=colors_d, autopct='%1.0f%%',
                                        startangle=90, pctdistance=0.75, wedgeprops=dict(width=0.35),
                                        textprops={'color': TEXT_COLOR, 'fontsize': 8})
    for t in autotexts:
        t.set_fontsize(9)
        t.set_fontweight('bold')
    ax3.set_title('Statut du reporting', color=TEXT_COLOR, fontsize=11, pad=5)
    
    # Issues (bar chart)
    ax4 = fig.add_axes([0.38, 0.06, 0.25, 0.36])
    ax4.set_facecolor(BG_COLOR)
    
    zone_issues = defaultdict(lambda: {'open': 0, 'closed': 0})
    for r in data:
        zn = r['zone_name'].split('-')[0]
        zone_issues[zn]['open'] += safe_int(r['open_issues'])
        zone_issues[zn]['closed'] += safe_int(r['closed_issues'])
    
    zi_names = sorted(zone_issues.keys())
    x_i = range(len(zi_names))
    w_i = 0.35
    
    ax4.bar([i - w_i/2 for i in x_i], [zone_issues[z]['open'] for z in zi_names], w_i, color=ACCENT_RED, alpha=0.7, label='Ouverts')
    ax4.bar([i + w_i/2 for i in x_i], [zone_issues[z]['closed'] for z in zi_names], w_i, color=ACCENT_GREEN, alpha=0.7, label='Fermés')
    ax4.set_xticks(x_i)
    ax4.set_xticklabels(zi_names, fontsize=7, color=SUBTITLE_COLOR, rotation=30)
    ax4.legend(fontsize=7, facecolor=CARD_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
    ax4.set_title('Problèmes par zone', color=TEXT_COLOR, fontsize=11, pad=10)
    ax4.tick_params(colors=SUBTITLE_COLOR, labelsize=7)
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)
    ax4.spines['bottom'].set_color(GRID_COLOR)
    ax4.spines['left'].set_color(GRID_COLOR)
    ax4.set_axisbelow(True)
    ax4.yaxis.grid(True, color=GRID_COLOR, alpha=0.3)
    
    # Mini table analytique
    ax5 = fig.add_axes([0.68, 0.06, 0.28, 0.36])
    ax5.set_facecolor(CARD_BG)
    for spine in ax5.spines.values():
        spine.set_visible(False)
    ax5.set_xticks([])
    ax5.set_yticks([])
    
    ax5.text(0.5, 0.95, 'Résumé par composante', ha='center', fontsize=10,
             fontweight='bold', color=TEXT_COLOR, transform=ax5.transAxes)
    
    ax5.text(0.05, 0.85, 'Composante', fontsize=8, fontweight='bold', color=SUBTITLE_COLOR, transform=ax5.transAxes)
    ax5.text(0.55, 0.85, 'Taux', fontsize=8, fontweight='bold', color=SUBTITLE_COLOR, transform=ax5.transAxes)
    ax5.text(0.75, 0.85, 'Statut', fontsize=8, fontweight='bold', color=SUBTITLE_COLOR, transform=ax5.transAxes)
    
    for i, cn in enumerate(sorted(comp_data.keys())):
        y = 0.72 - i * 0.16
        rate = comp_data[cn]['completed'] / comp_data[cn]['planned'] if comp_data[cn]['planned'] else 0
        color = ACCENT_GREEN if rate >= 0.85 else (ACCENT_ORANGE if rate >= 0.75 else ACCENT_RED)
        status = '●' if rate >= 0.85 else ('◐' if rate >= 0.75 else '○')
        short = cn[:18] + '..' if len(cn) > 18 else cn
        ax5.text(0.05, y, short, fontsize=8, color=TEXT_COLOR, transform=ax5.transAxes)
        ax5.text(0.55, y, f'{rate:.0%}', fontsize=10, fontweight='bold', color=color, transform=ax5.transAxes)
        ax5.text(0.80, y, status, fontsize=14, color=color, transform=ax5.transAxes)
    
    plt.savefig(os.path.join(OUTPUT_DIR, '05-operational-view-mockup.png'),
                facecolor=BG_COLOR, dpi=150, bbox_inches='tight', pad_inches=0.3)
    plt.close()
    print("  ✓ 05-operational-view-mockup.png")


# ─── Main ───────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("Génération des graphiques à partir des données réelles...")
    print()
    data = load_data()
    chart_01_executive_overview(data)
    chart_02_performance_by_zone(data)
    chart_03_budget_vs_results(data)
    chart_04_alerts_table(data)
    chart_05_operational_view(data)
    print()
    print(f"Terminé. Graphiques sauvegardés dans : {OUTPUT_DIR}")
