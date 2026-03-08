# Dictionnaire de données

Ce document décrit l'ensemble des colonnes utilisées dans le dataset de démonstration.

**Toutes les données de ce dépôt sont fictives, synthétiques et créées uniquement à des fins de démonstration.**

---

## Tables dimensionnelles

### dim_calendar.csv

| Colonne | Type | Description |
|---|---|---|
| `date_key` | date | Clé de date au format YYYY-MM-DD (premier jour du mois) |
| `year` | integer | Année |
| `quarter` | string | Trimestre (Q1, Q2, Q3, Q4) |
| `month_number` | integer | Numéro du mois (1 à 12) |
| `month_name` | string | Nom du mois en anglais |
| `month_label` | string | Libellé court (ex. Jan 2024) |
| `year_month` | string | Période au format YYYY-MM |

### dim_zone.csv

| Colonne | Type | Description |
|---|---|---|
| `zone_id` | string | Identifiant unique de zone (Z01 à Z06) |
| `zone_name` | string | Nom de la zone de pilotage |
| `region_group` | string | Regroupement régional |
| `site_count` | integer | Nombre de sites couverts par la zone |
| `population_coverage_estimate` | integer | Estimation de la population couverte |
| `zone_priority_level` | string | Niveau de priorité (High, Medium) |

### dim_program_component.csv

| Colonne | Type | Description |
|---|---|---|
| `component_id` | string | Identifiant unique de composante (C01 à C04) |
| `component_name` | string | Nom de la composante du programme |
| `activity_type` | string | Type d'activité |
| `strategic_axis` | string | Axe stratégique |
| `unit_of_measure` | string | Unité de mesure |

### dim_manager.csv

| Colonne | Type | Description |
|---|---|---|
| `manager_id` | string | Identifiant unique du responsable (M01 à M06) |
| `manager_name` | string | Nom du responsable |
| `team_name` | string | Nom de l'équipe |
| `role` | string | Rôle (Zone Manager) |
| `seniority_level` | string | Niveau d'ancienneté (Senior, Mid) |

---

## Tables factuelles

### fact_monthly_performance.csv

| Colonne | Type | Description |
|---|---|---|
| `date_key` | date | Clé de date (lien vers dim_calendar) |
| `zone_id` | string | Clé de zone (lien vers dim_zone) |
| `component_id` | string | Clé de composante (lien vers dim_program_component) |
| `manager_id` | string | Clé du responsable (lien vers dim_manager) |
| `planned_activities` | integer | Nombre d'activités planifiées pour le mois |
| `completed_activities` | integer | Nombre d'activités effectivement réalisées |
| `target_beneficiaries` | integer | Nombre de bénéficiaires ciblés |
| `actual_beneficiaries` | integer | Nombre de bénéficiaires effectivement atteints |
| `target_output_units` | integer | Nombre d'unités de production ciblées |
| `actual_output_units` | integer | Nombre d'unités de production effectivement livrées |
| `reports_expected` | integer | Nombre de rapports attendus |
| `reports_submitted` | integer | Nombre de rapports effectivement soumis |
| `reports_submitted_on_time` | integer | Nombre de rapports soumis dans les délais |
| `open_issues` | integer | Nombre de problèmes ouverts |
| `closed_issues` | integer | Nombre de problèmes clôturés |
| `high_priority_alerts` | integer | Nombre d'alertes de haute priorité |

### fact_budget.csv

| Colonne | Type | Description |
|---|---|---|
| `date_key` | date | Clé de date (lien vers dim_calendar) |
| `zone_id` | string | Clé de zone (lien vers dim_zone) |
| `component_id` | string | Clé de composante (lien vers dim_program_component) |
| `planned_budget` | integer | Budget planifié pour le mois (en XOF) |
| `spent_budget` | integer | Budget effectivement dépensé |
| `committed_budget` | integer | Budget engagé (dépensé + engagements en cours) |
| `variance_amount` | integer | Écart budgétaire en valeur absolue |
| `variance_percent` | float | Écart budgétaire en pourcentage |

---

## Fichier consolidé

### dashboard_input.csv

Ce fichier regroupe toutes les tables dimensionnelles et factuelles en un seul dataset prêt à charger dans Power BI. Il contient l'ensemble des colonnes listées ci-dessus, plus les colonnes calculées suivantes :

| Colonne calculée | Type | Formule | Description |
|---|---|---|---|
| `activity_completion_rate` | float | completed / planned | Taux d'achèvement des activités |
| `beneficiary_achievement_rate` | float | actual / target | Taux d'atteinte des bénéficiaires |
| `output_achievement_rate` | float | actual / target | Taux d'atteinte des outputs |
| `reporting_on_time_rate` | float | on_time / expected | Taux de reporting à temps |
| `budget_execution_rate` | float | spent / planned | Taux d'exécution budgétaire |
| `alert_flag` | integer | 0 ou 1 | Indicateur d'alerte (voir critères ci-dessous) |

### Critères d'alerte (`alert_flag = 1`)

Un enregistrement est marqué en alerte si au moins une des conditions suivantes est vraie :

- `activity_completion_rate` < 0.80
- `beneficiary_achievement_rate` < 0.80
- `budget_execution_rate` > 1.05
- `reporting_on_time_rate` < 0.75
- `high_priority_alerts` >= 2
