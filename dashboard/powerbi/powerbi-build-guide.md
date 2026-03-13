# Guide de construction du Dashboard Power BI

> Ce guide permet de reproduire le fichier `.pbix` de zéro.
> Chaque étape est numérotée et doit être suivie dans l'ordre.

---

## Étape 1 — Créer un rapport vierge

1. Ouvrir **Power BI Desktop**
2. Cliquer sur **Rapport vierge**

---

## Étape 2 — Importer les 6 fichiers CSV

Pour chaque fichier : **Accueil** → **Obtenir les données** → **Texte/CSV**

Chemin : `data/raw/`

| # | Fichier | Vérification |
|---|---|---|
| 1 | `dim_calendar.csv` | `date_key` → type **Date** |
| 2 | `dim_zone.csv` | `zone_id` → type **Texte** |
| 3 | `dim_program_component.csv` | `component_id` → type **Texte** |
| 4 | `dim_manager.csv` | `manager_id` → type **Texte** |
| 5 | `fact_monthly_performance.csv` | colonnes numériques → **Nombre entier** |
| 6 | `fact_budget.csv` | colonnes numériques → **Nombre entier** |

> **Si les colonnes s'affichent "Column1, Column2…"** :
> cliquer **Transformer les données** → **Utiliser la première ligne pour les en-têtes** → **Fermer et appliquer**

---

## Étape 3 — Créer la table Measures

1. **Accueil** → **Entrer des données**
2. Nommer la table `Measures`
3. Ne rien saisir
4. **Charger**

---

## Étape 4 — Créer les 7 relations

**Accueil** → **Gérer les relations** → **Nouveau…** (répéter 7 fois)

| # | Table du haut | Colonne | Table du bas | Colonne |
|---|---|---|---|---|
| 1 | `dim_calendar` | `date_key` | `fact_monthly_performance` | `date_key` |
| 2 | `dim_calendar` | `date_key` | `fact_budget` | `date_key` |
| 3 | `dim_zone` | `zone_id` | `fact_monthly_performance` | `zone_id` |
| 4 | `dim_zone` | `zone_id` | `fact_budget` | `zone_id` |
| 5 | `dim_program_component` | `component_id` | `fact_monthly_performance` | `component_id` |
| 6 | `dim_program_component` | `component_id` | `fact_budget` | `component_id` |
| 7 | `dim_manager` | `manager_id` | `fact_monthly_performance` | `manager_id` |

> Chaque relation doit afficher : **Cardinalité = Un à plusieurs (1:\*)** et **Direction = À sens unique**

---

## Étape 5 — Créer les mesures DAX

Clic droit sur `Measures` → **Nouvelle mesure** → **Ctrl+A** → coller → **Entrée**

### 5.1 — Volumes de base (8 mesures)

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
Reports Expected = SUM(fact_monthly_performance[reports_expected])
```

```dax
Reports Submitted On Time = SUM(fact_monthly_performance[reports_submitted_on_time])
```

```dax
Planned Budget = SUM(fact_budget[planned_budget])
```

```dax
Spent Budget = SUM(fact_budget[spent_budget])
```

### 5.2 — Taux KPI (4 mesures)

```dax
Activity Completion Rate = DIVIDE(SUM(fact_monthly_performance[completed_activities]), SUM(fact_monthly_performance[planned_activities]))
```

```dax
Beneficiary Achievement Rate = DIVIDE(SUM(fact_monthly_performance[actual_beneficiaries]), SUM(fact_monthly_performance[target_beneficiaries]))
```

```dax
Reporting On Time Rate = DIVIDE(SUM(fact_monthly_performance[reports_submitted_on_time]), SUM(fact_monthly_performance[reports_expected]))
```

```dax
Budget Execution Rate = DIVIDE(SUM(fact_budget[spent_budget]), SUM(fact_budget[planned_budget]))
```

### 5.3 — Écarts et alertes (3 mesures)

```dax
High Priority Alerts = SUM(fact_monthly_performance[high_priority_alerts])
```

```dax
Budget Variance Amount = SUM(fact_budget[spent_budget]) - SUM(fact_budget[planned_budget])
```

```dax
Zones In Alert = SUMX(VALUES(dim_zone[zone_id]), IF(DIVIDE(SUM(fact_monthly_performance[completed_activities]), SUM(fact_monthly_performance[planned_activities])) < 0.80 || DIVIDE(SUM(fact_monthly_performance[actual_beneficiaries]), SUM(fact_monthly_performance[target_beneficiaries])) < 0.80 || DIVIDE(SUM(fact_budget[spent_budget]), SUM(fact_budget[planned_budget])) > 1.05 || DIVIDE(SUM(fact_monthly_performance[reports_submitted_on_time]), SUM(fact_monthly_performance[reports_expected])) < 0.75 || SUM(fact_monthly_performance[high_priority_alerts]) >= 2, 1, 0))
```

> **Total : 15 mesures** dans la table Measures

### 5.4 — Mise en forme des mesures

Dans **Modélisation** → sélectionner chaque mesure → changer le format :

| Mesure | Format |
|---|---|
| Activity Completion Rate | Pourcentage, 0 décimale |
| Beneficiary Achievement Rate | Pourcentage, 0 décimale |
| Reporting On Time Rate | Pourcentage, 0 décimale |
| Budget Execution Rate | Pourcentage, 0 décimale |
| Planned Budget, Spent Budget | Nombre entier, séparateur milliers |
| Budget Variance Amount | Nombre entier, signe +/- |
| Zones In Alert | Nombre entier |

---

## Étape 6 — Page 1 : Résumé dirigeant

*(à compléter après construction)*

## Étape 7 — Page 2 : Analyse détaillée

*(à compléter après construction)*

## Étape 8 — Style et finitions

*(à compléter après construction)*

## Étape 9 — Export des captures

*(à compléter après construction)*

---

## Checklist de progression

- [x] Import des 6 CSV
- [x] Table Measures créée
- [x] 7 relations créées
- [x] 15 mesures DAX créées
- [ ] Mise en forme des mesures
- [ ] Page 1 — Résumé dirigeant
- [ ] Page 2 — Analyse détaillée
- [ ] Style visuel appliqué
- [ ] 3 captures exportées
- [ ] Sauvegarde `.pbix`
