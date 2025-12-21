# Projet de Recherche Opérationnelle — Problème de Transport

Ce projet implémente et compare plusieurs algorithmes classiques de **Recherche Opérationnelle** pour la résolution du **problème de transport** :

* Méthode du **Nord-Ouest**
* Méthode de **Balas-Hammer**
* Optimisation par la méthode du **Marche-Pied (Stepping Stone)**

L’objectif est de fournir :

* une implémentation claire et modulaire des algorithmes,
* des outils d’analyse (traces, benchmarks),
* une structure de code lisible et défendable dans un cadre académique.

---
## 👥 Membres de l’équipe
- [Inès Benalia](https://github.com/JuGurThales)
- [Nicolas E.](https://github.com/Legallait)
- [Yannick Han](https://github.com/Imyahan)
- [TorielLink](https://github.com/TorielLink)
- [Kim Lan Tran](https://github.com/Kim0871)

---

## 📁 Structure du projet

```
projet-recherche-op-probleme-de-transport/
│
├── algorithms/                 # Algorithmes de transport
│   ├── northwest.py            # Méthode du Nord-Ouest
│   ├── BalasHammer.py          # Méthode de Balas-Hammer
│   └── stepping_stone.py       # Méthode du Marche-Pied
│
├── utils/                      # Outils transverses
│   ├── graph/                  # Graphes, cycles, connexité
│   │   ├── connectivity.py
│   │   ├── cycle_graph.py
│   │   └── cycle_optimization.py
│   ├── math/                   # Calculs mathématiques
│   │   ├── cost.py
│   │   └── stepping_stone_costs.py
│   ├── io/                     # Entrées / sorties fichiers
│   │   ├── table_reader.py
│   │   └── trace_writer.py
│   ├── display/                # Affichage console
│   │   └── table_display.py
│   ├── generation/             # Génération de problèmes aléatoires
│   │   └── ramdom_problem.py
│   └── benchmark/              # Mesures de performance
│       └── timing.py
│
├── Tableaux/                   # Fichiers de données d’entrée
├── Traces/                     # Traces générées automatiquement
├── Data/                       # Données de benchmark (CSV)
├── Figures/                    # Graphiques de complexité
│
├── main.py                     # Interface principale utilisateur
├── generate_all_traces.py      # Génération automatique des traces
├── main_time_test.py           # Benchmarks simples
├── main_time_cloud.py          # Nuages de points de complexité
│
└── README.md
```

---

## ⚙️ Algorithmes implémentés

### 1️⃣ Méthode du Nord-Ouest

* Fournit une **solution initiale faisable**
* Très rapide mais généralement non optimale
* Implémentée dans `algorithms/northwest.py`

### 2️⃣ Méthode de Balas-Hammer

* Solution initiale améliorée par rapport au Nord-Ouest
* Basée sur le calcul de **pénalités lignes / colonnes**
* Implémentée dans `algorithms/BalasHammer.py`

### 3️⃣ Méthode du Marche-Pied (Stepping Stone)

* Méthode d’optimisation itérative
* Utilise :

  * la connexité du graphe de base,
  * les potentiels,
  * les coûts marginaux,
  * la recherche de cycles
* Implémentée dans `algorithms/stepping_stone.py`

---

## ▶️ Utilisation

### Lancer le programme principal

```bash
python main.py
```

Le programme permet de :

1. choisir un problème de transport,
2. calculer une solution initiale (Nord-Ouest ou Balas-Hammer),
3. optimiser la solution avec le Marche-Pied,
4. afficher les résultats et les coûts.

---

### Générer toutes les traces

```bash
python generate_all_traces.py
```

Ce script :

* génère automatiquement les solutions et optimisations,
* produit des fichiers de traces détaillés dans le dossier `Traces/`.

---

### Benchmarks et complexité

* **Benchmarks simples** :

```bash
python main_time_test.py
```

* **Nuages de points (complexité)** :

```bash
python main_time_cloud.py
```

Les résultats sont sauvegardés dans :

* `Data/` (CSV)
* `Figures/` (graphiques)

---

## 🧠 Choix de conception

* Séparation stricte entre :

  * algorithmes,
  * outils mathématiques,
  * graphes,
  * entrées / sorties,
  * affichage.
* Code volontairement **lisible et commenté simplement**.
* Architecture pensée pour un **projet académique** et une **présentation orale**.

---

## 📌 Remarques

* Les problèmes générés aléatoirement sont **équilibrés** (somme des provisions = somme des commandes).
* Les affichages de debug peuvent être activés/désactivés via le paramètre `display`.

---

## 👨‍🎓 Contexte

Projet réalisé dans le cadre d’un enseignement de **Recherche Opérationnelle**, visant à illustrer :

* la modélisation du problème de transport,
* la comparaison de méthodes exactes et heuristiques,
* l’analyse expérimentale des performances.

---

## ✅ État du projet

✔ Code fonctionnel
✔ Structure claire
✔ Algorithmes testés
✔ Prêt pour rendu et soutenance
