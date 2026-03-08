# Ce dossier contient le fichier Power BI du dashboard décisionnel

## Statut actuel

Le fichier `.pbix` n'est pas inclus dans cette version publique du dépôt.

Ce dépôt montre la structure complète, les données sources, les visuels de démonstration et la logique métier du tableau de bord.

## Reconstruction du dashboard

Le dashboard Power BI peut être reconstruit à partir des éléments suivants :

1. **Dataset principal** : `data/processed/dashboard_input.csv`
2. **Dictionnaire de données** : `data/dictionary/data_dictionary.md`
3. **Liste des KPI** : `docs/kpi-framework.md`
4. **Guide de lecture** : `docs/dashboard-reading-guide.md`
5. **Choix de conception** : `docs/design-decisions.md`

## Structure recommandée du fichier Power BI

Le dashboard comporte deux pages :

### Page 1 — Vue dirigeant

- Bandeau de KPI (6 cartes)
- Tendance mensuelle (colonnes + ligne)
- Comparaison par zone (barres horizontales)
- Budget vs résultats (barres groupées)
- Table d'alertes

### Page 2 — Vue opérationnelle

- Filtres (période, zone, composante, responsable)
- Détail par composante
- Détail par responsable
- Reporting et problèmes
- Tableau analytique filtrable

## Pourquoi le fichier `.pbix` n'est pas inclus

- Un fichier `.pbix` vide ou factice n'apporte aucune valeur.
- Les captures d'écran et la documentation montrent le résultat final.
- Le dataset fourni permet de reconstruire le dashboard facilement.
- Cette approche est plus honnête et plus crédible.
