"""Risk Assessment Service"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models import RiskAssessment, Sensor, SensorReading, Worker
from app.services.sensor import get_sensor_readings_by_zone
from app.services.worker import get_workers_in_zone


async def assess_zone_risk(db: Session, location_zone: str) -> Dict[str, Any]:
    """Assess risk for a location zone"""
    # Collect sensor data
    sensors_data = await get_sensor_readings_by_zone(db, location_zone)
    
    # Collect worker data
    workers = await get_workers_in_zone(db, location_zone)
    workers_data = [
        {
            "id": str(w.id),
            "name": w.name,
            "safety_score": w.safety_score,
            "ppe_equipped": {
                "helmet": w.helmet_equipped,
                "vest": w.vest_equipped,
                "gloves": w.gloves_equipped
            }
        }
        for w in workers
    ]
    
    # Calculate risk score (simplified)
    risk_score = calculate_risk_score(sensors_data, workers_data)
    
    # Determine risk level
    if risk_score < 25:
        risk_level = "SAFE"
    elif risk_score < 50:
        risk_level = "MEDIUM"
    elif risk_score < 75:
        risk_level = "HIGH"
    else:
        risk_level = "CRITICAL"
    
    # Create assessment record
    assessment = RiskAssessment(
        location_zone=location_zone,
        risk_score=risk_score,
        risk_level=risk_level,
        sensor_risk=calculate_sensor_risk(sensors_data),
        worker_risk=calculate_worker_risk(workers_data),
        factors=extract_risk_factors(sensors_data, workers_data),
        reasoning=generate_reasoning(risk_level, sensors_data, workers_data),
        key_risks=extract_key_risks(sensors_data, workers_data),
        recommended_actions=generate_actions(risk_level),
        workers_in_zone=workers_data,
        sensors_in_zone=sensors_data,
    )
    
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    
    return {
        "id": str(assessment.id),
        "location_zone": assessment.location_zone,
        "risk_score": assessment.risk_score,
        "risk_level": assessment.risk_level,
        "factors": assessment.factors,
        "reasoning": assessment.reasoning,
        "key_risks": assessment.key_risks,
        "recommended_actions": assessment.recommended_actions,
        "timestamp": assessment.timestamp
    }


async def get_all_zones_risk(db: Session) -> List[Dict[str, Any]]:
    """Get risk levels for all zones"""
    # Get latest assessment for each zone
    zones = set(s.location_zone for s in db.query(Sensor).all())
    
    zones_risk = []
    for zone in zones:
        assessment = db.query(RiskAssessment).filter(
            RiskAssessment.location_zone == zone
        ).order_by(desc(RiskAssessment.timestamp)).first()
        
        if assessment:
            zones_risk.append({
                "zone": zone,
                "risk_score": assessment.risk_score,
                "risk_level": assessment.risk_level,
                "timestamp": assessment.timestamp
            })
    
    return zones_risk


async def get_risk_history(db: Session, location_zone: str, hours: int = 24) -> List[Dict[str, Any]]:
    """Get risk assessment history for a zone"""
    since = datetime.utcnow() - timedelta(hours=hours)
    
    assessments = db.query(RiskAssessment).filter(
        RiskAssessment.location_zone == location_zone,
        RiskAssessment.timestamp >= since
    ).order_by(RiskAssessment.timestamp).all()
    
    return [
        {
            "risk_score": a.risk_score,
            "risk_level": a.risk_level,
            "timestamp": a.timestamp
        }
        for a in assessments
    ]


def calculate_risk_score(sensors_data: List[dict], workers_data: List[dict]) -> int:
    """Calculate overall risk score (0-100)"""
    sensor_risk = 0
    
    # Analyze sensor data
    for sensor in sensors_data:
        if sensor.get("is_critical"):
            sensor_risk += 40
        elif sensor.get("is_alert"):
            sensor_risk += 20
    
    sensor_risk = min(sensor_risk, 50)  # Cap at 50
    
    # Analyze worker data
    worker_risk = 0
    for worker in workers_data:
        ppe = worker.get("ppe_equipped", {})
        if not all(ppe.values()):
            worker_risk += 15
        
        if worker.get("safety_score", 100) < 80:
            worker_risk += 10
    
    worker_risk = min(worker_risk, 50)  # Cap at 50
    
    # Combined risk (simplified)
    total_risk = (sensor_risk + worker_risk) // 2
    
    return min(total_risk, 100)


def calculate_sensor_risk(sensors_data: List[dict]) -> int:
    """Calculate sensor-based risk"""
    if not sensors_data:
        return 0
    
    critical_count = sum(1 for s in sensors_data if s.get("is_critical"))
    alert_count = sum(1 for s in sensors_data if s.get("is_alert"))
    
    return min((critical_count * 40 + alert_count * 20) // len(sensors_data), 100)


def calculate_worker_risk(workers_data: List[dict]) -> int:
    """Calculate worker-based risk"""
    if not workers_data:
        return 0
    
    ppe_risk = sum(
        1 for w in workers_data
        if not all(w.get("ppe_equipped", {}).values())
    ) * 30
    
    safety_risk = sum(
        1 for w in workers_data
        if w.get("safety_score", 100) < 80
    ) * 20
    
    return min((ppe_risk + safety_risk) // len(workers_data), 100)


def extract_risk_factors(sensors_data: List[dict], workers_data: List[dict]) -> Dict[str, Any]:
    """Extract risk factors"""
    return {
        "sensor_count": len(sensors_data),
        "worker_count": len(workers_data),
        "alert_sensors": sum(1 for s in sensors_data if s.get("is_alert")),
        "critical_sensors": sum(1 for s in sensors_data if s.get("is_critical")),
        "unequipped_workers": sum(
            1 for w in workers_data
            if not all(w.get("ppe_equipped", {}).values())
        )
    }


def extract_key_risks(sensors_data: List[dict], workers_data: List[dict]) -> List[str]:
    """Extract key risks"""
    risks = []
    
    critical_sensors = [s for s in sensors_data if s.get("is_critical")]
    if critical_sensors:
        risks.append("Critical sensor readings detected")
    
    unequipped = [w for w in workers_data if not all(w.get("ppe_equipped", {}).values())]
    if unequipped:
        risks.append(f"{len(unequipped)} workers with incomplete PPE")
    
    return risks


def generate_reasoning(risk_level: str, sensors_data: List[dict], workers_data: List[dict]) -> str:
    """Generate AI reasoning for risk level"""
    return f"Risk level {risk_level} determined based on {len(sensors_data)} sensors and {len(workers_data)} workers in zone."


def generate_actions(risk_level: str) -> List[str]:
    """Generate recommended actions"""
    actions_map = {
        "SAFE": ["Continue normal operations", "Monitor sensor readings"],
        "MEDIUM": ["Increase monitoring frequency", "Inspect PPE compliance"],
        "HIGH": ["Restrict entry to zone", "Increase worker supervision", "Activate emergency protocols"],
        "CRITICAL": ["Evacuate zone immediately", "Activate full emergency response", "Notify emergency services"]
    }
    return actions_map.get(risk_level, [])
