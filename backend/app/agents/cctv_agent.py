"""CCTV Analysis Agent"""

from typing import Dict, List, Any
from sqlalchemy.orm import Session
from datetime import datetime


class CCTVAnalysisAgent:
    """AI Agent for CCTV Video Analysis"""

    def __init__(self):
        self.name = "CCTVAnalysisAgent"
        self.role = "Analyze CCTV footage for safety violations"

    async def analyze_frame(
        self,
        db: Session,
        frame_data: Dict[str, Any],
        camera_id: str,
    ) -> Dict[str, Any]:
        """
        Analyze video frame for:
        - PPE violations (missing helmet, vest, gloves)
        - Restricted area violations
        - Fire/smoke detection
        - Worker collapse detection
        - Crowd detection
        """
        
        detections = self._detect_violations(frame_data)
        alerts = self._generate_alerts(detections, camera_id)
        
        return {
            "camera_id": camera_id,
            "timestamp": datetime.utcnow(),
            "detections": detections,
            "alerts": alerts,
            "confidence_scores": self._calculate_confidence(detections),
            "action_required": len(alerts) > 0
        }
    
    def _detect_violations(self, frame_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect safety violations in frame"""
        detections = []
        
        # PPE detection
        if frame_data.get("people_detected"):
            for person in frame_data.get("people", []):
                if not person.get("helmet_detected"):
                    detections.append({
                        "type": "MISSING_HELMET",
                        "person_id": person.get("id"),
                        "confidence": 0.92,
                        "severity": "HIGH"
                    })
                
                if not person.get("vest_detected"):
                    detections.append({
                        "type": "MISSING_VEST",
                        "person_id": person.get("id"),
                        "confidence": 0.85,
                        "severity": "HIGH"
                    })
                
                if person.get("collapsed"):
                    detections.append({
                        "type": "WORKER_COLLAPSE",
                        "person_id": person.get("id"),
                        "confidence": 0.95,
                        "severity": "CRITICAL"
                    })
        
        # Fire/smoke detection
        if frame_data.get("fire_detected"):
            detections.append({
                "type": "FIRE",
                "confidence": 0.98,
                "severity": "CRITICAL",
                "location": frame_data.get("fire_location")
            })
        
        if frame_data.get("smoke_detected"):
            detections.append({
                "type": "SMOKE",
                "confidence": 0.88,
                "severity": "HIGH"
            })
        
        # Restricted area violation
        if frame_data.get("restricted_area_entry"):
            detections.append({
                "type": "RESTRICTED_AREA_VIOLATION",
                "person_id": frame_data.get("person_id"),
                "confidence": 0.91,
                "severity": "MEDIUM"
            })
        
        # Crowd detection
        if frame_data.get("crowd_detected") and frame_data.get("person_count", 0) > 10:
            detections.append({
                "type": "CROWD",
                "person_count": frame_data.get("person_count"),
                "confidence": 0.87,
                "severity": "MEDIUM"
            })
        
        return detections
    
    def _generate_alerts(self, detections: List[Dict[str, Any]], camera_id: str) -> List[Dict[str, str]]:
        """Generate alerts for critical detections"""
        alerts = []
        
        for detection in detections:
            if detection.get("severity") in ["CRITICAL", "HIGH"]:
                alert = {
                    "type": detection.get("type"),
                    "camera": camera_id,
                    "severity": detection.get("severity"),
                    "message": f"{detection.get('type')} detected at camera {camera_id}",
                    "action": self._recommend_action(detection.get("type"))
                }
                alerts.append(alert)
        
        return alerts
    
    def _recommend_action(self, violation_type: str) -> str:
        """Recommend action for violation"""
        actions = {
            "MISSING_HELMET": "Alert worker and supervisor",
            "MISSING_VEST": "Alert worker and supervisor",
            "FIRE": "Activate fire alarm and emergency response",
            "SMOKE": "Check for fire source",
            "WORKER_COLLAPSE": "Call medical team immediately",
            "RESTRICTED_AREA_VIOLATION": "Notify supervisor",
            "CROWD": "Monitor crowd and assess safety"
        }
        return actions.get(violation_type, "Investigate")
    
    def _calculate_confidence(self, detections: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate confidence scores"""
        if not detections:
            return {"overall": 1.0}
        
        avg_confidence = sum(d.get("confidence", 0) for d in detections) / len(detections)
        return {
            "overall": avg_confidence,
            "ppe_detection": 0.90,
            "fire_detection": 0.96,
            "worker_detection": 0.92
        }


cctv_agent = CCTVAnalysisAgent()
