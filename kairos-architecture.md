# KAIROS Architecture

This document contains two Mermaid diagrams based on the repository's visible files and the imports/API routes in `main.py`. It describes the architecture represented by the current code; it does not imply that every external dataset or model is independently validated.

## 1. System architecture

```mermaid
flowchart TD
    U[User] --> UI[React + TypeScript + Vite frontend]
    UI --> API[FastAPI application]

    subgraph INPUTS[Data and location inputs]
        W[Open-Meteo live weather]
        G[Geocoding and location search]
        P[City profiles and spatial grid]
        S[Source registry and supporting datasets]
    end

    API --> W
    API --> G
    API --> P
    API --> S

    subgraph CORE[Urban heat intelligence engines]
        H[Heat engine]
        C[Cause analysis engine]
        I[Impact analysis engine]
        R[Intervention recommendation engine]
        SIM[Intervention simulation engine]
        O[Budget optimization engine]
        CMP[City comparison engine]
        A[AI assistant]
    end

    P --> H
    W --> H
    H --> C
    H --> I
    H --> R
    H --> SIM
    H --> O
    H --> CMP
    H --> A

    C --> OUT[Structured API responses]
    I --> OUT
    R --> OUT
    SIM --> OUT
    O --> OUT
    CMP --> OUT
    A --> OUT
    H --> OUT

    OUT --> UI
    UI --> DASH[Maps, charts, city and hotspot dashboards]
    UI --> DEC[Scenario simulation and decision support]
```

## 2. Code architecture

```mermaid
flowchart TB
    subgraph FRONTEND[Frontend]
        REACT[React 19 + TypeScript]
        VITE[Vite development and build]
        MAP[Leaflet / React-Leaflet maps]
        CHART[Recharts visualizations]
        REACT --> MAP
        REACT --> CHART
        VITE --> REACT
    end

    subgraph BACKEND[Backend]
        MAIN[main.py — FastAPI routes and orchestration]

        subgraph DATA[Data and domain modules]
            SCHEMA[schemas.py — request and response models]
            LOC[location_registry.py]
            CITY[city_generator.py]
            SRC[source_registry.py]
            WATER[water_db.py]
            ENERGY[state_electricity_db.py]
        end

        subgraph SERVICES[Service and analysis modules]
            WEATHER[weather_service.py]
            GEO[geocoding_service.py]
            HEAT[heat_engine.py]
            CAUSE[cause_engine.py]
            IMPACT[impact_engine.py]
            INTERVENTION[intervention_engine.py]
            SIMULATION[simulation_engine.py]
            OPTIMIZER[optimizer_engine.py]
            COMPARE[comparison_engine.py]
            ASSISTANT[ai_assistant.py]
        end

        MAIN --> SCHEMA
        MAIN --> LOC
        MAIN --> CITY
        MAIN --> SRC
        MAIN --> WEATHER
        MAIN --> GEO
        MAIN --> HEAT
        MAIN --> CAUSE
        MAIN --> IMPACT
        MAIN --> INTERVENTION
        MAIN --> SIMULATION
        MAIN --> OPTIMIZER
        MAIN --> COMPARE
        MAIN --> ASSISTANT

        HEAT --> CITY
        HEAT --> LOC
        CAUSE --> HEAT
        IMPACT --> HEAT
        INTERVENTION --> HEAT
        SIMULATION --> INTERVENTION
        OPTIMIZER --> INTERVENTION
        ASSISTANT --> HEAT
        COMPARE --> HEAT
    end

    REACT <-->|HTTP / JSON API| MAIN
    WEATHER <-->|Live weather API| OPENMETEO[Open-Meteo]
    GEO <-->|Geocoding lookup| OSM[OpenStreetMap Nominatim]
```

## Main API capabilities

- Health, states, cities, location search, and geocoding
- Live weather and city profile/overview
- Hotspot grids and hotspot cause, impact, and recommendation details
- Energy, water, and heat-health overviews
- Intervention simulation and city-budget optimization
- Multi-city comparison and AI-assisted city queries
- Data-source and metric-provenance metadata

## Repository notes

- The frontend package manifest identifies React, TypeScript, Vite, Leaflet, and Recharts.
- The backend entry point is a FastAPI application in `main.py`.
- The backend entry point imports modules under `backend.models`, `backend.data`, and `backend.services`. Keep the diagram aligned with the actual package paths in the checked-out branch if those directories are reorganized.
- The current root `README.md` is still the default Vite template; replace or expand it with project-specific setup instructions and this architecture document.
