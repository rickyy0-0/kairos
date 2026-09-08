import numpy as np
from typing import List, Dict, Any, Optional
from backend.models.schemas import GridCell, CauseAnalysis, CauseItem

def calculate_cause_profile(cell: GridCell, city_cells: Optional[List[GridCell]] = None) -> CauseAnalysis:
    """
    Computes the 6-factor Cause Contribution Profile for a spatial cell and compares
    it directly with the city-wide averages.
    
    1. Excess asphalt & concrete
    2. Low vegetation & canopy deficit
    3. Building density & low ventilation
    4. Anthropogenic & traffic emissions
    5. Low soil moisture & water scarcity
    6. Poor nighttime thermal release
    """
    c_asphalt = (cell.impervious_pct / 100.0) * 0.65 + (cell.road_asphalt_pct / 50.0) * 0.35
    veg_deficit = max(0.0, 1.0 - (cell.vegetation_pct / 60.0))
    ndvi_deficit = max(0.0, 1.0 - max(0.0, cell.ndvi) / 0.7)
    c_vegetation = veg_deficit * 0.6 + ndvi_deficit * 0.4
    c_buildings = (cell.building_density_pct / 100.0) * 0.75 + (1.0 - min(cell.open_space_sqm / (cell.area_sqm * 0.3), 1.0)) * 0.25
    c_traffic = (cell.traffic_intensity / 100.0) * 0.7 + (cell.population / 35000.0) * 0.3
    c_water = max(0.0, 1.0 - (cell.soil_moisture_pct / 50.0))
    night_retention = max(0.0, (cell.night_temp_c - 25.0) / (34.0 - 25.0))
    c_night = night_retention * (cell.building_density_pct / 100.0)

    weights = [0.30, 0.28, 0.18, 0.10, 0.08, 0.06]
    raw_scores = [
        c_asphalt * weights[0],
        c_vegetation * weights[1],
        c_buildings * weights[2],
        c_traffic * weights[3],
        c_water * weights[4],
        c_night * weights[5]
    ]
    
    total_raw = sum(raw_scores) if sum(raw_scores) > 0 else 1.0
    percentages = [(s / total_raw) * 100.0 for s in raw_scores]
    
    rounded_pcts = [round(p, 1) for p in percentages]
    diff = round(100.0 - sum(rounded_pcts), 1)
    max_idx = int(np.argmax(rounded_pcts))
    rounded_pcts[max_idx] = round(rounded_pcts[max_idx] + diff, 1)

    causes: List[CauseItem] = [
        CauseItem(
            id="cause_asphalt",
            name="Excess asphalt & concrete",
            percentage=rounded_pcts[0],
            contribution_score=round(raw_scores[0], 3),
            indicator_description=f"Impervious cover ({cell.impervious_pct}%), Road surface ({cell.road_asphalt_pct}%)",
            evidence_text="High thermal mass of paved surfaces absorbing shortwave solar radiation and re-radiating sensible heat."
        ),
        CauseItem(
            id="cause_vegetation",
            name="Low vegetation & canopy deficit",
            percentage=rounded_pcts[1],
            contribution_score=round(raw_scores[1], 3),
            indicator_description=f"Canopy cover ({cell.vegetation_pct}%), NDVI ({cell.ndvi})",
            evidence_text="Severe evaporative cooling deficit; insufficient shading over artificial surfaces."
        ),
        CauseItem(
            id="cause_buildings",
            name="Building density & low ventilation",
            percentage=rounded_pcts[2],
            contribution_score=round(raw_scores[2], 3),
            indicator_description=f"Built density ({cell.building_density_pct}%), Sky view factor constrained",
            evidence_text="Dense multi-story structures creating urban street canyons that trap radiative heat and restrict wind flow."
        ),
        CauseItem(
            id="cause_traffic",
            name="Anthropogenic & traffic emissions",
            percentage=rounded_pcts[3],
            contribution_score=round(raw_scores[3], 3),
            indicator_description=f"Traffic score ({cell.traffic_intensity}/100), HVAC rejection",
            evidence_text="Direct thermal rejection from vehicular congestion and concentrated air conditioning condenser units."
        ),
        CauseItem(
            id="cause_water",
            name="Low soil moisture & water scarcity",
            percentage=rounded_pcts[4],
            contribution_score=round(raw_scores[4], 3),
            indicator_description=f"Soil moisture ({cell.soil_moisture_pct}%)",
            evidence_text="Dry surface conditions limiting latent heat flux and natural soil transpiration."
        ),
        CauseItem(
            id="cause_night",
            name="Poor nighttime thermal release",
            percentage=rounded_pcts[5],
            contribution_score=round(raw_scores[5], 3),
            indicator_description=f"Night LST ({cell.night_temp_c}°C)",
            evidence_text="Slow release of stored thermal energy from masonry, preventing nocturnal cooling."
        )
    ]
    
    causes.sort(key=lambda c: c.percentage, reverse=True)
    top_cause = causes[0]
    second_cause = causes[1]
    
    # Calculate differentials against city averages if city cells provided
    if city_cells and len(city_cells) > 0:
        city_avg_veg = round(float(np.mean([c.vegetation_pct for c in city_cells])), 1)
        city_avg_imp = round(float(np.mean([c.impervious_pct for c in city_cells])), 1)
        city_avg_lst = round(float(np.mean([c.surface_temp_c for c in city_cells])), 1)
        city_avg_bld = round(float(np.mean([c.building_density_pct for c in city_cells])), 1)
    else:
        city_avg_veg = 18.0
        city_avg_imp = 72.0
        city_avg_lst = 40.0
        city_avg_bld = 70.0
        
    zone_vs_city = {
        "zone_vegetation_pct": cell.vegetation_pct,
        "city_avg_vegetation_pct": city_avg_veg,
        "vegetation_diff": round(cell.vegetation_pct - city_avg_veg, 1),
        
        "zone_impervious_pct": cell.impervious_pct,
        "city_avg_impervious_pct": city_avg_imp,
        "impervious_diff": round(cell.impervious_pct - city_avg_imp, 1),
        
        "zone_lst_c": cell.surface_temp_c,
        "city_avg_lst_c": city_avg_lst,
        "lst_diff": round(cell.surface_temp_c - city_avg_lst, 1),
        
        "zone_building_pct": cell.building_density_pct,
        "city_avg_building_pct": city_avg_bld,
        "building_diff": round(cell.building_density_pct - city_avg_bld, 1)
    }

    narrative = (
        f"The strongest modeled contributor in {cell.name} is {top_cause.name.lower()} ({top_cause.percentage}%) "
        f"along with {second_cause.name.lower()} ({second_cause.percentage}%). "
        f"This zone exhibits {cell.impervious_pct}% impervious surface (City avg: {city_avg_imp}%) "
        f"and {cell.vegetation_pct}% vegetation cover (City avg: {city_avg_veg}%), creating pronounced localized heat retention."
    )
    
    return CauseAnalysis(
        zone_id=cell.id,
        zone_name=cell.name,
        city_name=cell.city_name,
        state_name=cell.state_name,
        dominant_cause=top_cause.name,
        causes=causes,
        zone_vs_city=zone_vs_city,
        qualitative_narrative=narrative,
        confidence_level=cell.confidence_level,
        data_completeness=cell.data_completeness
    )
