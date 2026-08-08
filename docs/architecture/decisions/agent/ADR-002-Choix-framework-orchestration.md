# ADR-002 : Choix du framework d'orchestration

## Contexte

L'architecture retenue repose sur un agent capable d'utiliser plusieurs outils, notamment :

- un moteur RAG pour l'interrogation documentaire ;
- des APIs métiers ;
- de futurs outils pouvant être ajoutés au cours de l'évolution du projet.

Le framework retenu doit donc permettre de construire un workflow clair, facilement évolutif et compatible avec une architecture basée sur des tools.

---

## Options considérées

### Option 1 — Développement sans framework

L'orchestration est entièrement développée en Python.

Cette approche offre un contrôle total sur le comportement du système mais nécessite d'implémenter manuellement la logique de routage, la gestion des états, l'exécution des outils et les évolutions futures.

Elle est adaptée à de petits projets mais augmente rapidement la complexité de maintenance lorsqu'un assistant doit évoluer.

---

### Option 2 — LangChain

LangChain fournit de nombreux composants prêts à l'emploi pour construire rapidement des applications LLM.

Il facilite l'intégration des modèles, des prompts, des outils et des agents.

Cependant, lorsque les workflows deviennent plus complexes, une partie de la logique d'exécution est masquée par le framework, ce qui rend le comportement global moins explicite et plus difficile à faire évoluer.

---

### Option 3 — LlamaIndex

LlamaIndex est principalement spécialisé dans les applications basées sur le RAG.

Il propose de nombreuses fonctionnalités pour l'indexation documentaire et la recherche d'information.

En revanche, son objectif principal n'est pas l'orchestration complète d'un assistant utilisant plusieurs outils métiers.

---

### Option 4 — CrewAI

CrewAI permet de construire des systèmes composés de plusieurs agents collaborant entre eux.

Cette approche est particulièrement adaptée lorsque différentes tâches doivent être réparties entre plusieurs agents spécialisés.

Dans notre contexte, l'assistant repose sur un agent unique capable de sélectionner les outils nécessaires. Une architecture multi-agents apporterait une complexité supplémentaire sans réel bénéfice fonctionnel.

---

### Option 5 — LangGraph

LangGraph construit l'application sous forme d'un graphe représentant explicitement les différentes étapes du workflow.

Chaque nœud possède une responsabilité précise et les transitions entre les étapes sont entièrement contrôlées par le développeur.

Cette approche permet de faire évoluer progressivement le système en ajoutant de nouveaux traitements, de nouveaux outils ou de nouvelles branches d'exécution sans modifier l'architecture globale.

---

## Décision

Le projet adopte **LangGraph** comme framework d'orchestration.

Ce choix est motivé par plusieurs éléments propres au contexte du projet :

- l'assistant est destiné à évoluer avec l'ajout progressif de nouvelles APIs métiers ;
- plusieurs outils devront être utilisés selon la nature des questions ;
- le fonctionnement du système doit rester facilement compréhensible et maintenable par l'équipe de développement ;
- l'entreprise souhaite disposer d'une architecture modulaire pouvant évoluer sans réécriture importante.

LangGraph répond à ces exigences en offrant une orchestration explicite des traitements tout en restant compatible avec une architecture basée sur un agent utilisant des tools.

---

## Architecture retenue

Le workflow sera piloté par un graphe LangGraph.

L'agent constituera le nœud principal du graphe et pourra invoquer les différents tools disponibles (RAG, APIs métiers, futurs outils).

Cette architecture permet de séparer clairement les responsabilités entre :

- l'orchestration du workflow ;
- la prise de décision par l'agent ;
- l'exécution des traitements par les différents tools.

Elle facilite également l'évolution du système au fur et à mesure des besoins de l'entreprise.