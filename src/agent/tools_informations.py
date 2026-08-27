TOOLS_INFORMATIONS = {
    "simulation": {
        "name": "simulation",
        "description": ("""
        À utiliser pour effectuer des calculs de tarification, estimer des coûts ou simuler des garanties en fonction de paramètres saisis (type de couverture, profil, options). Cet outil exécute des règles de calcul et retourne une estimation financière.
        """),
    },

    "recuperation_devis": {
        "name": "recuperation_devis",
        "description": (
            "Récupère ou télécharger un devis existant. Utilise cet outil lorsqu'un utilisateur souhaite "
            "consulter, récupérer, télécharger ou obtenir son devis existant. "
            "L'identifiant du devis ou de la police est obligatoire. "
        ),
    },

    "rag": {
        "name": "rag",
        "description": ("""
        Outil obligatoire pour TOUTE question liée à l'assurance (garanties, avantages, produits, conditions, tarifs, primes, contrats, franchises, sinistres, indemnisation, souscription, couvertures, documents, packs, offres). À appeler IMMÉDIATEMENT dès qu'un sujet d'assurance est abordé, y compris pour les demandes vagues, générales ou incomplètes, sans demander de clarification préalable et sans nécessiter d'informations obligatoires. Ne PAS utiliser uniquement en cas de simple salutation, de demande de simulation (utiliser simulation_tool), de recherche de devis existant (utiliser recuperation_devis_tool) ou de sujet hors assurance.
        """
        )
    }
}