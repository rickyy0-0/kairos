import numpy as np
from typing import List, Dict, Optional, Any
from backend.models.schemas import GridCell, InterventionDetail, RecommendationItem

INTERVENTIONS_CATALOG: List[InterventionDetail] = [
    InterventionDetail(
        id="cool_roof",
        name="High-Albedo Cool Roof Coating",
        category="Surface Albedo",
        description="High solar reflectance index (SRI >= 105) elastomer coating applied to building rooftops reflecting 85%+ solar radiation.",
        unit_cost_inr=110.0,
        cost_unit="₹/m²",
        expected_cooling_c_min=1.2,
        expected_cooling_c_max=2.8,
        energy_savings_pct=16.0,
        water_impact_type="Water Conserving",
        water_consumption_liters_yr=0.0,
        co2_benefit_tonnes_yr=45.0,
        lifespan_years=7,
        maintenance_cost_annual_inr=8.0,
        implementation_difficulty="Easy",
        implementation_time_months=3
    ),
    InterventionDetail(
        id="tree_planting",
        name="Targeted Urban Tree Canopy",
        category="Vegetation & Shading",
        description="Planting mature native drought-resistant shade species along pedestrian corridors and median strips.",
        unit_cost_inr=3200.0,
        cost_unit="₹/tree",
        expected_cooling_c_min=1.5,
        expected_cooling_c_max=3.4,
        energy_savings_pct=12.0,
        water_impact_type="Irrigation Required",
        water_consumption_liters_yr=1800.0,
        co2_benefit_tonnes_yr=25.0,
        lifespan_years=30,
        maintenance_cost_annual_inr=450.0,
        implementation_difficulty="Moderate",
        implementation_time_months=6
    ),
    InterventionDetail(
        id="reflective_pavement",
        name="Reflective & High-Albedo Pavements",
        category="Surface Albedo",
        description="Application of solar-reflective light-colored aggregate surfacing to roads, parking lots, and plazas.",
        unit_cost_inr=520.0,
        cost_unit="₹/m²",
        expected_cooling_c_min=1.0,
        expected_cooling_c_max=2.4,
        energy_savings_pct=8.0,
        water_impact_type="Neutral",
        water_consumption_liters_yr=0.0,
        co2_benefit_tonnes_yr=32.0,
        lifespan_years=8,
        maintenance_cost_annual_inr=35.0,
        implementation_difficulty="Moderate",
        implementation_time_months=4
    ),
    InterventionDetail(
        id="green_roof",
        name="Extensive Vegetative Green Roofs",
        category="Green Infrastructure",
        description="Engineered lightweight vegetative roof systems with native sedum and drought-tolerant succulents.",
        unit_cost_inr=1850.0,
        cost_unit="₹/m²",
        expected_cooling_c_min=1.4,
        expected_cooling_c_max=3.0,
        energy_savings_pct=18.0,
        water_impact_type="Irrigation Required",
        water_consumption_liters_yr=650.0,
        co2_benefit_tonnes_yr=60.0,
        lifespan_years=20,
        maintenance_cost_annual_inr=120.0,
        implementation_difficulty="Complex",
        implementation_time_months=8
    ),
    InterventionDetail(
        id="shade_structures",
        name="Solar Canopy & Tensile Shade Structures",
        category="Engineered Shading",
        description="High-density tensile fabric canopies and solar PV pergolas over bus stops, market corridors, and walkways.",
        unit_cost_inr=48000.0,
        cost_unit="₹/unit (30m²)",
        expected_cooling_c_min=1.8,
        expected_cooling_c_max=3.8,
        energy_savings_pct=14.0,
        water_impact_type="Neutral",
        water_consumption_liters_yr=0.0,
        co2_benefit_tonnes_yr=40.0,
        lifespan_years=15,
        maintenance_cost_annual_inr=2400.0,
        implementation_difficulty="Easy",
        implementation_time_months=2
    ),
    InterventionDetail(
        id="urban_forest",
        name="Miyawaki Dense Urban Micro-Forest",
        category="Green Infrastructure",
        description="Ultra-dense native afforestation in vacant urban plots creating multi-layered microclimate cooling sanctuaries.",
        unit_cost_inr=1400.0,
        cost_unit="₹/m²",
        expected_cooling_c_min=2.2,
        expected_cooling_c_max=4.5,
        energy_savings_pct=15.0,
        water_impact_type="Irrigation Required",
        water_consumption_liters_yr=1200.0,
        co2_benefit_tonnes_yr=95.0,
        lifespan_years=40,
        maintenance_cost_annual_inr=80.0,
        implementation_difficulty="Moderate",
        implementation_time_months=12
    ),
    InterventionDetail(
        id="permeable_pavement",
        name="Permeable Pervious Interlocking Pavements",
        category="Water & Surface",
        description="Porous concrete and cellular grass pavers allowing stormwater infiltration and evaporative cooling.",
        unit_cost_inr=950.0,
        cost_unit="₹/m²",
        expected_cooling_c_min=0.8,
        expected_cooling_c_max=2.0,
        energy_savings_pct=5.0,
        water_impact_type="Water Conserving",
        water_consumption_liters_yr=0.0,
        co2_benefit_tonnes_yr=20.0,
        lifespan_years=15,
        maintenance_cost_annual_inr=40.0,
        implementation_difficulty="Moderate",
        implementation_time_months=5
    ),
    InterventionDetail(
        id="pocket_parks",
        name="Micro-Pocket Parks with Shade Groves",
        category="Green Infrastructure",
        description="Transforming underutilized street corners into shaded neighborhood parks with permeable seating and trees.",
        unit_cost_inr=750000.0,
        cost_unit="₹/park (500m²)",
        expected_cooling_c_min=1.6,
        expected_cooling_c_max=3.5,
        energy_savings_pct=11.0,
        water_impact_type="Irrigation Required",
        water_consumption_liters_yr=24000.0,
        co2_benefit_tonnes_yr=35.0,
        lifespan_years=25,
        maintenance_cost_annual_inr=35000.0,
        implementation_difficulty="Moderate",
        implementation_time_months=6
    ),
    InterventionDetail(
        id="solar_shading",
        name="Solar PV Rooftop & Parking Pergolas",
        category="Engineered Shading",
        description="Photovoltaic canopies delivering dual benefit: renewable energy generation and surface solar shielding.",
        unit_cost_inr=4200.0,
        cost_unit="₹/m²",
        expected_cooling_c_min=1.5,
        expected_cooling_c_max=3.2,
        energy_savings_pct=28.0,
        water_impact_type="Neutral",
        water_consumption_liters_yr=0.0,
        co2_benefit_tonnes_yr=140.0,
        lifespan_years=25,
        maintenance_cost_annual_inr=150.0,
        implementation_difficulty="Moderate",
        implementation_time_months=4
    )
]

def generate_recommendations(cell: GridCell, city_profile: Optional[Dict[str, Any]] = None) -> List[RecommendationItem]:
    """
    Ranks interventions tailored to a specific spatial zone and climate context:
    - Penalizes water-intensive landscaping in water-stressed locations (e.g. Jaipur, Chennai)
    - Prioritizes cool roofs in dense commercial zones with large flat roofs
    - Prioritizes shade structures in dense pedestrian/transit corridors with high outdoor workers
    """
    water_stress = float(city_profile.get("water_stress_index", 65.0)) if city_profile else 65.0
    tariff = float(city_profile.get("electricity_tariff_inr", 8.20)) if city_profile else 8.20
    
    scored_items = []
    roof_avail = cell.roof_area_sqm
    pavement_avail = cell.pavement_area_sqm
    open_space_avail = cell.open_space_sqm
    
    for item in INTERVENTIONS_CATALOG:
        water_penalty = 0.0
        if item.water_impact_type == "Irrigation Required" and water_stress >= 75.0:
            water_penalty = (water_stress - 70.0) * 0.4
            
        if item.id == "cool_roof":
            scale_area = roof_avail * 0.45
            est_cost = scale_area * item.unit_cost_inr
            scale_desc = f"{int(scale_area):,} m² high-albedo roof coating ({int(scale_area/500)} buildings)"
            cooling_est = 2.1
            energy_kwh = (cell.population * 140.0) * 0.16 * 12.0
            savings_inr = energy_kwh * tariff
            co2_kg = (energy_kwh / 1000.0) * 850.0
            water_liters = -(energy_kwh * 1.85)
            reason = f"High roof surface area ({int(roof_avail):,} m²) with {cell.building_density_pct}% built density provides immediate passive cooling with zero water footprint."
            feasibility = 94.0
            suitability_boost = (cell.building_density_pct / 100.0) * 26.0
            
        elif item.id == "tree_planting":
            tree_count = int(min(open_space_avail / 40.0, 1200))
            est_cost = tree_count * item.unit_cost_inr
            scale_desc = f"{tree_count:,} native shade trees along pedestrian walkways"
            cooling_est = 2.4
            energy_kwh = (cell.population * 95.0) * 0.12 * 12.0
            savings_inr = energy_kwh * tariff
            co2_kg = tree_count * 22.0
            water_liters = tree_count * 1800.0
            reason = f"Vegetation deficit ({cell.vegetation_pct}% current canopy) makes native urban afforestation essential for long-term microclimate humidity buffer."
            feasibility = 82.0
            suitability_boost = (1.0 - cell.vegetation_pct / 70.0) * 28.0 - water_penalty
            
        elif item.id == "reflective_pavement":
            scale_area = pavement_avail * 0.35
            est_cost = scale_area * item.unit_cost_inr
            scale_desc = f"{int(scale_area):,} m² reflective pavement coating"
            cooling_est = 1.7
            energy_kwh = (cell.population * 60.0) * 0.08 * 12.0
            savings_inr = energy_kwh * tariff
            co2_kg = (energy_kwh / 1000.0) * 850.0
            water_liters = 0.0
            reason = f"Zone contains {cell.road_asphalt_pct}% asphalt cover; high solar reflectance suppresses daytime sensible heat re-radiation."
            feasibility = 86.0
            suitability_boost = (cell.road_asphalt_pct / 50.0) * 24.0
            
        elif item.id == "shade_structures":
            units = int(min(cell.population / 2500, 35))
            units = max(units, 8)
            est_cost = units * item.unit_cost_inr
            scale_desc = f"{units} tensile shade structures / solar transit canopies"
            cooling_est = 2.8
            energy_kwh = (cell.population * 80.0) * 0.14 * 12.0
            savings_inr = energy_kwh * tariff
            co2_kg = (energy_kwh / 1000.0) * 850.0
            water_liters = 0.0
            reason = f"High pedestrian and outdoor worker volume ({cell.outdoor_worker_pct}%) requires immediate shade shields in transit corridors."
            feasibility = 96.0
            suitability_boost = (cell.outdoor_worker_pct / 50.0) * 32.0
            
        elif item.id == "pocket_parks":
            parks = max(1, int(open_space_avail / 40000.0))
            parks = min(parks, 4)
            est_cost = parks * item.unit_cost_inr
            scale_desc = f"{parks} micro pocket park(s) (approx {parks*500} m² total)"
            cooling_est = 2.2
            energy_kwh = (cell.population * 70.0) * 0.11 * 12.0
            savings_inr = energy_kwh * tariff
            co2_kg = parks * 4500.0
            water_liters = parks * 24000.0
            reason = "Transforms open spaces into thermal cooling sinks and community heat refuges."
            feasibility = 78.0
            suitability_boost = (1.0 - cell.vegetation_pct / 60.0) * 20.0 - water_penalty
            
        else:
            scale_area = min(open_space_avail * 0.25, 5000.0)
            est_cost = scale_area * item.unit_cost_inr
            scale_desc = f"{int(scale_area):,} m² implementation area"
            cooling_est = (item.expected_cooling_c_min + item.expected_cooling_c_max) / 2.0
            energy_kwh = (cell.population * 50.0) * 0.08 * 12.0
            savings_inr = energy_kwh * tariff
            co2_kg = (energy_kwh / 1000.0) * 850.0
            water_liters = 0.0
            reason = f"{item.description}"
            feasibility = 75.0
            suitability_boost = 10.0 - water_penalty
            
        if savings_inr > 0 and est_cost > 0:
            payback_years = round(est_cost / savings_inr, 1)
            if payback_years <= 12.0:
                payback_str = f"~{payback_years} years"
            else:
                payback_str = "Long-term resilience benefit — financial payback not directly measurable"
                payback_years = None
        else:
            payback_years = None
            payback_str = "Long-term resilience benefit — financial payback not directly measurable"
            
        heat_benefit = (cooling_est / 4.0) * 30.0
        energy_benefit = min(savings_inr / 500_000.0, 1.0) * 20.0
        health_benefit = (cell.heat_severity_score / 100.0) * 20.0
        cost_penalty = min(est_cost / 15_000_000.0, 1.0) * 15.0
        
        final_score = float(np.clip(
            heat_benefit + energy_benefit + health_benefit + suitability_boost + (feasibility * 0.15) - cost_penalty,
            10.0, 99.0
        ))
        
        scored_items.append({
            "item": item,
            "reason": reason,
            "scale_desc": scale_desc,
            "cost_inr": round(est_cost, 0),
            "cooling_c": round(cooling_est, 1),
            "energy_kwh": round(energy_kwh, 0),
            "savings_inr": round(savings_inr, 0),
            "water_liters": round(water_liters, 0),
            "co2_kg": round(co2_kg, 0),
            "timeframe": f"{item.implementation_time_months} months",
            "payback_years": payback_years,
            "payback_str": payback_str,
            "confidence": "High" if cell.data_completeness >= 90 else "Medium",
            "score": round(final_score, 1)
        })
        
    scored_items.sort(key=lambda x: x["score"], reverse=True)
    
    top_recommendations = []
    for rank, entry in enumerate(scored_items[:3], start=1):
        top_recommendations.append(RecommendationItem(
            rank=rank,
            intervention_id=entry["item"].id,
            intervention_name=entry["item"].name,
            category=entry["item"].category,
            suitability_score=entry["score"],
            reason=entry["reason"],
            recommended_scale=entry["scale_desc"],
            estimated_cost_inr=entry["cost_inr"],
            estimated_cooling_impact_c=entry["cooling_c"],
            estimated_energy_savings_kwh=entry["energy_kwh"],
            annual_financial_savings_inr=entry["savings_inr"],
            estimated_water_impact_liters=entry["water_liters"],
            estimated_co2_reduction_kg=entry["co2_kg"],
            implementation_time=entry["timeframe"],
            payback_period_years=entry["payback_years"],
            payback_display=entry["payback_str"],
            confidence_level=entry["confidence"],
            recommendation_score=entry["score"]
        ))
        
    return top_recommendations
