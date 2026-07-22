"""Chatbot Agent"""

from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime


class ChatbotAgent:
    """AI Chatbot for Safety Intelligence"""

    def __init__(self):
        self.name = "ChatbotAgent"
        self.role = "Answer safety questions and provide guidance"

    async def process_query(
        self,
        db: Session,
        user_query: str,
        context: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        Process user query and generate response
        Supports:
        - Risk explanations
        - Alert clarifications
        - Procedure guidance
        - Incident history
        - Regulatory information
        """
        
        context = context or {}
        
        # Classify query
        query_type = self._classify_query(user_query)
        
        # Generate response based on query type
        if query_type == "risk_explanation":
            response = await self._explain_risk(db, user_query)
        elif query_type == "alert_explanation":
            response = await self._explain_alert(db, user_query, context)
        elif query_type == "procedure_guidance":
            response = await self._provide_procedure(db, user_query)
        elif query_type == "incident_history":
            response = await self._get_incident_info(db, user_query)
        elif query_type == "regulatory_guidance":
            response = await self._provide_regulatory_info(user_query)
        else:
            response = self._provide_general_response(user_query)
        
        return {
            "message": response["message"],
            "context": response.get("context", {}),
            "sources": response.get("sources", []),
            "follow_up_questions": response.get("follow_ups", []),
            "timestamp": datetime.utcnow()
        }
    
    def _classify_query(self, query: str) -> str:
        """Classify user query type"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["why", "risk", "zone"]):
            return "risk_explanation"
        elif any(word in query_lower for word in ["alert", "warning"]):
            return "alert_explanation"
        elif any(word in query_lower for word in ["how", "procedure", "process"]):
            return "procedure_guidance"
        elif any(word in query_lower for word in ["incident", "accident", "history"]):
            return "incident_history"
        elif any(word in query_lower for word in ["regulation", "compliance", "standard"]):
            return "regulatory_guidance"
        else:
            return "general"
    
    async def _explain_risk(self, db: Session, query: str) -> Dict[str, Any]:
        """Explain risk in a zone"""
        return {
            "message": "Risk in Zone A is HIGH (75/100) due to: 2 critical gas sensor readings (above threshold), "
                       "3 workers without complete PPE, and 1 active hot work permit without dedicated fire watch. "
                       "Recommend restricting zone entry and increasing supervision.",
            "context": {"zone": "Zone A", "risk_score": 75},
            "sources": ["Current sensor readings", "Worker status", "Active permits"],
            "follow_ups": [
                "What sensors are exceeding thresholds?",
                "Which workers need PPE?",
                "What actions should be taken?"
            ]
        }
    
    async def _explain_alert(self, db: Session, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Explain an alert"""
        return {
            "message": "This alert was triggered because gas sensors in Zone B detected CO levels at 150 ppm, "
                       "exceeding the safe threshold of 100 ppm. This poses a risk of CO poisoning if workers "
                       "are exposed. Immediate actions: Increase ventilation, check for gas source, evacuate if "
                       "levels continue to rise.",
            "context": {"alert_type": "GAS_THRESHOLD", "gas": "CO", "level": 150},
            "sources": ["Sensor ID: SENSOR-ZONE-B-001"],
            "follow_ups": [
                "What caused the high gas levels?",
                "What ventilation action is needed?",
                "Should the zone be evacuated?"
            ]
        }
    
    async def _provide_procedure(self, db: Session, query: str) -> Dict[str, Any]:
        """Provide procedural guidance"""
        return {
            "message": "To obtain a Hot Work Permit: 1) Identify the work area and equipment. 2) Complete the "
                       "permit form specifying work type and duration. 3) Have the area inspected for combustibles. "
                       "4) Arrange for a dedicated fire watch personnel. 5) Submit to supervisor for approval. "
                       "6) Conduct final safety briefing with all workers. 7) Display permit visibly at work site.",
            "context": {"procedure": "hot_work_permit"},
            "sources": ["Safety Procedures Manual", "OISD Guidelines"],
            "follow_ups": [
                "What is the approval timeline?",
                "What are the fire watch requirements?",
                "Are there any additional certifications needed?"
            ]
        }
    
    async def _get_incident_info(self, db: Session, query: str) -> Dict[str, Any]:
        """Get incident history and information"""
        return {
            "message": "In the past 30 days, there have been 5 incidents: 2 minor injuries from slips, "
                       "1 equipment damage, 1 near-miss fall incident, 1 chemical exposure incident. "
                       "Most common causes: insufficient PPE usage and inadequate training. Recommended actions: "
                       "Increase safety training frequency and enforce PPE compliance.",
            "context": {"period": "30 days", "incident_count": 5},
            "sources": ["Incident database"],
            "follow_ups": [
                "Which incidents were most serious?",
                "What were the root causes?",
                "What preventive measures are planned?"
            ]
        }
    
    async def _provide_regulatory_info(self, query: str) -> Dict[str, Any]:
        """Provide regulatory guidance"""
        return {
            "message": "Under OISD guidelines: All facilities must have a documented Safety Management System, "
                       "conduct incident reporting within 24 hours, ensure annual safety training, and maintain "
                       "emergency response procedures. For confined space work, DGMS standards require ventilation "
                       "certification, atmosphere testing, and rescue team readiness. Non-compliance can result in "
                       "fines and operational restrictions.",
            "context": {"regulations": ["OISD", "DGMS"]},
            "sources": ["OISD Guidelines", "DGMS Standards", "Factory Act"],
            "follow_ups": [
                "What are specific OISD requirements?",
                "How often must safety training be conducted?",
                "What are the penalties for non-compliance?"
            ]
        }
    
    def _provide_general_response(self, query: str) -> Dict[str, Any]:
        """Provide general response"""
        return {
            "message": "I'm the Industrial Safety Intelligence Chatbot. I can help you with: risk zone explanations, "
                       "alert clarifications, safety procedures, incident history, and regulatory guidance. "
                       "Please ask a specific question about safety or operations.",
            "context": {},
            "sources": [],
            "follow_ups": [
                "What is the current risk level in my zone?",
                "How do I obtain a work permit?",
                "What incidents have occurred recently?"
            ]
        }
    
    async def explain_alert(self, db: Session, alert_id: str) -> Optional[Dict[str, Any]]:
        """Explain a specific alert"""
        # In production, fetch alert from database and generate explanation
        return {
            "alert_id": alert_id,
            "explanation": "This is an explanation of the alert"
        }
    
    async def suggest_actions(self, db: Session, risk_zone: str) -> List[str]:
        """Suggest actions for a risk zone"""
        # In production, analyze zone and generate contextual actions
        return [
            "Increase supervision in zone",
            "Check sensor readings",
            "Inspect worker PPE compliance",
            "Review active permits"
        ]


chatbot_agent = ChatbotAgent()
