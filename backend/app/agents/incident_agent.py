"""Incident Analysis Agent"""

from typing import Dict, List, Any
from sqlalchemy.orm import Session
from datetime import datetime


class IncidentAnalysisAgent:
    """AI Agent for Incident Analysis and RAG"""

    def __init__(self):
        self.name = "IncidentAnalysisAgent"
        self.role = "Analyze incidents and retrieve similar historical patterns"

    async def analyze_incident(
        self,
        db: Session,
        incident_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Analyze incident using:
        - RAG (Retrieval-Augmented Generation) for similar incidents
        - Root cause analysis
        - Prevention recommendations
        """
        
        # Retrieve similar incidents from knowledge base
        similar_incidents = await self._retrieve_similar_incidents(
            db,
            incident_data.get("incident_type"),
            incident_data.get("location_zone")
        )
        
        # Analyze root cause
        root_cause = self._analyze_root_cause(incident_data)
        
        # Generate preventive actions based on similar incidents
        preventive_actions = self._generate_preventive_actions(
            incident_data,
            similar_incidents
        )
        
        # Map to regulatory requirements
        regulatory_mapping = self._map_to_regulations(incident_data)
        
        return {
            "incident_type": incident_data.get("incident_type"),
            "root_cause_analysis": root_cause,
            "similar_incidents": similar_incidents,
            "preventive_actions": preventive_actions,
            "regulatory_mapping": regulatory_mapping,
            "severity_assessment": incident_data.get("severity"),
            "timestamp": datetime.utcnow(),
        }
    
    async def _retrieve_similar_incidents(
        self,
        db: Session,
        incident_type: str,
        location_zone: str
    ) -> List[Dict[str, Any]]:
        """
        Retrieve similar incidents from RAG knowledge base
        In production, this would use FAISS vector search
        """
        
        # Mock similar incidents (in production, use semantic search)
        similar_patterns = {
            "minor_injury": [
                "Slips and falls on wet surfaces",
                "Minor cuts from equipment",
                "Repetitive strain injuries"
            ],
            "serious_injury": [
                "Equipment-related trauma",
                "Fall from height incidents",
                "Chemical exposure"
            ],
            "near_miss": [
                "Close calls with machinery",
                "Potential fall hazards",
                "Equipment failures"
            ]
        }
        
        patterns = similar_patterns.get(incident_type, [])
        return [
            {"pattern": p, "frequency": "3-5 times/year", "location": location_zone}
            for p in patterns[:5]
        ]
    
    def _analyze_root_cause(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze root cause of incident"""
        return {
            "primary_cause": incident_data.get("root_cause", "Unknown"),
            "contributing_factors": incident_data.get("contributing_factors", []),
            "human_factors": ["Lack of attention", "Improper procedure"],
            "systemic_factors": ["Inadequate training", "Poor maintenance"],
            "environmental_factors": ["Wet surfaces", "Poor lighting"]
        }
    
    def _generate_preventive_actions(
        self,
        incident_data: Dict[str, Any],
        similar_incidents: List[Dict[str, Any]]
    ) -> List[Dict[str, str]]:
        """Generate preventive actions based on incident and similar patterns"""
        return [
            {
                "action": "Implement additional safety training",
                "priority": "High",
                "timeline": "2 weeks"
            },
            {
                "action": "Review and update safety procedures",
                "priority": "High",
                "timeline": "1 week"
            },
            {
                "action": "Conduct equipment inspection and maintenance",
                "priority": "Medium",
                "timeline": "1 month"
            },
            {
                "action": "Install additional safety barriers/signage",
                "priority": "Medium",
                "timeline": "2 weeks"
            },
            {
                "action": "Increase monitoring and supervision",
                "priority": "High",
                "timeline": "Immediate"
            }
        ]
    
    def _map_to_regulations(self, incident_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Map incident to regulatory requirements"""
        incident_type = incident_data.get("incident_type", "")
        
        regulation_map = {
            "serious_injury": [
                "OISD - Incident Reporting",
                "Factory Act - Injury Report",
                "DGMS - Accident Investigation"
            ],
            "fatality": [
                "OISD - Major Incident Report",
                "Factory Act - Fatality Report",
                "DGMS - Mandatory Investigation",
                "Police - FIR Registration"
            ],
            "near_miss": [
                "Internal Safety Review",
                "Risk Assessment Update"
            ]
        }
        
        return {
            "applicable_regulations": regulation_map.get(incident_type, []),
            "reporting_deadline": "24-48 hours",
            "investigation_required": incident_type != "near_miss"
        }


incident_agent = IncidentAnalysisAgent()
