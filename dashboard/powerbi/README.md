# Ce dossier contient les éléments du dashboard décisionnel

## Statut actuel

Le fichier `.pbix` n'est pas inclus dans cette version du dépôt.

Le dépôt fournit actuellement :

- la structure complète des données ;
- le dataset consolidé prêt à charger ;
- des graphiques générés à partir des données réelles du dépôt ;
- la documentation métier et le cadre des indicateurs.

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

## Pourquoi le fichier `.pbix` n'est pas encore inclus

- Un fichier `.pbix` vide ou factice n'apporte aucune valeur.
- Les graphiques générés dans `assets/charts/` montrent les données réelles du dépôt.
- Le dataset fourni permet de reconstruire le dashboard facilement.
- Le `.pbix` réel sera ajouté dès que la V1 du dashboard sera construite.
