# Résultats des tests – Agent RAG & API

## 1. Test RAG

### Conversation

**Utilisateur**

> Quelles sont les pièces à fournir en cas de sinistre ?

**Assistant**

> En cas de sinistre, il est généralement nécessaire de fournir les pièces suivantes :
>
> * Un constat à l'amiable ou un PV
> * Une copie de la carte grise du véhicule
> * Une copie de la police d'assurance
> * En cas de blessures, des certificats médicaux peuvent être nécessaires.
> * En cas de panne mécanique garantie par le contrat, un diagnostic précis de la panne ou de l'incident peut être demandé.
>
> Il est également nécessaire de transmettre à l'assureur les documents relatifs au sinistre et d'indiquer les informations permettant de l'identifier.

### Validation technique du workflow

**Tool sélectionné**

```text
rag
```

**Question transmise au RAG**

```text
quelles sont les pièces à fournir en cas de sinistre
```

### Retriever

|  Score | Document                                           | Page |
| -----: | -------------------------------------------------- | ---: |
| 0.6706 | Véhicule_pro.pdf                                   |    3 |
| 0.6953 | Auto+_véhicules_utilitaires.pdf                    |    4 |
| 0.6740 | Auto+_véhicules_utilitaires.pdf                    |    5 |
| 0.6285 | Notice d'Information Multirisque auto+ 02 2024.pdf |    3 |
| 0.6130 | Notice d'Information Multirisque auto+ 02 2024.pdf |    3 |

### Reranker

|  Score | Document                                           | Page |
| -----: | -------------------------------------------------- | ---: |
| 0.9928 | Véhicule_pro.pdf                                   |    3 |
| 0.9860 | Auto+_véhicules_utilitaires.pdf                    |    4 |
| 0.9741 | Auto+_véhicules_utilitaires.pdf                    |    5 |
| 0.7649 | Notice d'Information Multirisque auto+ 02 2024.pdf |    3 |
| 0.5027 | Notice d'Information Multirisque auto+ 02 2024.pdf |    3 |

**Résultat :** le RAG a correctement sélectionné les documents les plus pertinents et le reranker a amélioré leur classement avant la génération de la réponse.

---

# 2. Test Simulation API

### Conversation

**Utilisateur**

> Je souhaite une simulation d'assurance auto.

**Assistant**

> Pour effectuer une simulation d'assurance auto, nous avons besoin de certaines informations supplémentaires. Pourriez-vous me donner votre nom, prénom, catégorie professionnelle, code du pack, numéro de téléphone, type de motorisation, puissance fiscale, valeur à neuf, valeur vénale ainsi que les coordonnées GPS ?

**Utilisateur**

> Voici les informations demandées : Nom : BENALI, Prénom : Ahmed, Catégorie professionnelle : AU, Code pack : PTR, Téléphone : 0662149815, Type de motorisation : Diesel, Puissance fiscale : 8, Valeur à neuf : 500000 MAD, Valeur vénale : 300000 MAD, Longitude GPS : -7.493215, Latitude GPS : 33.613599.

**Assistant**

> Votre simulation d'assurance auto a été créée avec succès. Vous avez reçu le numéro de devis 38823427. La prime mensuelle est de 618,38 MAD.

### Validation technique du workflow

**Premier appel**

```text
Tool sélectionné : simulation
Paramètres : informations manquantes
Action : l'agent demande les informations nécessaires
```

**Deuxième appel**

```json
{
  "nom_clie": "BENALI",
  "prenclie": "Ahmed",
  "cateprof": "AU",
  "codepack": "PTR",
  "telemobi": "0662149815",
  "typemote": "Diesel",
  "puisvehi": 8,
  "valeneuf": 500000,
  "valevena": 300000,
  "long_gps": -7.493215,
  "lati_gps": 33.613599
}
```

**Réponse du Mock API**

```json
{
  "success": true,
  "simulation_id": "SIM-20260806-0001",
  "quote_number": "38823427",
  "product": "Auto+ Particulier",
  "premium": {
    "annual": 7420.50,
    "monthly": 618.38,
    "currency": "MAD"
  },
  "status": "SIMULATION_CREATED"
}
```

**Résultat :** l'agent conserve le contexte conversationnel, collecte les informations nécessaires, appelle le tool de simulation et génère une réponse à partir du résultat de l'API.

