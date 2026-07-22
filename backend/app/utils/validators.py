"""Validation Utilities"""

from typing import Dict, Any, List, Tuple
import re


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_sensor_reading(reading: Dict[str, Any], sensor_config: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate sensor reading against configuration"""
    errors = []
    
    value = reading.get("value")
    if value is None:
        errors.append("Value is required")
        return False, errors
    
    if sensor_config.get("min_threshold") and value < sensor_config["min_threshold"]:
        errors.append(f"Value below minimum threshold: {sensor_config['min_threshold']}")
    
    if sensor_config.get("max_threshold") and value > sensor_config["max_threshold"]:
        errors.append(f"Value above maximum threshold: {sensor_config['max_threshold']}")
    
    return len(errors) == 0, errors


def validate_permit_conditions(permit_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate permit conditions are met"""
    errors = []
    
    if permit_data.get("permit_type") == "hot_work":
        if not permit_data.get("fire_watch_present"):
            errors.append("Fire watch personnel required for hot work")
        if not permit_data.get("fire_extinguisher_ready"):
            errors.append("Fire extinguisher must be ready")
    
    if permit_data.get("permit_type") == "confined_space":
        if not permit_data.get("atmosphere_tested"):
            errors.append("Atmosphere must be tested before entry")
        if not permit_data.get("ventilation_active"):
            errors.append("Ventilation must be active")
    
    return len(errors) == 0, errors


def validate_worker_ppe(worker_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate worker has required PPE"""
    errors = []
    
    if not worker_data.get("helmet_equipped"):
        errors.append("Helmet is required")
    if not worker_data.get("vest_equipped"):
        errors.append("Safety vest is required")
    if not worker_data.get("gloves_equipped"):
        errors.append("Work gloves are required")
    
    return len(errors) == 0, errors
