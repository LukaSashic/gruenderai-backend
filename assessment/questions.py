"""
Question Bank for Gründungszuschuss Assessment
Based on research and key rejection reasons
"""

# Assessment dimensions (from Howard et al. and rejection analysis)
DIMENSIONS = [
    "Unternehmerische Persönlichkeit",  # Entrepreneurial personality
    "Fachkompetenz",                    # Professional competence
    "Marktverständnis",                 # Market understanding
    "Finanzplanung",                    # Financial planning
    "Umsetzungsreife"                   # Implementation readiness
]

def get_question_bank():
    """
    Returns the complete question bank for assessment
    15 questions covering 5 dimensions
    """
    
    questions = [
        # ===== Unternehmerische Persönlichkeit (3 questions) =====
        {
            "id": "ENT_001",
            "dimension": "Unternehmerische Persönlichkeit",
            "type": "likert",
            "text": "Ich bin bereit, kalkulierte Risiken einzugehen, um meine Geschäftsziele zu erreichen.",
            "options": [
                {"value": 1, "label": "Stimme gar nicht zu"},
                {"value": 2, "label": "Stimme eher nicht zu"},
                {"value": 3, "label": "Neutral"},
                {"value": 4, "label": "Stimme eher zu"},
                {"value": 5, "label": "Stimme voll zu"}
            ]
        },
        {
            "id": "ENT_002",
            "dimension": "Unternehmerische Persönlichkeit",
            "type": "likert",
            "text": "Ich ergreife proaktiv Initiativen und warte nicht darauf, dass andere mir sagen, was zu tun ist.",
            "options": [
                {"value": 1, "label": "Stimme gar nicht zu"},
                {"value": 2, "label": "Stimme eher nicht zu"},
                {"value": 3, "label": "Neutral"},
                {"value": 4, "label": "Stimme eher zu"},
                {"value": 5, "label": "Stimme voll zu"}
            ]
        },
        {
            "id": "ENT_003",
            "dimension": "Unternehmerische Persönlichkeit",
            "type": "likert",
            "text": "Ich kann gut mit Unsicherheit umgehen und bleibe auch bei Rückschlägen motiviert.",
            "options": [
                {"value": 1, "label": "Stimme gar nicht zu"},
                {"value": 2, "label": "Stimme eher nicht zu"},
                {"value": 3, "label": "Neutral"},
                {"value": 4, "label": "Stimme eher zu"},
                {"value": 5, "label": "Stimme voll zu"}
            ]
        },
        
        # ===== Fachkompetenz (3 questions) =====
        {
            "id": "COMP_001",
            "dimension": "Fachkompetenz",
            "type": "multiple_choice",
            "text": "Wie lange haben Sie bereits Erfahrung in der Branche Ihrer geplanten Selbstständigkeit?",
            "options": [
                {"value": "no_experience", "label": "Keine Erfahrung"},
                {"value": "less_1_year", "label": "Weniger als 1 Jahr"},
                {"value": "1_3_years", "label": "1-3 Jahre"},
                {"value": "3_5_years", "label": "3-5 Jahre"},
                {"value": "more_5_years", "label": "Mehr als 5 Jahre"}
            ],
            "scoring": {
                "no_experience": 1,
                "less_1_year": 2,
                "1_3_years": 3,
                "3_5_years": 4,
                "more_5_years": 5
            }
        },
        {
            "id": "COMP_002",
            "dimension": "Fachkompetenz",
            "type": "yes_no",
            "text": "Haben Sie eine formale Ausbildung oder Qualifikation, die für Ihre Gründung relevant ist?",
            "options": [
                {"value": "yes", "label": "Ja"},
                {"value": "no", "label": "Nein"}
            ],
            "scoring": {"yes": 5, "no": 1}
        },
        {
            "id": "COMP_003",
            "dimension": "Fachkompetenz",
            "type": "likert",
            "text": "Ich verfüge über alle notwendigen fachlichen Fähigkeiten, um mein Geschäft erfolgreich zu führen.",
            "options": [
                {"value": 1, "label": "Stimme gar nicht zu"},
                {"value": 2, "label": "Stimme eher nicht zu"},
                {"value": 3, "label": "Neutral"},
                {"value": 4, "label": "Stimme eher zu"},
                {"value": 5, "label": "Stimme voll zu"}
            ]
        },
        
        # ===== Marktverständnis (3 questions) =====
        {
            "id": "MARKET_001",
            "dimension": "Marktverständnis",
            "type": "yes_no",
            "text": "Haben Sie eine detaillierte Zielgruppenanalyse durchgeführt und wissen genau, wer Ihre Kunden sein werden?",
            "options": [
                {"value": "yes", "label": "Ja, detailliert"},
                {"value": "partial", "label": "Teilweise"},
                {"value": "no", "label": "Nein, noch nicht"}
            ],
            "scoring": {"yes": 5, "partial": 3, "no": 1}
        },
        {
            "id": "MARKET_002",
            "dimension": "Marktverständnis",
            "type": "yes_no",
            "text": "Kennen Sie Ihre direkten Wettbewerber und können Sie klar beschreiben, was Ihr Angebot von ihnen unterscheidet?",
            "options": [
                {"value": "yes", "label": "Ja, genau"},
                {"value": "partial", "label": "Teilweise"},
                {"value": "no", "label": "Nein"}
            ],
            "scoring": {"yes": 5, "partial": 3, "no": 1}
        },
        {
            "id": "MARKET_003",
            "dimension": "Marktverständnis",
            "type": "likert",
            "text": "Ich habe bereits potenzielle Kunden befragt oder Interesse an meinem Angebot validiert.",
            "options": [
                {"value": 1, "label": "Stimme gar nicht zu"},
                {"value": 2, "label": "Stimme eher nicht zu"},
                {"value": 3, "label": "Neutral"},
                {"value": 4, "label": "Stimme eher zu"},
                {"value": 5, "label": "Stimme voll zu"}
            ]
        },
        
        # ===== Finanzplanung (3 questions) =====
        {
            "id": "FIN_001",
            "dimension": "Finanzplanung",
            "type": "yes_no",
            "text": "Haben Sie eine detaillierte Finanzplanung für mindestens die ersten 3 Jahre erstellt?",
            "options": [
                {"value": "yes", "label": "Ja, vollständig"},
                {"value": "partial", "label": "Teilweise"},
                {"value": "no", "label": "Nein"}
            ],
            "scoring": {"yes": 5, "partial": 3, "no": 1}
        },
        {
            "id": "FIN_002",
            "dimension": "Finanzplanung",
            "type": "multiple_choice",
            "text": "Wie hoch ist Ihr geschätzter Kapitalbedarf für die Gründung?",
            "options": [
                {"value": "unclear", "label": "Noch unklar"},
                {"value": "under_10k", "label": "Unter 10.000€"},
                {"value": "10_30k", "label": "10.000€ - 30.000€"},
                {"value": "30_50k", "label": "30.000€ - 50.000€"},
                {"value": "over_50k", "label": "Über 50.000€"}
            ],
            "scoring": {
                "unclear": 1,
                "under_10k": 4,
                "10_30k": 5,
                "30_50k": 4,
                "over_50k": 3
            }
        },
        {
            "id": "FIN_003",
            "dimension": "Finanzplanung",
            "type": "likert",
            "text": "Ich habe realistische Umsatzprognosen erstellt, die auf Marktdaten basieren.",
            "options": [
                {"value": 1, "label": "Stimme gar nicht zu"},
                {"value": 2, "label": "Stimme eher nicht zu"},
                {"value": 3, "label": "Neutral"},
                {"value": 4, "label": "Stimme eher zu"},
                {"value": 5, "label": "Stimme voll zu"}
            ]
        },
        
        # ===== Umsetzungsreife (3 questions) =====
        {
            "id": "IMPL_001",
            "dimension": "Umsetzungsreife",
            "type": "multiple_choice",
            "text": "In welchem Stadium befindet sich Ihre Gründungsvorbereitung?",
            "options": [
                {"value": "idea", "label": "Frühe Ideenphase"},
                {"value": "concept", "label": "Konzeptentwicklung"},
                {"value": "planning", "label": "Detailplanung"},
                {"value": "ready", "label": "Startbereit"}
            ],
            "scoring": {
                "idea": 2,
                "concept": 3,
                "planning": 4,
                "ready": 5
            }
        },
        {
            "id": "IMPL_002",
            "dimension": "Umsetzungsreife",
            "type": "yes_no",
            "text": "Haben Sie bereits konkrete Schritte unternommen (z.B. Gewerbe angemeldet, Website erstellt, Kunden kontaktiert)?",
            "options": [
                {"value": "yes", "label": "Ja, mehrere"},
                {"value": "some", "label": "Einige"},
                {"value": "no", "label": "Noch keine"}
            ],
            "scoring": {"yes": 5, "some": 3, "no": 1}
        },
        {
            "id": "IMPL_003",
            "dimension": "Umsetzungsreife",
            "type": "likert",
            "text": "Ich könnte innerhalb der nächsten 4 Wochen mit meiner selbstständigen Tätigkeit starten.",
            "options": [
                {"value": 1, "label": "Stimme gar nicht zu"},
                {"value": 2, "label": "Stimme eher nicht zu"},
                {"value": 3, "label": "Neutral"},
                {"value": 4, "label": "Stimme eher zu"},
                {"value": 5, "label": "Stimme voll zu"}
            ]
        }
    ]
    
    return questions
