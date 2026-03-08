# Decision Dashboard Showcase

**Démonstration de tableau de bord décisionnel pour le pilotage d'activité.**

Ce dépôt montre comment des données d'activité dispersées peuvent être transformées en un tableau de bord clair, synthétique et exploitable pour le pilotage.

L'objectif n'est pas de présenter un outil pour lui-même, mais de montrer un résultat concret :
**aider un dirigeant, un coordonnateur ou un responsable à voir l'essentiel, repérer les écarts et décider plus vite.**

> Power BI est utilisé comme support de restitution, pas comme finalité.
> Ce qui compte ici, c'est la **lecture décisionnelle**, pas l'outil.

---

## Ce qu'un dirigeant voit en 10 secondes

1. **Niveau global d'exécution** — sommes-nous en ligne avec les objectifs ?
2. **Tendance récente** — la trajectoire est-elle favorable ou défavorable ?
3. **Zones en avance ou en retard** — qui performe, qui décroche ?
4. **Cohérence budget / résultats** — dépensons-nous de manière cohérente ?
5. **Alertes prioritaires** — où faut-il agir maintenant ?

---

## À qui s'adresse cette démonstration

Cette démonstration est pensée pour des organisations qui ont besoin de mieux suivre leurs performances, leur exécution ou leurs résultats, notamment :

- ONG et programmes internationaux.
- PME et entreprises structurées.
- Institutions et administrations.
- Structures de services et cabinets.
- Directions opérationnelles et équipes de pilotage.

---

## Le problème métier traité

Dans beaucoup d'organisations, les données existent déjà, mais elles sont souvent :

- dispersées entre plusieurs fichiers ;
- difficiles à consolider ;
- lues trop tardivement ;
- peu comparables d'une zone à l'autre ;
- insuffisamment structurées pour aider à la décision.

Le problème n'est pas seulement la production de données.
Le problème est surtout **la difficulté à les transformer en lecture décisionnelle claire**.

---

## Ce que montre ce dépôt

Cette démonstration illustre comment structurer un tableau de bord pour répondre à des questions de pilotage simples mais critiques :

- Où en sommes-nous globalement par rapport aux objectifs ?
- Quelles zones performent le mieux ?
- Où se situent les écarts majeurs ?
- La dynamique récente est-elle favorable ?
- Le niveau de dépense est-il cohérent avec les résultats ?
- Quels points nécessitent une action rapide ?

---

## Cas d'usage démontré

Le cas retenu est celui d'un **programme multi-zones** déployé sur 6 zones en Afrique, qui suit mensuellement :

- des objectifs planifiés et des réalisations effectives ;
- des bénéficiaires atteints ;
- des budgets planifiés et consommés ;
- des responsables de zone ;
- des alertes de pilotage.

Ce choix permet une lecture transposable à plusieurs contextes : ONG, projet, PME, structure de services ou direction opérationnelle.

---

## Structure de la démonstration

Le dépôt contient :

- une **vue dirigeant** orientée synthèse ;
- une **vue opérationnelle** orientée analyse des écarts ;
- un **jeu de données fictif et synthétique** (6 zones, 4 composantes, 15 mois) ;
- des **scripts Python** de génération, préparation et visualisation des données ;
- un **dictionnaire de données** complet ;
- une **documentation métier** détaillée ;
- des **graphiques générés** à partir du dataset réel du dépôt ;
- une **checklist QA** de validation structurelle et métier.

---

## Visuels du dépôt

### Graphiques générés (`assets/charts/`)

Les 5 visuels présents dans `assets/charts/` sont **générés automatiquement** par le script `scripts/generate_charts.py` à partir du dataset synthétique `data/processed/dashboard_input.csv`.

Ils reflètent fidèlement les données du dépôt : mêmes zones, mêmes composantes, mêmes responsables, mêmes KPI, mêmes seuils d'alerte.

| Graphique | Contenu |
|---|---|
| `01-executive-overview.png` | KPI globaux, tendance mensuelle, classement par zone, alertes |
| `02-performance-by-zone.png` | Taux d'achèvement par zone, tableau récapitulatif |
| `03-budget-vs-results.png` | Budget planifié vs dépensé, scatter exécution vs performance |
| `04-alerts-table.png` | Heatmap zone × composante, détail par type d'alerte |
| `05-operational-view.png` | Composantes, responsables, reporting, problèmes |

### Captures Power BI (`assets/screenshots/`)

Les captures réelles du dashboard Power BI seront ajoutées lors de la construction du fichier `.pbix` (étape suivante).

---

## Données utilisées

**Toutes les données de ce dépôt sont fictives, synthétiques et créées uniquement à des fins de démonstration.**

Elles ne correspondent à aucun client réel, aucun projet réel et aucun résultat réel livré. Le but est uniquement de montrer une approche de structuration, de restitution et de lecture décisionnelle.

---

## Principaux indicateurs suivis

Le tableau de bord met en avant 6 indicateurs de pilotage essentiels :

| Indicateur | Formule | Seuil d'alerte |
|---|---|---|
| Taux d'achèvement des activités | Réalisées / Planifiées | < 80% |
| Taux d'atteinte des bénéficiaires | Atteints / Ciblés | < 80% |
| Taux d'exécution budgétaire | Dépensé / Planifié | > 105% |
| Taux de reporting à temps | À temps / Attendus | < 75% |
| Nombre de zones en alerte | Zones avec indicateur critique | — |
| Écart budgétaire global | Dépensé - Planifié | — |

L'approche privilégie une lecture sobre, hiérarchisée et orientée action.

---

## Fichiers importants

### Dashboard

- [`dashboard/powerbi/`](dashboard/powerbi/) — Instructions de reconstruction du dashboard

### Données

- [`data/raw/`](data/raw/) — Tables dimensionnelles et factuelles (6 fichiers CSV)
- [`data/processed/dashboard_input.csv`](data/processed/dashboard_input.csv) — Dataset consolidé (360 lignes)
- [`data/dictionary/data_dictionary.md`](data/dictionary/data_dictionary.md) — Dictionnaire de données

### Scripts

- [`scripts/generate_synthetic_data.py`](scripts/generate_synthetic_data.py) — Génération des données synthétiques
- [`scripts/prepare_dashboard_input.py`](scripts/prepare_dashboard_input.py) — Préparation du dataset consolidé
- [`scripts/generate_charts.py`](scripts/generate_charts.py) — Génération des graphiques à partir des données
- [`scripts/validate_outputs.py`](scripts/validate_outputs.py) — Validation QA du dataset et des livrables

### Documentation

- [`docs/business-case.md`](docs/business-case.md) — Cas métier et contexte
- [`docs/dashboard-reading-guide.md`](docs/dashboard-reading-guide.md) — Guide de lecture du dashboard
- [`docs/kpi-framework.md`](docs/kpi-framework.md) — Cadre des indicateurs
- [`docs/adaptation-by-sector.md`](docs/adaptation-by-sector.md) — Adaptation à d'autres secteurs
- [`docs/design-decisions.md`](docs/design-decisions.md) — Choix de conception
- [`docs/qa-checklist.md`](docs/qa-checklist.md) — Checklist de validation qualité

---

## Choix de conception

Cette démonstration suit quelques principes simples :

- peu d'indicateurs, mais bien choisis ;
- forte lisibilité ;
- hiérarchie claire de l'information ;
- pas de surcharge visuelle ;
- priorité à la décision plutôt qu'à la décoration.

---

## Adaptation à d'autres secteurs

Le même modèle peut être adapté à :

- une **PME commerciale** : ventes, objectifs, zones, produits, équipes ;
- une **entreprise de distribution** : volumes, couverture, agents, performance mensuelle ;
- un **centre de formation** : inscriptions, présence, recettes, performance par filière ;
- une **structure de services** : activité, rentabilité, délais, responsables ;
- une **direction opérationnelle** : exécution, résultats, écarts, alertes.

---

## Stack utilisée

| Outil | Usage |
|---|---|
| Power BI | Restitution et visualisation (dashboard réel à venir) |
| Python / Matplotlib | Génération des données, préparation, graphiques et validation |
| CSV | Format des données de démonstration |

---

## Utilisation commerciale possible

Ce dépôt peut servir comme :

- preuve de compétence ;
- support de prospection ;
- vitrine GitHub ;
- base pour une présentation client ;
- annexe dans un PDF commercial.

---

## Ce que cette démonstration ne prétend pas

Cette démonstration :

- ne présente aucun client réel ;
- ne contient aucun faux témoignage ;
- ne revendique aucun résultat chiffré réel ;
- ne remplace pas un cadrage métier client ;
- ne prétend pas qu'un dashboard seul résout tous les problèmes de pilotage.

Elle montre une méthode, une logique de restitution et un niveau d'exécution.

---

## Contact

Je conçois ce type de tableau de bord pour aider des organisations à mieux structurer, suivre et restituer leurs données de pilotage.

Pour échanger sur un besoin similaire, vous pouvez me contacter directement.

---

## Licence

Tous droits réservés. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
