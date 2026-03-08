# Choix de conception

Ce document explique les décisions de conception prises pour ce tableau de bord.

---

## Principes fondamentaux

### 1. Sobriété avant tout

- Peu d'indicateurs, mais bien choisis.
- Pas de surcharge visuelle.
- Pas d'effet "sapin de Noël" (couleurs multiples, animations inutiles).
- Chaque élément visible doit servir une décision.

### 2. Hiérarchie claire de l'information

- **Niveau 1** : ce qu'un dirigeant voit en 10 secondes.
- **Niveau 2** : ce qu'un analyste explore en 2 minutes.
- **Niveau 3** : ce qu'un opérationnel filtre pour son contexte.

### 3. Lecture orientée action

Chaque visuel répond à une question métier :

| Visuel | Question |
|---|---|
| KPI cards | Où en sommes-nous globalement ? |
| Tendance mensuelle | La trajectoire est-elle favorable ? |
| Classement par zone | Qui performe, qui décroche ? |
| Budget vs résultats | Dépensons-nous de manière cohérente ? |
| Table d'alertes | Où faut-il agir maintenant ? |

---

## Choix visuels

### Palette de couleurs

- Fond sombre pour la lisibilité en comité.
- Couleurs d'accent limitées à 2-3 tons.
- Rouge réservé aux alertes critiques.
- Vert utilisé avec modération (pas de "tout est vert").

### Typographie

- Titres lisibles et hiérarchisés.
- Chiffres en taille suffisante pour une lecture rapide.
- Labels courts et explicites.

### Disposition

- Lecture de gauche à droite, de haut en bas.
- KPI en bandeau supérieur.
- Détail progressif vers le bas de la page.

---

## Choix techniques

### Modèle de données

- Structure en étoile (dim/fact) pour la clarté.
- Un fichier consolidé (`dashboard_input.csv`) pour simplifier le chargement.
- Colonnes calculées incluses dans le fichier source pour réduire la charge du modèle.

### Filtres

- 5 filtres principaux maximum par page.
- Pas de filtres redondants.
- Pas de filtres trop techniques.

### Ce qui n'a pas été fait volontairement

- Pas de drill-through complexe.
- Pas de bookmarks multiples.
- Pas de visualisations personnalisées extravagantes.
- Pas de DAX ultra-complexe au détriment de la lisibilité.

---

## Pourquoi ces choix

> Un bon tableau de bord n'est pas celui qui impressionne par sa complexité.
> C'est celui qui permet à un décideur de comprendre la situation et d'agir.

La complexité technique est un moyen, pas une fin. La vraie valeur est dans la **clarté décisionnelle**.

---

## Note Passe 2 — Lisibilité exportable

La Passe 2 a renforcé les choix suivants :

- **Sobriété visuelle** : réduction des effets superflus, respiration accrue.
- **Cohérence des codes couleurs** : vert = conforme, orange = vigilance, rouge = critique.
- **Distinction claire** entre preuve versionnable (charts + PDF) et futur dashboard Power BI natif.
- **Priorité à l'exportabilité** : le PDF de synthèse doit être partageable tel quel, sans contexte supplémentaire.
