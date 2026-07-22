"""Permit Validation Agent"""

from typing import Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime


class PermitValidationAgent:
    """AI Agent for Permit Validation"""

    def __init__(self):
        self.name = "PermitValidationAgent"
        self.role = "Validate work permits based on real-time conditions"

    async def validate_permit(
        self,
        db: Session,
        permit_type: str,
        permit_data: Dict[str, Any],
        worker_status: Dict[str, Any],
        sensor_readings: Dict[str, Any],
        location_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Validate permit based on:
        - Permit type and conditions
        - Worker certification and PPE
        - Current sensor readings
        - Location and equipment status
        """
        
        checks = {}
        unsafe_conditions = []
        is_safe = True
        reasoning = []
        
        # Check permit type specific conditions
        if permit_type == "hot_work":
            checks["fire_watch"] = permit_data.get("fire_watch_present", False)
            checks["fire_extinguisher"] = permit_data.get("fire_extinguisher_ready", False)
            checks["no_combustibles"] = location_data.get("combustibles_cleared", False)
            
            if not checks["fire_watch"]:
                unsafe_conditions.append("No fire watch personnel assigned")
                is_safe = False
            
            if not checks["fire_extinguisher"]:
                unsafe_conditions.append("Fire extinguisher not ready")
                is_safe = False
        
        elif permit_type == "confined_space":
            checks["ventilation"] = permit_data.get("ventilation_active", False)
            checks["atmosphere_tested"] = permit_data.get("atmosphere_tested", False)
            checks["rescue_ready"] = permit_data.get("rescue_team_ready", False)
            
            # Check gas sensors
            if sensor_readings.get("gas_level", 0) > 50:
                unsafe_conditions.append(f"Gas level too high: {sensor_readings.get('gas_level')} ppm")
                is_safe = False
            
            if not checks["ventilation"]:
                unsafe_conditions.append("Ventilation not active")
                is_safe = False
        
        elif permit_type == "height_work":
            checks["harness_ready"] = worker_status.get("harness_equipped", False)
            checks["anchor_point"] = location_data.get("anchor_point_available", False)
            checks["weather_safe"] = location_data.get("high_wind", False) == False
            
            if not checks["harness_ready"]:
                unsafe_conditions.append("Safety harness not equipped")
                is_safe = False
            
            if not checks["weather_safe"]:
                unsafe_conditions.append("High wind conditions - unsafe for height work")
                is_safe = False
        
        # Check worker certification
        if not worker_status.get("certified", False):
            unsafe_conditions.append("Worker not certified for this permit type")
            is_safe = False
        
        # Check PPE
        ppe = worker_status.get("ppe", {})
        if not ppe.get("helmet"):
            unsafe_conditions.append("Helmet not equipped")
            is_safe = False
        
        if not ppe.get("vest"):
            unsafe_conditions.append("Safety vest not equipped")
            is_safe = False
        
        if is_safe:
            reasoning = [f"Permit {permit_type} can be safely approved."]
        else:
            reasoning = [f"Permit {permit_type} cannot be approved due to unsafe conditions."]
        
        recommendations = self._generate_recommendations(permit_type, unsafe_conditions)
        
        return {
            "permit_type": permit_type,
            "is_approved": is_safe,
            "checks_passed": sum(1 for v in checks.values() if v),
            "checks_total": len(checks),
            "unsafe_conditions": unsafe_conditions,
            "reasoning": " ".join(reasoning),
            "recommendations": recommendations,
            "timestamp": datetime.utcnow(),
        }
    
    def _generate_recommendations(self, permit_type: str, unsafe_conditions: list) -> list:
        """Generate recommendations to make permit safe"""
        recommendations = []
        
        for condition in unsafe_conditions:
            if "fire watch" in condition.lower():
                recommendations.append("Assign certified fire watch personnel")
            elif "ventilation" in condition.lower():
                recommendations.append("Activate mechanical ventilation system")
            elif "harness" in condition.lower():
                recommendations.append("Equip worker with approved safety harness")
            elif "wind" in condition.lower():
                recommendations.append("Reschedule work after weather improves")
            elif "certified" in condition.lower():
                recommendations.append("Request certified worker for this permit type")
            elif "PPE" in condition:
                recommendations.append("Provide required PPE before starting work")
        
        return list(set(recommendations))  # Remove duplicates


permit_agent = PermitValidationAgent()
