# Mesures DAX — Decision Dashboard Showcase

> **Mode d'emploi** : créer une table vide nommée `Measures` dans Power BI
> (Accueil > Entrer des données > nommer "Measures" > Charger),
> puis créer chaque mesure ci-dessous dans cette table.
>
> Copier-coller chaque bloc DAX tel quel dans l'éditeur de mesures.

---

## 1. Volumes de base

```dax
Planned Activities = SUM(fact_monthly_performance[planned_activities])
```

```dax
Completed Activities = SUM(fact_monthly_performance[completed_activities])
```

```dax
Target Beneficiaries = SUM(fact_monthly_performance[target_beneficiaries])
```

```dax
Actual Beneficiaries = SUM(fact_monthly_performance[actual_beneficiaries])
```

```dax
Target Output Units = SUM(fact_monthly_performance[target_output_units])
```

```dax
Actual Output Units = SUM(fact_monthly_performance[actual_output_units])
```

```dax
Reports Expected = SUM(fact_monthly_performance[reports_expected])
```

```dax
Reports Submitted = SUM(fact_monthly_performance[reports_submitted])
```

```dax
Reports Submitted On Time = SUM(fact_monthly_performance[reports_submitted_on_time])
```

```dax
Open Issues = SUM(fact_monthly_performance[open_issues])
```

```dax
Closed Issues = SUM(fact_monthly_performance[closed_issues])
```

```dax
High Priority Alerts = SUM(fact_monthly_performance[high_priority_alerts])
```

```dax
Planned Budget = SUM(fact_budget[planned_budget])
```

```dax
Spent Budget = SUM(fact_budget[spent_budget])
```

```dax
Committed Budget = SUM(fact_budget[committed_budget])
```

---

## 2. Taux principaux (KPI)

```dax
Activity Completion Rate =
DIVIDE([Completed Activities], [Planned Activities])
```

```dax
Beneficiary Achievement Rate =
DIVIDE([Actual Beneficiaries], [Target Beneficiaries])
```

```dax
Output Achievement Rate =
DIVIDE([Actual Output Units], [Target Output Units])
```

```dax
Reporting Submission Rate =
DIVIDE([Reports Submitted], [Reports Expected])
```

```dax
Reporting On Time Rate =
DIVIDE([Reports Submitted On Time], [Reports Expected])
```

```dax
Budget Execution Rate =
DIVIDE([Spent Budget], [Planned Budget])
```

```dax
Issue Resolution Rate =
DIVIDE([Closed Issues], [Open Issues] + [Closed Issues])
```

---

## 3. Écarts

```dax
Budget Variance Amount = [Spent Budget] - [Planned Budget]
```

```dax
Budget Variance Percent =
DIVIDE([Budget Variance Amount], [Planned Budget])
```

```dax
Activities Gap = [Completed Activities] - [Planned Activities]
```

```dax
Beneficiaries Gap = [Actual Beneficiaries] - [Target Beneficiaries]
```

---

## 4. Reporting décomposé (pour barre empilée)

```dax
Reports Late = [Reports Submitted] - [Reports Submitted On Time]
```

```dax
Reports Not Submitted = [Reports Expected] - [Reports Submitted]
```

---

## 5. Alertes et pilotage

```dax
Zone Alert Flag =
VAR acr = [Activity Completion Rate]
VAR bar = [Beneficiary Achievement Rate]
VAR ber = [Budget Execution Rate]
VAR rtr = [Reporting On Time Rate]
VAR hpa = [High Priority Alerts]
RETURN
IF(
    acr < 0.80 ||
    bar < 0.80 ||
    ber > 1.05 ||
    rtr < 0.75 ||
    hpa >= 2,
    1,
    0
)
```

```dax
Zones In Alert =
SUMX(
    VALUES(dim_zone[zone_id]),
    [Zone Alert Flag]
)
```

```dax
Total Alert Records =
COUNTROWS(
    FILTER(
        fact_monthly_performance,
        CALCULATE([Activity Completion Rate]) < 0.80 ||
        CALCULATE([Beneficiary Achievement Rate]) < 0.80 ||
        CALCULATE([Budget Execution Rate]) > 1.05 ||
        CALCULATE([Reporting On Time Rate]) < 0.75 ||
        fact_monthly_performance[high_priority_alerts] >= 2
    )
)
```

```dax
Alert Rate = DIVIDE([Total Alert Records], COUNTROWS(fact_monthly_performance))
```

---

## 6. Score de pilotage (optionnel, pour tri des zones)

```dax
Pilotage Score =
(
    [Activity Completion Rate] * 0.35 +
    [Beneficiary Achievement Rate] * 0.25 +
    [Reporting On Time Rate] * 0.20 +
    (1 - ABS(1 - [Budget Execution Rate])) * 0.20
)
```

---

## 7. Mise en forme conditionnelle (texte de statut)

```dax
Activity Status =
SWITCH(
    TRUE(),
    [Activity Completion Rate] >= 0.85, "Conforme",
    [Activity Completion Rate] >= 0.70, "À surveiller",
    "Critique"
)
```

```dax
Budget Status =
SWITCH(
    TRUE(),
    [Budget Execution Rate] <= 1.05 && [Budget Execution Rate] >= 0.85, "Maîtrisé",
    [Budget Execution Rate] > 1.05, "Dépassement",
    "Sous-consommation"
)
```

---

## 8. Texte dynamique de période (pour titre de page)

```dax
Period Label =
VAR MinDate = MIN(dim_calendar[date_key])
VAR MaxDate = MAX(dim_calendar[date_key])
RETURN
FORMAT(MinDate, "MMM YYYY") & " – " & FORMAT(MaxDate, "MMM YYYY")
```

---

## 9. Budget en millions (pour affichage lisible)

```dax
Planned Budget M = DIVIDE([Planned Budget], 1000000)
```

```dax
Spent Budget M = DIVIDE([Spent Budget], 1000000)
```

```dax
Budget Variance M = DIVIDE([Budget Variance Amount], 1000000)
```

---

## Rappel : mise en forme dans Power BI

| Mesure | Format recommandé |
|---|---|
| Taux (%) | Pourcentage, 0 décimale |
| Budgets bruts | Nombre entier, séparateur milliers |
| Budgets M | Nombre décimal, 1 décimale |
| Écart budgétaire | Nombre entier, signe +/- |
| Zones In Alert | Nombre entier |
| Scores | Nombre décimal, 2 décimales |
| Statuts texte | Texte (pas de format) |

---

## Relations à créer (rappel)

```
dim_calendar[date_key]             → fact_monthly_performance[date_key]
dim_calendar[date_key]             → fact_budget[date_key]
dim_zone[zone_id]                  → fact_monthly_performance[zone_id]
dim_zone[zone_id]                  → fact_budget[zone_id]
dim_program_component[component_id] → fact_monthly_performance[component_id]
dim_program_component[component_id] → fact_budget[component_id]
dim_manager[manager_id]            → fact_monthly_performance[manager_id]
```

> Direction : simple · Cardinalité : one-to-many
