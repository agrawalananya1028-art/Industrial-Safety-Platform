"""Helper Utilities"""

from datetime import datetime, timedelta
from typing import Dict, Any, List
import json


def calculate_risk_score(factors: Dict[str, float]) -> int:
    """Calculate risk score from multiple factors"""
    if not factors:
        return 0
    
    weighted_score = sum(factors.values()) / len(factors)
    return min(int(weighted_score), 100)


def format_datetime(dt: datetime) -> str:
    """Format datetime for display"""
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def get_time_remaining(expiry_time: datetime) -> str:
    """Get human-readable time remaining"""
    now = datetime.utcnow()
    diff = expiry_time - now
    
    if diff.days > 0:
        return f"{diff.days} days"
    elif diff.seconds > 3600:
        return f"{diff.seconds // 3600} hours"
    elif diff.seconds > 60:
        return f"{diff.seconds // 60} minutes"
    else:
        return "Expiring soon"


def get_risk_color(risk_score: int) -> str:
    """Get color code for risk level"""
    if risk_score < 25:
        return "#00FF00"  # Green - Safe
    elif risk_score < 50:
        return "#FFFF00"  # Yellow - Medium
    elif risk_score < 75:
        return "#FF8800"  # Orange - High
    else:
        return "#FF0000"  # Red - Critical


def parse_sensor_data(raw_data: str) -> Dict[str, Any]:
    """Parse raw sensor data"""
    try:
        return json.loads(raw_data)
    except json.JSONDecodeError:
        return {}


def generate_report_summary(data: Dict[str, Any]) -> str:
    """Generate summary report from data"""
    summary = f"""
    Report Summary
    ==============
    Generated: {format_datetime(datetime.utcnow())}
    
    Key Metrics:
    - Total Incidents: {data.get('total_incidents', 0)}
    - Critical Incidents: {data.get('critical_incidents', 0)}
    - Active Alerts: {data.get('active_alerts', 0)}
    - Compliance Score: {data.get('compliance_score', 0)}%
    """
    return summary
