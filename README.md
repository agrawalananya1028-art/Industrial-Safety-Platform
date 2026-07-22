# AI-Powered Industrial Safety Intelligence Platform

A production-ready, real-time industrial safety monitoring and prediction system that combines IoT sensor data, CCTV analytics, worker location tracking, and AI-powered risk assessment to prevent industrial accidents before they happen.

## Overview

This platform implements a comprehensive zero-harm operations strategy for industrial facilities by:

- **Real-time Monitoring**: Aggregates data from 100+ IoT sensors, SCADA systems, and CCTV feeds
- **Compound Risk Detection**: Uses multi-agent AI to identify dangerous situations that individual sensors cannot detect
- **Predictive Analytics**: Forecasts critical incidents 30 minutes in advance
- **Intelligent Permit Management**: AI-powered approval/rejection of work permits based on real-time conditions
- **Compliance Automation**: Continuous monitoring of regulatory compliance (OISD, DGMS, Factory Act)
- **Emergency Orchestration**: Automated response workflows for critical incidents
- **Advanced Analytics**: Historical incident analysis, trend prediction, and root cause analysis

## Key Features

### 1. Smart Dashboard
- Real-time KPIs (workers online, sensor status, gas readings, alerts)
- Live risk assessment and scoring
- Active permits and maintenance tasks
- Incident counter and historical trends

### 2. Compound Risk Detection Engine
- Analyzes 12+ data signals simultaneously
- Risk levels: Safe, Medium, High, Critical
- Explainable AI reasoning for each alert
- Contextual action recommendations

### 3. Geospatial Safety Heatmap
- Plant layout visualization with worker positions
- Real-time movement tracking
- Restricted zones, equipment, and hazard areas
- Color-coded risk visualization (Green→Yellow→Orange→Red)

### 4. CCTV AI Analytics
- Detects: Missing PPE, restricted area violations, fire, smoke, crowds, worker collapse
- Snapshot capture and alerting
- Multi-camera coordination

### 5. Digital Permit Intelligence Agent
- Validates: Hot Work, Confined Space, Electrical, Height Work, Isolation
- Real-time permit approval/rejection
- Explains unsafe conditions

### 6. Incident Pattern Intelligence
- RAG-based historical incident analysis
- Similar incident matching
- Regulatory mapping
- Preventive recommendations

### 7. Emergency Response Orchestrator
- Automated multi-channel alerts
- Evacuation coordination
- Incident report generation
- Timeline preservation

### 8. Compliance Monitoring
- Continuous audit trails
- Documentation tracking
- Certification management
- Compliance scoring

### 9. AI Safety Chatbot
- Natural language Q&A
- Alert explanation
- Incident history queries
- Regulatory guidance

### 10. Advanced Analytics
- Incident trends
- Risk heatmaps
- Department analysis
- Predictive forecasting

## Tech Stack

### Frontend
- React 18 with TypeScript
- Next.js 14 for SSR
- Tailwind CSS
- Framer Motion
- Recharts
- Leaflet/Mapbox
- Shadcn UI

### Backend
- FastAPI (Python)
- LangGraph for multi-agent orchestration
- CrewAI
- OpenAI APIs
- Sentence Transformers
- FAISS

### Database
- PostgreSQL
- Redis
- pgvector

### DevOps
- Docker & Docker Compose
- Nginx
- Prometheus & Grafana

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- OpenAI API Key

### Installation

```bash
# Clone repository
git clone https://github.com/agrawalananya1028-art/Industrial-Safety-Platform.git
cd Industrial-Safety-Platform

# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Start with Docker Compose
docker-compose up -d

# Initialize database
docker-compose exec backend python -m alembic upgrade head

# Load mock data
docker-compose exec backend python -m app.data.mock_data_generator
```

### Access Points
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Grafana: http://localhost:3001
- Prometheus: http://localhost:9090

## Project Structure

```
Industrial-Safety-Platform/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── schemas/
│   │   ├── models/
│   │   ├── api/
│   │   ├── services/
│   │   ├── agents/
│   │   ├── rag/
│   │   └── utils/
│   ├── data/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── styles/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── database/
├── docs/
├── docker-compose.yml
├── ARCHITECTURE.md
└── README.md
```

## Documentation

- [Architecture](ARCHITECTURE.md)
- [API Documentation](docs/API.md)
- [Installation Guide](docs/INSTALLATION.md)
- [Demo Script](docs/DEMO.md)

## License

Proprietary - Industrial Safety Intelligence Platform

## Version

v1.0.0 - Production Ready
