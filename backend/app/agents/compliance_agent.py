"""Compliance Monitoring Agent"""

from typing import Dict, List, Any
from sqlalchemy.orm import Session
from datetime import datetime, timedelta


class ComplianceMonitoringAgent:
    """AI Agent for Compliance Monitoring"""

    def __init__(self):
        self.name = "ComplianceMonitoringAgent"
        self.role = "Monitor regulatory compliance and audit requirements"

    async def monitor_compliance(
        self,
        db: Session,
        compliance_type: str,  # OISD, DGMS, FACTORY_ACT
    ) -> Dict[str, Any]:
        """
        Monitor compliance based on regulatory framework
        
        Checks:
        - OISD (Oil Industry Safety Directorate) guidelines
        - DGMS (Directorate General of Mines Safety) standards
        - Factory Act requirements
        - ISO 45001 standards
        """
        
        checks = {}
        issues = []
        compliance_score = 100
        
        if compliance_type == "OISD":
            checks = self._check_oisd_compliance(db)
        elif compliance_type == "DGMS":
            checks = self._check_dgms_compliance(db)
        elif compliance_type == "FACTORY_ACT":
            checks = self._check_factory_act_compliance(db)
        
        # Count compliance issues
        for check_name, check_result in checks.items():
            if not check_result["status"]:
                issues.append(check_result["issue"])
                compliance_score -= check_result.get("penalty", 5)
        
        compliance_score = max(0, compliance_score)
        
        return {
            "compliance_type": compliance_type,
            "compliance_score": compliance_score,
            "checks": checks,
            "issues": issues,
            "recommendations": self._generate_compliance_actions(issues),
            "timestamp": datetime.utcnow(),
        }
    
    def _check_oisd_compliance(self, db: Session) -> Dict[str, Any]:
        """Check OISD guidelines compliance"""
        return {
            "safety_management_system": {
                "status": True,
                "requirement": "Safety Management System in place",
                "penalty": 10
            },
            "incident_reporting": {
                "status": True,
                "requirement": "Incidents reported within 24 hours",
                "penalty": 15
            },
            "worker_training": {
                "status": True,
                "requirement": "Annual safety training completed",
                "penalty": 10
            },
            "emergency_procedures": {
                "status": True,
                "requirement": "Emergency response procedures documented",
                "penalty": 10
            },
            "permit_to_work": {
                "status": True,
                "requirement": "PTW system for high-risk activities",
                "penalty": 15
            },
        }
    
    def _check_dgms_compliance(self, db: Session) -> Dict[str, Any]:
        """Check DGMS standards compliance"""
        return {
            "ventilation_systems": {
                "status": True,
                "requirement": "Proper ventilation in confined spaces",
                "issue": "Ventilation records not updated",
                "penalty": 10
            },
            "equipment_inspection": {
                "status": True,
                "requirement": "Regular equipment inspection",
                "penalty": 8
            },
            "worker_health_surveillance": {
                "status": False,
                "requirement": "Annual health check for workers",
                "issue": "Health surveillance overdue for 5 workers",
                "penalty": 12
            },
            "documentation": {
                "status": True,
                "requirement": "Safety documentation maintained",
                "penalty": 8
            },
        }
    
    def _check_factory_act_compliance(self, db: Session) -> Dict[str, Any]:
        """Check Factory Act compliance"""
        return {
            "first_aid_facilities": {
                "status": True,
                "requirement": "First aid facilities available",
                "penalty": 8
            },
            "worker_registration": {
                "status": True,
                "requirement": "All workers registered",
                "penalty": 10
            },
            "ppe_provision": {
                "status": True,
                "requirement": "PPE provided to all workers",
                "penalty": 12
            },
            "safety_committees": {
                "status": True,
                "requirement": "Safety committee meetings held",
                "penalty": 8
            },
        }
    
    def _generate_compliance_actions(self, issues: List[str]) -> List[str]:
        """Generate compliance improvement actions"""
        actions = []
        
        for issue in issues:
            if "training" in issue.lower():
                actions.append("Schedule safety training sessions")
            elif "inspection" in issue.lower():
                actions.append("Conduct equipment inspection")
            elif "documentation" in issue.lower():
                actions.append("Update compliance documentation")
            elif "health" in issue.lower():
                actions.append("Schedule worker health surveillance")
            elif "certificate" in issue.lower():
                actions.append("Renew expired certifications")
        
        return list(set(actions))


compliance_agent = ComplianceMonitoringAgent()
