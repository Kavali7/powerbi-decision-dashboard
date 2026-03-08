# Cadre des indicateurs (KPI Framework)

## Hiérarchie des indicateurs

Les indicateurs sont organisés en 3 niveaux de lecture.

---

## Niveau 1 — KPI de direction

Ces indicateurs sont visibles immédiatement en haut du dashboard. Ils répondent à la question : **où en sommes-nous globalement ?**

### 1. Taux global d'achèvement des activités

- **Formule** : `SUM(completed_activities) / SUM(planned_activities)`
- **Lecture** : proportion d'activités effectivement réalisées sur la période
- **Seuil d'alerte** : < 80%

### 2. Taux d'atteinte des bénéficiaires

- **Formule** : `SUM(actual_beneficiaries) / SUM(target_beneficiaries)`
- **Lecture** : proportion de bénéficiaires effectivement atteints
- **Seuil d'alerte** : < 80%

### 3. Taux d'exécution budgétaire

- **Formule** : `SUM(spent_budget) / SUM(planned_budget)`
- **Lecture** : proportion du budget effectivement consommé
- **Seuil d'alerte** : > 105% (surconsommation)

### 4. Taux de reporting à temps

- **Formule** : `SUM(reports_submitted_on_time) / SUM(reports_expected)`
- **Lecture** : discipline de reporting
- **Seuil d'alerte** : < 75%

### 5. Nombre de zones en alerte

- **Définition** : zones avec au moins un indicateur en alerte
- **Critères** : activity_completion_rate < 0.80 OU beneficiary_achievement_rate < 0.80 OU budget_execution_rate > 1.05 OU reporting_on_time_rate < 0.75 OU high_priority_alerts >= 2

### 6. Écart budgétaire global

- **Formule** : `SUM(spent_budget) - SUM(planned_budget)`
- **Lecture** : montant total de l'écart budgétaire en valeur absolue

---

## Niveau 2 — KPI analytiques

Ces indicateurs permettent une **lecture plus fine** des performances.

### 7. Taux d'atteinte des outputs

- **Formule** : `SUM(actual_output_units) / SUM(target_output_units)`

### 8. Taux de soumission des rapports

- **Formule** : `SUM(reports_submitted) / SUM(reports_expected)`

### 9. Taux de résolution des problèmes

- **Formule** : `SUM(closed_issues) / (SUM(open_issues) + SUM(closed_issues))`

### 10. Variation mensuelle de performance

- Évolution du taux d'achèvement par rapport au mois précédent

### 11. Zone la plus performante

- Classement selon un score composite pondéré

### 12. Zone la plus en difficulté

- Classement inverse selon le même score composite

---

## Niveau 3 — Score composite (optionnel)

### 13. Score de pilotage global

Score synthétique pondéré pour un résumé rapide.

| Composante | Pondération |
|---|---|
| Activités réalisées | 35% |
| Bénéficiaires atteints | 25% |
| Reporting à temps | 20% |
| Discipline budgétaire | 20% |

> **Note** : Ce score est indicatif. Il ne doit pas être l'unique lecture. Les indicateurs de niveau 1 restent la référence principale.
