"""
Assessment Engine
Core logic for adaptive assessment using simplified IRT principles
"""

import random
from typing import Dict, List, Any, Optional
from .questions import get_question_bank, DIMENSIONS

class AssessmentEngine:
    """
    Sophisticated assessment engine for Gründungszuschuss readiness
    Based on research from Howard et al. and IRT principles
    """
    
    def __init__(self):
        self.question_bank = get_question_bank()
        self.total_questions = len(self.question_bank)
        self.dimensions = DIMENSIONS
        
    def get_next_question(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get the next question based on current progress
        For MVP: Sequential questions
        For future: Adaptive selection based on IRT
        """
        current_index = session_data["current_question_index"]
        
        if current_index >= self.total_questions:
            return None
            
        question = self.question_bank[current_index]
        
        return {
            "question_id": question["id"],
            "question_text": question["text"],
            "question_type": question["type"],
            "options": question.get("options", []),
            "dimension": question["dimension"],
            "order": current_index + 1,
            "total": self.total_questions
        }
    
    def calculate_results(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate comprehensive assessment results
        """
        answers = session_data["answers"]
        
        # Initialize dimension scores
        dimension_scores = {dim: {"raw_score": 0, "count": 0} for dim in self.dimensions}
        
        # Calculate scores per dimension
        for question in self.question_bank:
            question_id = question["id"]
            
            if question_id in answers:
                answer_data = answers[question_id]
                dimension = question["dimension"]
                
                # Score the answer
                score = self._score_answer(question, answer_data["answer"])
                
                dimension_scores[dimension]["raw_score"] += score
                dimension_scores[dimension]["count"] += 1
        
        # Calculate normalized scores (0-100)
        normalized_dimensions = {}
        for dim, data in dimension_scores.items():
            if data["count"] > 0:
                avg_score = data["raw_score"] / data["count"]
                normalized_dimensions[dim] = {
                    "score": round(avg_score * 20, 1),  # Convert 0-5 to 0-100
                    "level": self._get_level(avg_score),
                    "interpretation": self._get_interpretation(dim, avg_score)
                }
        
        # Calculate overall score (weighted average)
        overall_score = self._calculate_overall_score(normalized_dimensions)
        readiness_level = self._get_readiness_level(overall_score)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(normalized_dimensions, overall_score)
        next_steps = self._generate_next_steps(readiness_level, normalized_dimensions)
        
        return {
            "overall_score": overall_score,
            "readiness_level": readiness_level,
            "dimensions": normalized_dimensions,
            "recommendations": recommendations,
            "next_steps": next_steps
        }
    
    def _score_answer(self, question: Dict, answer: Any) -> float:
        """
        Score a single answer
        Returns 0-5 scale
        """
        question_type = question["type"]
        
        if question_type == "likert":
            # Likert scale 1-5
            return float(answer)
            
        elif question_type == "multiple_choice":
            # Check scoring key
            scoring = question.get("scoring", {})
            return scoring.get(str(answer), 0)
            
        elif question_type == "yes_no":
            # Simple binary
            scoring = question.get("scoring", {"yes": 5, "no": 0})
            return scoring.get(answer.lower(), 0)
            
        elif question_type == "text":
            # Text answers score based on presence (3 = answered)
            return 3.0 if len(str(answer).strip()) > 0 else 0
            
        return 0
    
    def _get_level(self, score: float) -> str:
        """Convert numeric score to level"""
        if score >= 4.0:
            return "Hoch"
        elif score >= 2.5:
            return "Mittel"
        else:
            return "Niedrig"
    
    def _get_interpretation(self, dimension: str, score: float) -> str:
        """Get interpretation text for dimension score"""
        level = self._get_level(score)
        
        interpretations = {
            "Unternehmerische Persönlichkeit": {
                "Hoch": "Sie zeigen ausgeprägte unternehmerische Eigenschaften wie Risikobereitschaft und Proaktivität.",
                "Mittel": "Ihre unternehmerischen Eigenschaften sind gut entwickelt, können aber noch gestärkt werden.",
                "Niedrig": "Es empfiehlt sich, an unternehmerischen Kompetenzen zu arbeiten."
            },
            "Fachkompetenz": {
                "Hoch": "Sie verfügen über starke fachliche Qualifikationen für Ihre Gründung.",
                "Mittel": "Ihre fachlichen Kompetenzen sind solide, spezifische Weiterbildung könnte hilfreich sein.",
                "Niedrig": "Fachliche Weiterbildung wird empfohlen, um Ihre Erfolgschancen zu erhöhen."
            },
            "Marktverständnis": {
                "Hoch": "Sie haben ein klares Verständnis Ihres Zielmarktes und Ihrer Kunden.",
                "Mittel": "Ihr Marktverständnis ist vorhanden, vertiefte Marktforschung wäre vorteilhaft.",
                "Niedrig": "Intensivere Auseinandersetzung mit dem Markt ist wichtig für Ihren Erfolg."
            },
            "Finanzplanung": {
                "Hoch": "Ihre Finanzplanung ist durchdacht und realistisch.",
                "Mittel": "Grundlegende Finanzplanung vorhanden, Details sollten verfeinert werden.",
                "Niedrig": "Professionelle Unterstützung bei der Finanzplanung wird dringend empfohlen."
            },
            "Umsetzungsreife": {
                "Hoch": "Sie sind gut vorbereitet und können mit der Umsetzung beginnen.",
                "Mittel": "Einige Vorbereitungen sind noch zu treffen, bevor Sie starten können.",
                "Niedrig": "Erhebliche Vorarbeit ist noch erforderlich für einen erfolgreichen Start."
            }
        }
        
        return interpretations.get(dimension, {}).get(level, "")
    
    def _calculate_overall_score(self, dimensions: Dict) -> float:
        """Calculate weighted overall score"""
        # Weights based on importance for Gründungszuschuss approval
        weights = {
            "Unternehmerische Persönlichkeit": 0.20,
            "Fachkompetenz": 0.25,
            "Marktverständnis": 0.25,
            "Finanzplanung": 0.20,
            "Umsetzungsreife": 0.10
        }
        
        weighted_sum = 0
        total_weight = 0
        
        for dim, data in dimensions.items():
            if dim in weights:
                weighted_sum += data["score"] * weights[dim]
                total_weight += weights[dim]
        
        return round(weighted_sum / total_weight if total_weight > 0 else 0, 1)
    
    def _get_readiness_level(self, overall_score: float) -> str:
        """Determine overall readiness level"""
        if overall_score >= 75:
            return "Hoch - Sehr gute Bewilligungschancen"
        elif overall_score >= 55:
            return "Mittel - Gute Chancen mit Optimierungen"
        elif overall_score >= 35:
            return "Ausbaufähig - Verbesserungen erforderlich"
        else:
            return "Niedrig - Erhebliche Vorbereitung notwendig"
    
    def _generate_recommendations(self, dimensions: Dict, overall_score: float) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Find weak areas
        weak_dimensions = [
            dim for dim, data in dimensions.items() 
            if data["score"] < 60
        ]
        
        if overall_score >= 75:
            recommendations.append("Ihre Vorbereitung ist ausgezeichnet. Fokussieren Sie jetzt auf die formale Antragstellung.")
        
        if "Finanzplanung" in weak_dimensions:
            recommendations.append("Erstellen Sie eine detaillierte 3-Jahres-Finanzplanung mit realistischen Annahmen.")
        
        if "Marktverständnis" in weak_dimensions:
            recommendations.append("Führen Sie eine gründliche Markt- und Wettbewerbsanalyse durch.")
        
        if "Fachkompetenz" in weak_dimensions:
            recommendations.append("Dokumentieren Sie Ihre fachlichen Qualifikationen und Branchenerfahrung detailliert.")
        
        if "Umsetzungsreife" in weak_dimensions:
            recommendations.append("Entwickeln Sie einen konkreten Zeitplan für Ihre ersten 6 Monate.")
        
        # Always add general recommendation
        recommendations.append("Nutzen Sie die Gründungszuschuss-Beratung Ihrer Agentur für Arbeit.")
        
        return recommendations[:5]  # Max 5 recommendations
    
    def _generate_next_steps(self, readiness_level: str, dimensions: Dict) -> List[str]:
        """Generate actionable next steps"""
        steps = []
        
        if "Hoch" in readiness_level:
            steps = [
                "Terminvereinbarung mit Ihrer Agentur für Arbeit",
                "Businessplan finalisieren und formatieren",
                "Stellungnahme einer fachkundigen Stelle einholen",
                "Alle erforderlichen Unterlagen zusammenstellen",
                "Antrag einreichen"
            ]
        elif "Mittel" in readiness_level:
            steps = [
                "Schwachstellen in Ihrem Konzept identifizieren und beheben",
                "Businessplan von Experten prüfen lassen",
                "Fehlende Qualifikationen nachweisen oder aufbauen",
                "Finanzplanung mit einem Berater durchgehen",
                "Dann Antrag bei der Agentur für Arbeit stellen"
            ]
        else:
            steps = [
                "Gründungsberatung in Anspruch nehmen",
                "Businessplan-Workshop oder -Kurs besuchen",
                "Geschäftsidee schärfen und validieren",
                "Fachliche Kompetenzen gezielt ausbauen",
                "Assessment nach Vorbereitung wiederholen"
            ]
        
        return steps

