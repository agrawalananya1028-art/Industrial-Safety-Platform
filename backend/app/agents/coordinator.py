"""Coordinator Agent - Master Orchestrator"""

from typing import Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime

from app.agents import (
    risk_agent,
    permit_agent,
    compliance_agent,
    incident_agent,
    emergency_agent,
    cctv_agent,
)
from app.schemas.permit import PermitValidationRequest


class CoordinatorAgent:
    """Master Coordinator Agent"""

    def __init__(self):
        self.name = "CoordinatorAgent"
        self.role = "Orchestrate all agents for comprehensive safety management"
        self.agents = {
            "risk": risk_agent,
            "permit": permit_agent,
            "compliance": compliance_agent,
            "incident": incident_agent,
            "emergency": emergency_agent,
            "cctv": cctv_agent,
        }

    async def validate_permit(
        self,
        db: Session,
        validation_request: PermitValidationRequest
    ) -> Dict[str, Any]:
        """
        Validate permit using permit agent
        Coordinates with other agents if needed
        """
        result = await permit_agent.validate_permit(
            db,
            permit_type="hot_work",
            permit_data=validation_request.sensor_readings or {},
            worker_status=validation_request.worker_status or {},
            sensor_readings=validation_request.sensor_readings or {},
            location_data=validation_request.location_data or {},
        )
        
        # If permit unsafe, check risk assessment
        if not result["is_approved"]:
            # Could coordinate with risk agent for additional insights
            pass
        
        return {
            "permit_id": str(validation_request.permit_id),
            "is_approved": result["is_approved"],
            "reasoning": result["reasoning"],
            "unsafe_conditions": result["unsafe_conditions"],
            "recommendations": result["recommendations"],
            "timestamp": datetime.utcnow()
        }
    
    async def comprehensive_assessment(
        self,
        db: Session,
        location_zone: str,
        sensor_data: Dict[str, Any],
        worker_data: list,
    ) -> Dict[str, Any]:
        """
        Run comprehensive safety assessment
        Coordinates all agents for complete picture
        """
        
        # Risk assessment
        risk_result = await risk_agent.assess_risk(
            db,
            location_zone,
            sensor_data,
            worker_data,
            {}, {},
        )
        
        # Compliance check
        compliance_result = await compliance_agent.monitor_compliance(db, "OISD")
        
        # Aggregate results
        return {
            "location_zone": location_zone,
            "risk_assessment": risk_result,
            "compliance_status": compliance_result,
            "overall_safety_status": "SAFE" if risk_result["risk_level"] == "SAFE" else "AT_RISK",
            "timestamp": datetime.utcnow()
        }


coordinator_agent = CoordinatorAgent()
