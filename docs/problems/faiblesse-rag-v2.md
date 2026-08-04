Voici la liste consolidée des faiblesses identifiées jusqu'ici, organisées par couche du pipeline — c'est important de les séparer, parce que la solution n'est pas la même selon la couche responsable.

## 1. Faiblesse sur les tableaux (ta remarque)

C'est confirmé, mais avec deux causes différentes selon le tableau :

- **Tableaux simples, bien extraits** (vétusté carrosserie/pièces d'usure) → le RAG répond correctement (Q6 : 10%). Donc le RAG *peut* lire un tableau markdown quand il est propre.
- **Tableaux à cellules fusionnées/en-têtes multi-niveaux** (Valeur Vénale, barème incapacités) → une ligne entière manque à l'extraction (Q7 échoue, "pas d'info", ce qui est honnête mais révèle une vraie perte de donnée en amont).
- **Hypothèse à vérifier** : même quand un tableau est bien extrait, le format markdown en pipes se prête mal à l'embedding sémantique — une question en langage naturel ("quel taux à l'année 3") matche moins bien avec une ligne de tableau brute qu'avec une phrase de prose. À tester : le retrieval remonte-t-il le bon tableau de façon fiable sur des reformulations différentes de la question, ou seulement sur des questions qui reprennent le vocabulaire exact des en-têtes ?

## 2. Perte silencieuse de données à l'extraction

- Ligne manquante dans le tableau Valeur Vénale (VH Location, PF>12CV, Diesel/Essence année 1).
- Table of Contents (Sommaire) entièrement absent du parsing.
- Aucune alerte automatique ne signale ces trous — on ne les a découverts qu'en comparant manuellement au PDF.

## 3. Ordre de lecture cassé sur les pages multi-colonnes

Jamais corrigé (contrairement aux accents). Des blocs mélangent plusieurs articles différents dans une seule unité de texte (ex. Article 22 + Article 20 + Article 18 fusionnés dans un même bloc). Impact direct : le contexte donné au LLM peut être syntaxiquement incohérent, même si — on l'a vu sur Q5 — un modèle assez robuste peut parfois extraire la bonne info malgré ce bruit. Ce n'est pas fiable à 100%.

## 4. Numérotation d'articles dupliquée, non désambiguïsée

Le document a deux "Article 23" différents (Protection des Passagers dans le corps ; Prescription dans l'Annexe I RC). Le RAG n'a aucune logique pour détecter/signaler ce cas — il répond soit au hasard, soit "pas d'info" (Q8). Ni le retrieval ni le prompt système ne gèrent la désambiguïsation par section/annexe.

## 5. Chunking mal aligné sur les unités logiques

- Des chunks header-only sans corps (`"V. PRIMES"`, `"Article 16"`, `"C."`) — quasi inutiles en l'état pour la génération si ils sont recupérés seuls.
- D'autres chunks fourre-tout regroupant plusieurs articles sans frontière claire.
- → c'est exactement ce qui justifie le neighbor retrieval qu'on vient de discuter, mais ça ne couvre qu'une partie du problème (le chunk voisin peut lui aussi être mal aligné).

## 6. Échecs silencieux du pipeline (le plus préoccupant, pas encore diagnostiqué)

Réponses `{}` complètement vides sur Q1 et Q9 (avec régression sur Q9 par rapport à avant). Ce n'est pas un "je ne sais pas" propre — c'est un signe de bug d'ingénierie (retrieval qui renvoie rien, ou parsing JSON de la sortie LLM qui plante et catch une exception silencieusement). Tant que ce n'est pas débogué, on ne sait même pas si c'est un problème de données ou un bug de code pur.

## 7. Formatage de sortie incohérent

Chaque réponse a une structure JSON différente selon la question (`{"réponse": ...}`, `{"error_code": 0, "result": 10}`, `{"garantie DTA": "", ...}`, `{}`). Ça complique l'évaluation automatique et signale que le prompt système ne force pas un schéma de sortie stable — un souci d'ingénierie indépendant de la qualité du contenu.

## 8. Dépendance à la formulation exacte de la question

Pas encore testé explicitement, mais suspecté : vu les problèmes de chunking/embedding sur les tableaux et le vocabulaire juridique très spécifique du document, il est probable que reformuler légèrement une question fasse basculer une bonne réponse vers un échec. Vaudrait le coup d'ajouter des variantes de formulation à ta liste de test pour vérifier la robustesse.

---

**Pour prioriser** : le point 6 (échecs silencieux) est le plus urgent à traiter — tant qu'on ne sait pas *pourquoi* Q1/Q9 renvoient du vide, on navigue à l'aveugle sur tout le reste. Ensuite, le point 1/2 (tableaux à cellules fusionnées) est le plus structurel côté qualité de donnée. Veux-tu qu'on commence par écrire un script de debug qui logue le contexte récupéré + la réponse brute du LLM avant parsing, pour Q1 et Q9 précisément ?