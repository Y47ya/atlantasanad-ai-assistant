# Point d'avancement – Semaine 4

**Projet :** Assistant IA basé sur un système RAG pour ATLANTASANAD Assurance
**Période :** Semaine 4

---

# Objectif de la semaine

L'objectif principal de cette semaine était de commencer la seconde partie du projet, consacrée à l'intégration des API métiers au système RAG, afin de permettre à l'assistant de traiter à la fois les questions documentaires et les demandes nécessitant des données ou opérations métier.

---

# Travaux réalisés

## 1. Conception de l'architecture d'orchestration

Une architecture basée sur un **agent LLM avec outils (tools)** a été retenue.

L'agent peut sélectionner dynamiquement l'action nécessaire selon la question de l'utilisateur :

* recherche documentaire via le RAG ;
* appel d'une API métier ;

Cette approche permet de gérer des questions variées sans définir à l'avance un workflow spécifique pour chaque scénario.

---

## 2. Mise en place du squelette LangGraph

Le squelette de l'orchestrateur a été développé avec **LangGraph**.

Le workflow repose actuellement sur :

* un **Agent Node**, responsable de la décision et du raisonnement ;
* un **Tool Node**, responsable de l'exécution des outils sélectionnés par l'agent.

Le graphe permet ainsi de faire circuler les résultats des tools vers l'agent afin de produire la réponse finale.

---

## 3. Intégration du RAG comme outil

Le pipeline RAG développé précédemment a été intégré sous forme de **tool** utilisable par l'agent.

L'agent peut désormais identifier une question documentaire et déclencher automatiquement la recherche dans les documents internes avant de générer sa réponse.

---

## 4. Intégration des APIs métiers

Deux premières APIs métiers ont été intégrées sous forme de tools :

* **Simulation** : permet de réaliser une simulation d'assurance ;
* **Edition de devis** : permet de traiter un devis existant.

Une couche de service a également été mise en place afin de séparer la logique de l'agent de la communication avec les APIs.

En attendant l'accès aux APIs réelles, leur comportement est actuellement simulé à l'aide de **mock JSON** fournis pour le développement et les tests.

---

## 5. Gestion du contexte conversationnel

La conservation de l'historique des messages a été mise en place afin de permettre des interactions en plusieurs étapes.

Par exemple, l'utilisateur peut d'abord demander une simulation, puis fournir les informations demandées par l'assistant dans un message suivant sans avoir à répéter sa demande initiale.

---

# Résultats obtenus

Une première version fonctionnelle de l'agent est désormais opérationnelle.

Les tests réalisés permettent notamment de :

* détecter une question nécessitant le RAG et effectuer automatiquement la recherche ;
* identifier une demande de simulation et collecter les informations nécessaires ;
* appeler le tool correspondant avec les informations fournies ;
* récupérer le résultat du mock API ;
* générer une réponse finale à partir du résultat obtenu ;
* conserver le contexte entre plusieurs messages.

La boucle principale de l'agent est donc fonctionnelle :

**Utilisateur → Agent → Tool → Résultat → Agent → Réponse**

---

# Difficultés rencontrées

Les premiers tests avec le modèle utilisé montrent que le **tool calling peut être imprécis lorsque certaines informations sont manquantes**, notamment avec un modèle de petite taille.

Le modèle peut dans certains cas tenter d'appeler un outil avant d'avoir obtenu tous les paramètres nécessaires.

Une validation supplémentaire des paramètres côté application sera donc nécessaire afin de garantir que les APIs ne soient appelées qu'avec des données valides.

---

# Travaux prévus pour la semaine suivante

Les prochains travaux porteront principalement sur :

* ajout de la validation des paramètres des tools ;
* tests de l'API d'édition de devis ;
* gestion des scénarios combinant RAG et APIs ;
* amélioration de la gestion des erreurs et de la fiabilité du tool calling ;
* poursuite de l'intégration des APIs réelles dès que leur accès sera disponible ;
* préparation progressive des aspects frontend et sécurité.
