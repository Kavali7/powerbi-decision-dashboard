# Guide de lecture du dashboard

> Les visuels de référence pour ce guide se trouvent dans `assets/charts/`, générés à partir du dataset du dépôt.

## Logique de lecture en 10 secondes

Un décideur doit pouvoir capter l'essentiel en regardant le dashboard pendant 10 secondes.

### Secondes 1-2 — Où en sommes-nous ?

Regarder les **6 KPI principaux** en haut du dashboard :

- Taux d'achèvement des activités
- Taux d'atteinte des bénéficiaires
- Taux d'exécution budgétaire
- Taux de reporting à temps
- Nombre de zones en alerte
- Écart budgétaire global

### Secondes 3-4 — La trajectoire est-elle bonne ?

Lire la **tendance mensuelle** :

- Les colonnes montrent le planifié
- La ligne montre le réalisé
- L'écart entre les deux raconte l'histoire

### Secondes 5-6 — Quelles zones décrochent ?

Observer le **classement par zone** :

- Barres horizontales, triées de la meilleure à la moins performante
- Les zones en bas du classement nécessitent attention

### Secondes 7-8 — Dépense vs exécution ?

Vérifier la **cohérence budget-résultats** :

- Une zone qui dépense beaucoup mais produit peu est une alerte
- Une zone qui produit bien avec peu de budget est un modèle

### Secondes 9-10 — Où agir ?

Consulter la **table d'alertes** :

- Zone concernée
- Composante impactée
- Type d'alerte
- Niveau de gravité

## Structure du dashboard

### Page 1 — Vue dirigeant

| Zone | Contenu |
|---|---|
| Bandeau supérieur | Titre, période active, mention "données synthétiques" |
| Ligne KPI | 6 cartes de KPI principaux |
| Tendance centrale | Colonnes (planifié) + ligne (réalisé) par mois |
| Comparaison par zone | Barres horizontales classées |
| Budget vs résultats | Barres groupées par zone |
| Alertes | Table courte avec zone, composante, indicateur, niveau |

### Page 2 — Vue opérationnelle

| Zone | Contenu |
|---|---|
| Filtres | Période, zone, composante, responsable |
| Détail composante | Barres planifié vs réalisé par composante |
| Détail responsable | Performance par manager |
| Reporting | Taux de soumission et problèmes ouverts/fermés |
| Tableau analytique | Table filtrable avec toutes les dimensions |

## Filtres disponibles

| Filtre | Options |
|---|---|
| Période | Mois, trimestre, année |
| Zone | Les 6 zones du programme |
| Composante | Mobilisation, Formation, Suivi, Appui |
| Responsable | Les 6 managers |
| Priorité | High, Medium |
