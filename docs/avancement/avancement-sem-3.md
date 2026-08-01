# Point d'avancement – Semaine 3

**Projet :** Assistant IA basé sur un système RAG pour ATLANTASANAD Assurance
**Période :** Semaine 3

---

# Objectif de la semaine

L'objectif principal de cette semaine était de corriger les principales limitations identifiées lors de la première version du système RAG. Les travaux se sont concentrés sur l'amélioration du pipeline de retrieval, l'enrichissement du contexte transmis au LLM ainsi que sur l'amélioration du parsing des documents afin d'obtenir une première version plus robuste du système.

---

# Travaux réalisés

## 1. Finalisation d'une première version complète du pipeline RAG

Une première version fonctionnelle de la chaîne RAG a été finalisée.

Le pipeline comprend désormais les étapes suivantes :

1. ingestion des documents ;
2. génération des métadonnées ;
3. découpage en chunks ;
4. génération des embeddings ;
5. stockage vectoriel dans Qdrant ;
6. embedding des requêtes utilisateurs ;
7. recherche vectorielle ;
8. reranking des résultats ;
9. récupération des chunks voisins (*Neighbor Retrieval*) ;
10. construction du contexte ;
11. génération de la réponse via un LLM.

Chaque composant reste indépendant afin de faciliter les évolutions futures et le remplacement éventuel de certaines briques techniques.

---

## 2. Amélioration du pipeline de retrieval

Plusieurs améliorations ont été apportées à la phase de recherche documentaire afin d'améliorer la qualité du contexte fourni au modèle de génération.

Les principales évolutions sont :

* amélioration de la représentation du texte utilisé pour les embeddings ;
* mise en place d'un pipeline de retrieval modulaire ;
* intégration d'une étape de reranking des résultats ;
* implémentation d'un mécanisme de **Neighbor Retrieval** permettant de récupérer automatiquement les chunks adjacents afin de restituer davantage de contexte autour des passages retrouvés ;
* amélioration de la construction du contexte envoyé au LLM.

Ces améliorations permettent de limiter les pertes d'information provoquées par le découpage des documents en plusieurs chunks.

---

## 3. Révision du pipeline d'ingestion

Le pipeline d'ingestion a été revu afin d'améliorer la qualité des données indexées.

Les principales modifications concernent :

* simplification de la structure interne des sections ;
* révision des prompts utilisés pour la génération des métadonnées ;
* génération des résumés, titres et mots-clés exclusivement en français ;
* enrichissement du contenu utilisé pour la génération des embeddings.

---

## 4. Analyse approfondie du parsing

Une phase importante de cette semaine a été consacrée à l'analyse de la qualité du parsing.

Les documents générés ont été comparés manuellement avec les PDF d'origine afin d'identifier précisément les erreurs de structure pouvant dégrader les performances du système RAG.

Plusieurs approches et configurations ont été testées afin d'améliorer cette étape.

---

## 5. Évaluation de différentes approches de parsing

Différentes pistes ont été explorées afin de résoudre les problèmes observés :

* ajustement des paramètres de Docling ;
* amélioration du nettoyage des documents ;
* modification des stratégies de structuration ;
* essais avec d'autres approches d'extraction documentaire.

Ces expérimentations ont permis d'améliorer certains aspects de l'extraction, mais plusieurs limitations importantes semblent provenir directement de la structure des documents PDF.

---

# Résultats obtenus

Les principaux résultats obtenus sont les suivants :

* première version complète du pipeline RAG opérationnelle ;
* génération de réponses basée sur le contexte récupéré ;
* pipeline de retrieval enrichi avec le reranking et le Neighbor Retrieval ;
* amélioration de la qualité des embeddings grâce à un texte d'indexation enrichi ;
* amélioration des métadonnées générées pour les sections et les chunks ;
* correction de la majorité des problèmes liés aux caractères accentués ;
* amélioration de l'extraction des tableaux simples.

Cette version permet désormais de réaliser des tests complets sur l'ensemble de la chaîne RAG.

---

# Difficultés rencontrées

Les analyses réalisées cette semaine montrent que plusieurs limitations subsistent malgré les nombreuses expérimentations effectuées.

Les principales difficultés sont :

* certains caractères accentués restent mal extraits dans quelques parties spécifiques des documents, probablement en raison de l'encodage ou des polices utilisées dans les PDF ;
* l'ordre de lecture des documents comportant plusieurs colonnes n'est pas correctement reconstruit ;
* les tableaux contenant des cellules fusionnées ou des structures complexes ne sont pas entièrement restitués.

Après avoir testé différentes configurations et plusieurs approches de parsing, ces limitations semblent davantage liées aux capacités actuelles des outils de parsing qu'à l'architecture du pipeline développée.

Je poursuis néanmoins la recherche d'autres solutions permettant d'améliorer cette étape, celle-ci ayant un impact direct sur la qualité de la recherche documentaire et des réponses générées.

Si vous avez déjà rencontré ce type de problématique ou si vous connaissez des outils ou des approches adaptés à ce type de documents, je serais très intéressé par vos recommandations.

À défaut, une autre piste envisagée serait d'utiliser des modèles de compréhension documentaire plus performants afin de limiter l'impact de ces erreurs lors de l'interprétation des documents. Malheureusement, les ressources matérielles actuellement disponibles ne permettent pas de tester ce type de modèles dans de bonnes conditions.

---

# Travaux prévus pour la semaine suivante

Compte tenu des nombreuses expérimentations déjà réalisées sur le parsing et des limites qui semblent principalement liées aux documents eux-mêmes, je souhaite désormais concentrer la suite du projet sur la seconde partie prévue : l'intégration des API métiers.

Les travaux prévus sont les suivants :

* conception de l'architecture d'intégration des API dans le système ;
* développement du pipeline d'interrogation des API pour les données dynamiques ;
* mise en place du mécanisme permettant de combiner les informations issues du RAG et des API au sein d'un même assistant ;
* réalisation des premiers tests de fonctionnement de cette nouvelle architecture.

Parallèlement, je continuerai à effectuer une veille sur les solutions de parsing documentaire afin d'évaluer, si possible, des modèles plus performants lorsque les ressources matérielles le permettront.
