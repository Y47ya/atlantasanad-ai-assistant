# ADR-001 : Choix de l'architecture d'orchestration

## Contexte

L'assistant est destiné à un usage public. Les utilisateurs peuvent poser des questions de nature variée, pouvant nécessiter :

* une recherche dans la base documentaire (RAG) ;
* un ou plusieurs appels aux APIs métiers ;
* une combinaison de ces deux sources.

Les scénarios d'utilisation ne pouvant pas être définis à l'avance, l'architecture doit rester suffisamment flexible pour traiter différents types de requêtes.

---

## Options considérées

### Option 1 : Routage par règles

Le routage est réalisé à l'aide de règles codées (`if/else`).

* Architecture simple à implémenter.
* Peu flexible.
* Chaque nouveau scénario nécessite l'ajout de nouvelles règles.

---

### Option 2 : LLM Router

Un LLM analyse la question et choisit l'une des routes suivantes :

* RAG ;
* API ;
* RAG + API.

Le workflow reste entièrement défini dans le code.

* Les différents chemins d'exécution doivent être définis à l'avance.
* Devient moins adapté lorsque les scénarios métier se multiplient.

---

### Option 3 : Agent avec outils

Le RAG et les APIs sont exposés sous forme de **tools**. L'agent sélectionne automatiquement le ou les outils nécessaires en fonction de la question.

**Avantages**

* Grande flexibilité.
* Adapté à des questions variées et imprévisibles.
* Possibilité d'utiliser un ou plusieurs outils pour une même requête.
* Ajout de nouveaux outils sans modification de la logique générale.

---

## Décision

Le projet adopte une architecture basée sur un **agent unique** utilisant des **tools**.

Les principaux outils seront :

* un outil de recherche documentaire (RAG) ;
* les APIs métiers.

Ce choix est retenu car l'assistant est destiné à un usage public, où les questions ne sont pas connues à l'avance. Une même requête peut nécessiter plusieurs sources d'information, ce qui rend une architecture basée sur un agent plus adaptée qu'un routage prédéfini.

---

## Architecture retenue

* Le système reposera sur un **agent unique** chargé d'orchestrer les traitements.
* Le moteur RAG sera exposé comme un **tool**.
* Chaque API métier sera également exposée comme un **tool**.
* L'agent analysera la requête de l'utilisateur et sélectionnera automatiquement le ou les tools nécessaires afin de produire la réponse la plus pertinente.
