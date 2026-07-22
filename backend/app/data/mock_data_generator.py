"""Mock Data Generator for Development and Testing"""

import random
import string
from datetime import datetime, timedelta
from uuid import uuid4
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine, Base
from app.models import (
    Worker, Sensor, SensorReading, Permit, Incident,
    Alert, RiskAssessment, ComplianceRecord, Machine, User
)
from app.models.worker import WorkerStatus
from app.models.sensor import SensorType, SensorStatus
from app.models.permit import PermitType, PermitStatus
from app.models.incident import IncidentType, IncidentSeverity
from app.models.alert import AlertType, AlertSeverity, AlertStatus
from app.models.compliance import ComplianceType, ComplianceStatus
from app.models.user import UserRole


def init_database():
    """Initialize database schema"""
    Base.metadata.create_all(bind=engine)
    print("Database schema created successfully")


def generate_mock_workers(db: Session, count: int = 20):
    """Generate mock worker data"""
    departments = ["Operations", "Maintenance", "Safety", "Engineering", "Administration"]
    roles = ["Operator", "Technician", "Supervisor", "Manager", "Coordinator"]
    zones = ["Zone A", "Zone B", "Zone C", "Zone D"]
    
    for i in range(count):
        worker = Worker(
            name=f"Worker-{i+1}",
            email=f"worker{i+1}@company.com",
            employee_id=f"EMP{str(i+1).zfill(4)}",
            department=random.choice(departments),
            role=random.choice(roles),
            status=random.choice(list(WorkerStatus)),
            latitude=28.6139 + random.uniform(-0.01, 0.01),
            longitude=77.2090 + random.uniform(-0.01, 0.01),
            current_zone=random.choice(zones),
            safety_score=random.uniform(70, 100),
            helmet_equipped=random.choice([True, False]),
            vest_equipped=random.choice([True, False]),
            gloves_equipped=random.choice([True, False]),
        )
        db.add(worker)
    
    db.commit()
    print(f"Created {count} mock workers")


def generate_mock_sensors(db: Session, count: int = 20):
    """Generate mock sensor data"""
    zones = ["Zone A", "Zone B", "Zone C", "Zone D"]
    sensor_types = list(SensorType)
    
    for i in range(count):
        sensor = Sensor(
            name=f"Sensor-{i+1}",
            sensor_id=f"SENSOR{str(i+1).zfill(4)}",
            sensor_type=random.choice(sensor_types),
            location_zone=random.choice(zones),
            latitude=28.6139 + random.uniform(-0.01, 0.01),
            longitude=77.2090 + random.uniform(-0.01, 0.01),
            unit="ppm" if random.choice([True, False]) else "°C",
            min_threshold=random.uniform(0, 50),
            max_threshold=random.uniform(50, 100),
            critical_threshold=random.uniform(100, 150),
            status=random.choice(list(SensorStatus)),
            battery_level=random.randint(20, 100),
        )
        db.add(sensor)
    
    db.commit()
    print(f"Created {count} mock sensors")


def generate_mock_sensor_readings(db: Session, count: int = 100):
    """Generate mock sensor readings"""
    sensors = db.query(Sensor).all()
    
    for i in range(count):
        sensor = random.choice(sensors)
        reading = SensorReading(
            sensor_id=sensor.id,
            value=random.uniform(0, 200),
            unit=sensor.unit,
            is_alert=random.choice([True, False, False, False]),
            is_critical=random.choice([True, False, False, False, False]),
            temperature=random.uniform(20, 40),
            humidity=random.uniform(30, 80),
            pressure=random.uniform(1000, 1015),
            timestamp=datetime.utcnow() - timedelta(minutes=random.randint(0, 1440))
        )
        db.add(reading)
    
    db.commit()
    print(f"Created {count} mock sensor readings")


def generate_mock_permits(db: Session, count: int = 10):
    """Generate mock permit data"""
    workers = db.query(Worker).all()
    permit_types = list(PermitType)
    zones = ["Zone A", "Zone B", "Zone C", "Zone D"]
    
    for i in range(count):
        permit = Permit(
            permit_number=f"PERMIT-{datetime.utcnow().strftime('%Y%m%d')}-{str(i+1).zfill(4)}",
            permit_type=random.choice(permit_types),
            requested_by=random.choice(workers).id,
            location_zone=random.choice(zones),
            latitude=28.6139 + random.uniform(-0.01, 0.01),
            longitude=77.2090 + random.uniform(-0.01, 0.01),
            status=random.choice(list(PermitStatus)),
            issued_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(hours=random.randint(4, 24)),
        )
        db.add(permit)
    
    db.commit()
    print(f"Created {count} mock permits")


def generate_mock_incidents(db: Session, count: int = 5):
    """Generate mock incident data"""
    workers = db.query(Worker).all()
    zones = ["Zone A", "Zone B", "Zone C", "Zone D"]
    
    for i in range(count):
        incident = Incident(
            incident_number=f"INC-{datetime.utcnow().strftime('%Y%m%d')}-{str(i+1).zfill(4)}",
            incident_type=random.choice(list(IncidentType)),
            severity=random.choice(list(IncidentSeverity)),
            location_zone=random.choice(zones),
            latitude=28.6139 + random.uniform(-0.01, 0.01),
            longitude=77.2090 + random.uniform(-0.01, 0.01),
            description=f"Mock incident description {i+1}",
            incident_date=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
        )
        db.add(incident)
    
    db.commit()
    print(f"Created {count} mock incidents")


def generate_mock_alerts(db: Session, count: int = 15):
    """Generate mock alert data"""
    zones = ["Zone A", "Zone B", "Zone C", "Zone D"]
    
    for i in range(count):
        alert = Alert(
            alert_type=random.choice(list(AlertType)),
            severity=random.choice(list(AlertSeverity)),
            status=random.choice(list(AlertStatus)),
            title=f"Mock Alert {i+1}",
            message=f"Mock alert message for testing {i+1}",
            location_zone=random.choice(zones),
            created_at=datetime.utcnow() - timedelta(hours=random.randint(0, 72)),
        )
        db.add(alert)
    
    db.commit()
    print(f"Created {count} mock alerts")


def generate_all_mock_data():
    """Generate all mock data"""
    db = SessionLocal()
    
    try:
        # Initialize database
        init_database()
        
        # Generate mock data
        generate_mock_workers(db, 20)
        generate_mock_sensors(db, 15)
        generate_mock_sensor_readings(db, 100)
        generate_mock_permits(db, 8)
        generate_mock_incidents(db, 5)
        generate_mock_alerts(db, 15)
        
        print("\n✅ All mock data generated successfully!")
    except Exception as e:
        print(f"\n❌ Error generating mock data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    generate_all_mock_data()
