# Point d'avancement – Semaine 2

**Projet :** Assistant IA basé sur un système RAG pour ATLANTASANAD Assurance
**Période :** Semaine 2

---

# Objectif de la semaine

L'objectif principal de ces deux semaines était de concevoir les fondations du pipeline d'ingestion des documents afin de construire une base documentaire exploitable par un système RAG. L'accent a été mis sur la mise en place d'une architecture modulaire permettant de séparer clairement les différentes étapes du traitement.

---

# Travaux réalisés

## 1. Définition de l'architecture globale

Une première architecture du projet a été définie afin de séparer les différentes responsabilités du système :

* ingestion des documents ;
* génération des métadonnées ;
* découpage des documents ;
* génération des embeddings ;
* stockage vectoriel ;
* recherche (retrieval) ;
* génération des réponses.

Chaque étape est implémentée sous forme de pipeline indépendant afin de faciliter les évolutions futures.

---

## 2. Pipeline d'ingestion

Le pipeline d'ingestion a été entièrement mis en place.

Les étapes actuellement réalisées sont les suivantes :

1. Parsing du document PDF ;
2. Nettoyage du document ;
3. Extraction de la structure hiérarchique (sections) ;
4. Génération de métadonnées sémantiques pour les sections ;
5. Découpage des sections en chunks ;
6. Génération de métadonnées sémantiques pour chaque chunk ;
7. Génération des embeddings ;
8. Stockage des vecteurs dans Qdrant.

---

## 3. Parsing des documents

Un adaptateur basé sur Docling a été intégré afin d'extraire automatiquement :

* les sections ;
* les titres ;
* les listes ;
* les tableaux ;
* le contenu textuel.

Une représentation interne du document a ensuite été définie sous forme de modèles Python (`Document`, `Section`, `Chunk`, etc.).

---

## 4. Génération des métadonnées

Un enrichissement sémantique est effectué à deux niveaux :

### Métadonnées de section

Pour chaque section :

* résumé ;
* mots-clés.

### Métadonnées de chunk

Pour chaque chunk :

* résumé ;
* mots-clés.

Cette étape est réalisée à l'aide d'un LLM local (Qwen2.5 via Ollama).

---

## 5. Chunking

Un découpage récursif (Recursive Chunking) a été implémenté afin de produire des chunks adaptés à la recherche vectorielle.

Les paramètres de chunking (taille, overlap et séparateurs) sont entièrement configurables.

---

## 6. Génération des embeddings

Les embeddings sont générés avec le modèle :

* **BAAI/bge-m3**

L'implémentation est volontairement indépendante afin que le même composant puisse être réutilisé ultérieurement pour l'embedding des requêtes utilisateurs.

---

## 7. Stockage vectoriel

Qdrant a été intégré comme base de données vectorielle.

Les travaux réalisés comprennent :

* création automatique de la collection ;
* conversion des chunks en points Qdrant ;
* génération du payload ;
* insertion des embeddings.

Le payload stocké contient notamment :

* texte du chunk ;
* identifiants du document ;
* numéro de page ;
* titre de section ;
* résumés ;
* mots-clés ;
* informations d'indexation.

---

## 8. Début du pipeline de recherche

Une première version du pipeline de recherche a été développée.

Elle comprend :

* embedding de la requête utilisateur ;
* recherche vectorielle dans Qdrant ;
* reranking des résultats ;
* construction du contexte envoyé au LLM.

Cette architecture est indépendante du pipeline d'ingestion afin de pouvoir faire évoluer les deux parties séparément.

---

# Résultats obtenus

Les principaux résultats obtenus sont :

* pipeline d'ingestion entièrement fonctionnel ;
* génération automatique des embeddings ;
* stockage des documents dans Qdrant ;
* recherche vectorielle opérationnelle ;
* premiers tests de récupération de contexte réalisés avec succès.

L'ensemble constitue une première chaîne complète allant du document PDF jusqu'à la récupération des passages les plus pertinents.

---

# Difficultés rencontrées

Plusieurs difficultés techniques ont été rencontrées au cours de cette première phase :

* temps de traitement important lors de la génération des métadonnées avec le LLM local ;
* incompatibilités entre certaines versions du client et du serveur Qdrant ;
* sérialisation et désérialisation des objets métier (JSON ↔ dataclasses) ;
* gestion des identifiants lors de l'insertion dans Qdrant (UUID requis) ;
* ajustement des modèles de données afin de conserver une architecture propre.

Les différents problèmes ont été progressivement corrigés au cours de l'implémentation.

---

# Analyse préliminaire

Les premiers essais mettent également en évidence plusieurs limites du pipeline actuel :

* le parsing de certains PDF dégrade parfois la structure logique du document ;
* certaines phrases sont découpées de manière excessive ;
* le contenu des chunks perd parfois une partie de son contexte ;
* les résumés générés par le LLM sont parfois produits en anglais alors que les documents sont en français.

Ces observations serviront de base aux prochaines améliorations.

---

# Travaux prévus pour la semaine suivante

Les prochains travaux porteront principalement sur l'amélioration de la qualité du système RAG :

* amélioration du parsing des documents ;
* amélioration de la stratégie de chunking afin de conserver davantage de contexte ;
* enrichissement du texte indexé avec les informations de section ;
* amélioration des prompts utilisés pour la génération des métadonnées ;
* évaluation qualitative de la recherche vectorielle ;
* amélioration du reranking ;
* implémentation complète de la génération de réponses basée sur le contexte récupéré ;
* début de la phase d'évaluation du système.
