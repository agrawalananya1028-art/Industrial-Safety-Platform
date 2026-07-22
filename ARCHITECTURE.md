# System Architecture

## Overview

The Industrial Safety Intelligence Platform follows a modern microservices-inspired architecture with real-time data processing and AI-powered decision making.

## High-Level Architecture

```
Frontend (Next.js React)
    ↓ WebSocket & REST API
API Gateway (Nginx)
    ↓
Backend Services (FastAPI)
├─ REST Routes
├─ WebSocket Handler
├─ Service Layer
├─ AI Agents (LangGraph)
│  ├─ Risk Assessment Agent
│  ├─ Permit Validation Agent
│  ├─ Compliance Agent
│  ├─ Incident Analysis Agent
│  ├─ Emergency Response Agent
│  ├─ CCTV Analysis Agent
│  └─ Coordinator Agent
├─ RAG System
│  ├─ Vector Store (FAISS)
│  ├─ Embeddings (Sentence-Transformers)
│  └─ Document Retrieval
└─ Data Access Layer
    ↓
Data Storage
├─ PostgreSQL (Primary DB)
├─ Redis (Cache & Pub/Sub)
└─ FAISS (Vector Index)
    ↓
Data Sources
├─ IoT Sensors
├─ SCADA Systems
├─ CCTV Feeds
├─ Worker Location
├─ Permits & Maintenance
└─ Historical Data
```

## Frontend Architecture

- **Next.js 14**: SSR, routing, API routes
- **React 18**: Component-based UI
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling
- **Framer Motion**: Animations
- **Recharts**: Data visualization
- **Socket.io**: Real-time updates
- **Shadcn UI**: Component library

## Backend Architecture

- **FastAPI**: REST API server
- **SQLAlchemy**: ORM for database
- **Pydantic**: Data validation
- **LangGraph**: AI agent orchestration
- **CrewAI**: Multi-agent framework
- **OpenAI APIs**: LLM and embeddings

## AI Agent System (LangGraph)

```
Coordinator Agent (Master)
├─ Risk Assessment Agent
│  ├─ Sensor Analysis
│  ├─ Historical Patterns
│  ├─ Weather Data
│  └─ Location Context
├─ Permit Validation Agent
│  ├─ Permit Type Validation
│  ├─ Worker Status Check
│  ├─ Location Verification
│  └─ Safety Condition Review
├─ Compliance Agent
│  ├─ Audit Trail Review
│  ├─ Documentation Check
│  ├─ Certification Verification
│  └─ Regulation Compliance
├─ Incident Analysis Agent
│  ├─ Pattern Matching (RAG)
│  ├─ Similar Incident Retrieval
│  ├─ Root Cause Analysis
│  └─ Prevention Recommendations
├─ Emergency Response Agent
│  ├─ Alarm Triggering
│  ├─ Notification Dispatch
│  ├─ Evacuation Coordination
│  └─ Report Generation
├─ CCTV Analysis Agent
│  ├─ Frame Processing
│  ├─ Object Detection
│  ├─ PPE Verification
│  └─ Violation Alerting
└─ Chatbot Agent
   ├─ Query Processing
   ├─ Context Retrieval
   ├─ Response Generation
   └─ Follow-up Handling
```

## Data Flow

### Real-time Pipeline
1. Sensors → Data Ingestion
2. Validation & Transformation
3. Redis Stream Queue
4. Real-time Processing
5. Risk Assessment
6. Alert Generation
7. WebSocket Broadcast
8. Frontend Updates (<500ms)

### Batch Pipeline
1. PostgreSQL Data Lake
2. Batch Jobs (6-hour intervals)
3. Aggregations & Analytics
4. Pattern Mining
5. Trend Analysis
6. Predictive Models
7. Analytics Dashboard

## Database Schema (Key Tables)

- `workers` - Employee information
- `sensors` - IoT sensor metadata
- `sensor_readings` - Time-series data
- `machines` - Equipment inventory
- `permits` - Work permits
- `incidents` - Accident reports
- `alerts` - Generated alerts
- `risk_assessments` - Risk history
- `compliance_records` - Audit trail
- `incident_patterns` - RAG data (pgvector)

## Security

- JWT authentication
- Role-based access control (RBAC)
- AES-256 encryption at rest
- TLS 1.3 in transit
- Field-level encryption for sensitive data
- Audit logging for all operations

## Performance Targets

- Dashboard updates: <500ms
- Risk assessment: <2s
- Alert generation: <3s
- API response: <200ms average
- Concurrent users: 500+
- Sensor readings: 100,000+/minute
- Uptime SLA: 99.9%

## Deployment

- **Development**: Docker Compose (all-in-one)
- **Production**: Kubernetes cluster with HA
- **Monitoring**: Prometheus + Grafana
- **Backup**: Daily + WAL archiving
- **DR**: RTO <1h, RPO <15min
