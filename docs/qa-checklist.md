# Checklist QA — Decision Dashboard

Ce document décrit les vérifications de qualité appliquées au dataset et aux livrables.

---

## Vérifications automatisées

Le script `scripts/validate_outputs.py` vérifie automatiquement :

### Présence des fichiers

- 6 fichiers CSV dans `data/raw/`
- 1 fichier consolidé `data/processed/dashboard_input.csv`
- 5 graphiques PNG dans `assets/charts/`

### Structure des données

| Vérification | Attendu |
|---|---|
| Lignes dans `fact_monthly_performance.csv` | 360 |
| Lignes dans `fact_budget.csv` | 360 |
| Lignes dans `dashboard_input.csv` | 360 |
| Mois distincts | 15 (Jan 2024 – Mar 2025) |
| Zones distinctes | 6 |
| Composantes distinctes | 4 |
| Managers distincts | 6 |

### Cohérence métier

| Vérification | Critère |
|---|---|
| Activités réalisées | Jamais > 150% du planifié |
| Budget planifié | Jamais négatif |
| Alertes | Présentes mais pas omniprésentes |
| Zones en alerte | Au moins 2 zones concernées |
| `activity_completion_rate` | Cohérent avec completed / planned |
| `alert_flag` | Conforme aux 5 critères du KPI framework |

### Exécution

```bash
python scripts/validate_outputs.py
```

Sortie attendue : `ALL CHECKS PASSED`.

---

## Vérifications manuelles restantes

Ces points ne sont pas automatisables et doivent être vérifiés visuellement :

| Vérification | Statut |
|---|---|
| Dashboard Power BI réel construit | ⬜ À faire (Passe 3) |
| Captures réelles dans `assets/screenshots/` | ⬜ À faire (Passe 3) |
| Export PDF réel dans `assets/pdf/` | ✅ Fait (Passe 2) |
| Lecture "prospect non technique" du README | ⬜ À valider |
| Cohérence visuelle des graphiques | ✅ Vérifié (Passe 1) |

---

## Contrôles manuels Passe 2

| Vérification | Statut |
| --- | --- |
| PDF généré sans erreur (5 pages) | ✅ |
| Pagination correcte (1/5 à 5/5) | ✅ |
| Titre cohérent sur la couverture | ✅ |
| Mention "données synthétiques" visible | ✅ |
| Charts nets dans le PDF (graphiques pages 2 et 3) | ✅ |
| README mis à jour avec lien PDF | ✅ |
| Script PDF renommé (`generate_pdf_summary.py`) | ✅ |

---

## Critères d'alerte (`alert_flag = 1`)

Un enregistrement est marqué en alerte si au moins une condition est vraie :

- `activity_completion_rate` < 0.80
- `beneficiary_achievement_rate` < 0.80
- `budget_execution_rate` > 1.05
- `reporting_on_time_rate` < 0.75
- `high_priority_alerts` >= 2
