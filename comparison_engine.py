from typing import List, Dict, Any
from backend.models.schemas import CityComparisonMetric, CityComparisonResponse, GridCell
from backend.data.location_registry import get_or_generate_city_profile
from backend.data.city_generator import generate_city_grid
from backend.services.heat_engine import compute_city_overview
from backend.services.cause_engine import calculate_cause_profile

def compare_cities(city_ids: List[str]) -> CityComparisonResponse:
    """
    Compares 2 to 4 Indian cities across heat severity, energy demand, water stress,
    vulnerable population, and climate resilience.
    """
    metrics_list: List[CityComparisonMetric] = []
    
    # Cache grids during comparison
    for cid in city_ids[:4]:  # limit to max 4
        profile = get_or_generate_city_profile(cid)
        cells = generate_city_grid(city_profile=profile)
        overview = compute_city_overview(cells, city_profile=profile)
        
        # Calculate primary heat driver for the city from top severe zone or overall avg
        severe_cells = [c for c in cells if c.heat_classification in ["Extreme Hotspot", "Severe Hotspot"]]
        primary_driver = "Impervious Surface & Albedo"
        if severe_cells:
            cause_res = calculate_cause_profile(severe_cells[0])
            primary_driver = cause_res.dominant_cause
            
        avg_veg = round(float(sum(c.vegetation_pct for c in cells) / len(cells)), 1)
        avg_imp = round(float(sum(c.impervious_pct for c in cells) / len(cells)), 1)
        avg_health = round(float(sum(c.heat_severity_score * (1.0 + c.elderly_pct/100.0) for c in cells) / len(cells)), 1)
        
        # Estimated city-wide intervention need (₹ Cr) based on hotspots
        est_need_cr = round((overview.hotspots_count * 2.8) + (overview.severe_hotspots_count * 4.5), 1)
        
        metrics_list.append(CityComparisonMetric(
            city_id=profile["id"],
            city_name=profile["name"],
            state_name=profile["state"],
            climate_zone=profile["climate_zone"],
            avg_temperature_c=overview.city_avg_temperature_c,
            max_surface_temp_c=overview.city_max_temperature_c,
            hotspots_count=overview.hotspots_count,
            severe_hotspots_count=overview.severe_hotspots_count,
            people_exposed=overview.people_exposed_high_risk,
            avg_vegetation_pct=avg_veg,
            avg_impervious_pct=avg_imp,
            excess_energy_gwh_yr=overview.excess_electricity_gwh_yr,
            annual_cooling_cost_cr=round(overview.annual_cooling_cost_inr / 1e7, 2),
            water_stress_index=overview.water_stress_score,
            excess_water_ml_yr=overview.excess_water_ml_yr,
            avg_health_risk_score=min(100.0, avg_health),
            city_resilience_score=overview.city_resilience_score,
            estimated_intervention_need_cr=est_need_cr,
            primary_heat_driver=primary_driver
        ))
        
    # Generate comparative narrative and differentiators
    if len(metrics_list) == 0:
        return CityComparisonResponse(
            cities=[],
            comparative_ai_insight="No cities selected for comparison.",
            key_differentiators=[]
        )
        
    # Sort cities by heat severity
    sorted_by_heat = sorted(metrics_list, key=lambda x: x.avg_temperature_c, reverse=True)
    hottest = sorted_by_heat[0]
    coolest = sorted_by_heat[-1]
    
    # Sort by water stress
    sorted_by_water = sorted(metrics_list, key=lambda x: x.water_stress_index, reverse=True)
    driest = sorted_by_water[0]
    
    # Sort by resilience
    sorted_by_res = sorted(metrics_list, key=lambda x: x.city_resilience_score)
    least_resilient = sorted_by_res[0]
    
    insight = (
        f"Cross-city climate analysis across {len(metrics_list)} metropolitan regions reveals substantial microclimate divergence. "
        f"**{hottest.city_name}** ({hottest.state_name}) exhibits the highest thermal burden with an average temperature of {hottest.avg_temperature_c}°C "
        f"and {hottest.severe_hotspots_count} critical zones, primarily driven by {hottest.primary_heat_driver}. "
        f"In contrast, **{coolest.city_name}** experiences relatively lower baseline temperatures ({coolest.avg_temperature_c}°C) but requires targeted albedo management. "
        f"From a water-energy nexus perspective, **{driest.city_name}** faces severe water constraints (Stress Index: {driest.water_stress_index}/100), "
        f"meaning active misting and high-irrigation urban forestry will exacerbate water depletion. Instead, cool roofs and shade structures provide higher net resilience ROI. "
        f"Overall, **{least_resilient.city_name}** requires the most urgent capital deployment (estimated ₹{least_resilient.estimated_intervention_need_cr} Cr) to protect its {least_resilient.people_exposed:,} highly exposed citizens."
    )
    
    differentiators = [
        f"Thermal Contrast: {hottest.city_name} is {round(hottest.avg_temperature_c - coolest.avg_temperature_c, 1)}°C hotter than {coolest.city_name} on average.",
        f"Energy Burden: {sorted_by_heat[0].city_name} incurs ₹{sorted_by_heat[0].annual_cooling_cost_cr} Cr/yr in excess AC electricity costs.",
        f"Water Constraints: {driest.city_name} requires dry/albedo cooling interventions rather than water-intensive evaporative solutions.",
        f"Vulnerability Footprint: Combined population exposed to severe heat across these regions is {sum(m.people_exposed for m in metrics_list):,} citizens."
    ]
    
    return CityComparisonResponse(
        cities=metrics_list,
        comparative_ai_insight=insight,
        key_differentiators=differentiators
    )
