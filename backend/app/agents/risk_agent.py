"""Risk Assessment Agent"""

from typing import Dict, Any, List
from sqlalchemy.orm import Session
from datetime import datetime


class RiskAssessmentAgent:
    """AI Agent for Risk Assessment"""

    def __init__(self):
        self.name = "RiskAssessmentAgent"
        self.role = "Analyze sensor data and environmental factors to calculate compound risk"

    async def assess_risk(
        self,
        db: Session,
        location_zone: str,
        sensors_data: Dict[str, Any],
        workers_data: List[Dict[str, Any]],
        weather_data: Dict[str, Any],
        permit_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Assess compound risk in a location
        
        Analyzes:
        - Sensor readings (gas, temperature, pressure, humidity)
        - Worker location and PPE status
        - Weather conditions
        - Active permits and maintenance
        - Historical incident patterns
        """
        
        risk_factors = {}
        risk_score = 0
        reasoning = []
        
        # Analyze sensor data
        sensor_risk = self._analyze_sensors(sensors_data)
        risk_score += sensor_risk["score"] * 0.4
        risk_factors["sensor_risk"] = sensor_risk
        reasoning.extend(sensor_risk["observations"])
        
        # Analyze worker data
        worker_risk = self._analyze_workers(workers_data)
        risk_score += worker_risk["score"] * 0.25
        risk_factors["worker_risk"] = worker_risk
        reasoning.extend(worker_risk["observations"])
        
        # Analyze weather
        weather_risk = self._analyze_weather(weather_data)
        risk_score += weather_risk["score"] * 0.15
        risk_factors["weather_risk"] = weather_risk
        reasoning.extend(weather_risk["observations"])
        
        # Analyze permits
        permit_risk = self._analyze_permits(permit_data)
        risk_score += permit_risk["score"] * 0.2
        risk_factors["permit_risk"] = permit_risk
        reasoning.extend(permit_risk["observations"])
        
        # Normalize risk score
        risk_score = min(100, max(0, int(risk_score)))
        
        # Determine risk level
        if risk_score < 25:
            risk_level = "SAFE"
        elif risk_score < 50:
            risk_level = "MEDIUM"
        elif risk_score < 75:
            risk_level = "HIGH"
        else:
            risk_level = "CRITICAL"
        
        # Generate recommendations
        recommendations = self._generate_recommendations(risk_level, risk_factors)
        
        return {
            "location_zone": location_zone,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "factors": risk_factors,
            "reasoning": " ".join(reasoning),
            "recommendations": recommendations,
            "timestamp": datetime.utcnow(),
        }
    
    def _analyze_sensors(self, sensors_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze sensor readings"""
        observations = []
        risk = 0
        
        for sensor_name, value in sensors_data.items():
            if isinstance(value, dict) and "value" in value:
                if value.get("is_critical"):
                    risk += 40
                    observations.append(f"CRITICAL: {sensor_name} reading is critical.")
                elif value.get("is_alert"):
                    risk += 20
                    observations.append(f"WARNING: {sensor_name} reading is abnormal.")
        
        risk = min(risk, 100)
        
        if not observations:
            observations.append("All sensor readings are within safe parameters.")
        
        return {
            "score": risk,
            "observations": observations,
            "data": sensors_data
        }
    
    def _analyze_workers(self, workers_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze worker safety"""
        observations = []
        risk = 0
        
        if not workers_data:
            return {"score": 0, "observations": ["No workers in zone."], "data": []}
        
        unequipped = sum(
            1 for w in workers_data
            if not all(w.get("ppe_equipped", {}).values())
        )
        
        if unequipped > 0:
            risk += unequipped * 20
            observations.append(f"{unequipped} workers with incomplete PPE detected.")
        
        low_safety_score = sum(
            1 for w in workers_data
            if w.get("safety_score", 100) < 70
        )
        
        if low_safety_score > 0:
            risk += low_safety_score * 15
            observations.append(f"{low_safety_score} workers have low safety scores.")
        
        if not observations:
            observations.append(f"All {len(workers_data)} workers are properly equipped.")
        
        return {
            "score": min(risk, 100),
            "observations": observations,
            "worker_count": len(workers_data)
        }
    
    def _analyze_weather(self, weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze weather conditions"""
        observations = []
        risk = 0
        
        if weather_data.get("severe_weather"):
            risk += 30
            observations.append("Severe weather conditions detected.")
        
        if weather_data.get("high_temperature"):
            risk += 15
            observations.append("High temperature increases heat stress risk.")
        
        if not observations:
            observations.append("Weather conditions are normal.")
        
        return {
            "score": risk,
            "observations": observations,
            "data": weather_data
        }
    
    def _analyze_permits(self, permit_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze permit status"""
        observations = []
        risk = 0
        
        if permit_data.get("has_hot_work") and permit_data.get("fire_watch_missing"):
            risk += 35
            observations.append("Hot work without fire watch coverage detected.")
        
        if permit_data.get("has_confined_space") and permit_data.get("ventilation_missing"):
            risk += 40
            observations.append("Confined space work without proper ventilation.")
        
        if permit_data.get("expired_permit"):
            risk += 25
            observations.append("Expired work permit detected.")
        
        if not observations:
            observations.append("All permits are valid and conditions are met.")
        
        return {
            "score": risk,
            "observations": observations,
            "permit_count": len([p for p in permit_data.values() if p])
        }
    
    def _generate_recommendations(self, risk_level: str, factors: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on risk level"""
        recommendations = []
        
        if risk_level == "CRITICAL":
            recommendations = [
                "EVACUATE zone immediately",
                "Activate emergency response protocols",
                "Notify emergency services",
                "Secure all equipment"
            ]
        elif risk_level == "HIGH":
            recommendations = [
                "Restrict entry to zone",
                "Increase worker supervision",
                "Conduct safety briefing",
                "Inspect and repair faulty sensors"
            ]
        elif risk_level == "MEDIUM":
            recommendations = [
                "Increase monitoring frequency",
                "Inspect PPE compliance",
                "Review work procedures"
            ]
        else:  # SAFE
            recommendations = [
                "Continue normal operations",
                "Maintain regular monitoring",
                "Document sensor readings"
            ]
        
        return recommendations


risk_agent = RiskAssessmentAgent()
