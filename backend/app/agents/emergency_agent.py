"""Emergency Response Orchestration Agent"""

from typing import Dict, List, Any
from sqlalchemy.orm import Session
from datetime import datetime


class EmergencyResponseAgent:
    """AI Agent for Emergency Response Orchestration"""

    def __init__(self):
        self.name = "EmergencyResponseAgent"
        self.role = "Orchestrate emergency response and notifications"

    async def handle_emergency(
        self,
        db: Session,
        emergency_type: str,
        location: Dict[str, Any],
        affected_workers: List[str],
    ) -> Dict[str, Any]:
        """
        Handle emergency incidents:
        - Fire, explosion, chemical spill
        - Worker injuries
        - Equipment failures
        - Environmental hazards
        """
        
        response_plan = self._get_response_plan(emergency_type)
        notifications = self._generate_notifications(emergency_type, location)
        evacuation_plan = self._generate_evacuation_plan(location, affected_workers)
        
        return {
            "emergency_type": emergency_type,
            "severity_level": self._assess_severity(emergency_type),
            "response_plan": response_plan,
            "notifications": notifications,
            "evacuation_plan": evacuation_plan,
            "resources_needed": self._allocate_resources(emergency_type),
            "estimated_response_time": "5-10 minutes",
            "timestamp": datetime.utcnow(),
        }
    
    def _get_response_plan(self, emergency_type: str) -> List[Dict[str, str]]:
        """Get response plan for emergency type"""
        plans = {
            "fire": [
                {"step": 1, "action": "Activate fire alarm", "responsibility": "First responder"},
                {"step": 2, "action": "Evacuate zone", "responsibility": "Supervisor"},
                {"step": 3, "action": "Use fire extinguisher (if safe)", "responsibility": "Trained personnel"},
                {"step": 4, "action": "Call fire department", "responsibility": "Safety officer"},
                {"step": 5, "action": "Account for all workers", "responsibility": "Supervisor"},
            ],
            "chemical_spill": [
                {"step": 1, "action": "Stop work immediately", "responsibility": "Area supervisor"},
                {"step": 2, "action": "Alert nearby workers", "responsibility": "First responder"},
                {"step": 3, "action": "Contain spill", "responsibility": "Response team"},
                {"step": 4, "action": "Call hazmat team", "responsibility": "Safety officer"},
                {"step": 5, "action": "Medical evaluation", "responsibility": "Medical team"},
            ],
            "worker_injury": [
                {"step": 1, "action": "Call for medical help", "responsibility": "Nearest person"},
                {"step": 2, "action": "Provide first aid", "responsibility": "Trained responder"},
                {"step": 3, "action": "Secure the area", "responsibility": "Supervisor"},
                {"step": 4, "action": "Document incident", "responsibility": "Safety officer"},
                {"step": 5, "action": "Notify management", "responsibility": "Supervisor"},
            ]
        }
        return plans.get(emergency_type, [])
    
    def _generate_notifications(self, emergency_type: str, location: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate notification list"""
        notifications = [
            {
                "recipient": "Safety Officer",
                "channel": "SMS + Email + In-app alert",
                "priority": "Critical"
            },
            {
                "recipient": "Plant Manager",
                "channel": "SMS + Call + Email",
                "priority": "Critical"
            },
            {
                "recipient": "Emergency Response Team",
                "channel": "SMS + In-app alert",
                "priority": "Critical"
            },
            {
                "recipient": "Medical Team",
                "channel": "Direct call + SMS",
                "priority": "Critical"
            },
            {
                "recipient": "Nearby Workers",
                "channel": "Alarm + SMS",
                "priority": "High"
            }
        ]
        
        return notifications
    
    def _generate_evacuation_plan(self, location: Dict[str, Any], workers: List[str]) -> Dict[str, Any]:
        """Generate evacuation plan"""
        return {
            "evacuation_zone": location.get("zone", "Unknown"),
            "assembly_point": f"Assembly Point - {location.get('zone', 'Area')} A",
            "estimated_evacuation_time": "5-10 minutes",
            "affected_workers": len(workers),
            "evacuation_routes": [
                "Route 1: Main Exit",
                "Route 2: Emergency Exit - North",
                "Route 3: Emergency Exit - South"
            ],
            "personnel_accountability": "Mandatory headcount at assembly point"
        }
    
    def _assess_severity(self, emergency_type: str) -> str:
        """Assess severity level"""
        severity_map = {
            "fire": "CRITICAL",
            "explosion": "CRITICAL",
            "chemical_spill": "HIGH",
            "worker_injury": "HIGH",
            "equipment_failure": "MEDIUM"
        }
        return severity_map.get(emergency_type, "MEDIUM")
    
    def _allocate_resources(self, emergency_type: str) -> List[str]:
        """Allocate resources needed for response"""
        resources_map = {
            "fire": ["Fire extinguishers", "First aid kit", "Emergency lighting", "Communication devices"],
            "chemical_spill": ["PPE kits", "Absorbent materials", "Containment equipment", "Medical supplies"],
            "worker_injury": ["First aid kit", "Stretcher", "Medical supplies", "Transport vehicle"],
        }
        return resources_map.get(emergency_type, [])


emergency_agent = EmergencyResponseAgent()
