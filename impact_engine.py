import numpy as np
from typing import Dict, List, Any, Optional
from backend.models.schemas import GridCell, ImpactAnalysis

from backend.data.state_electricity_db import get_city_electricity_baseline
from backend.utils.unit_converter import (
    calculate_annual_cost_inr, calculate_annual_cost_crore, calculate_co2_tonnes_from_gwh
)

def calculate_impact_profile(cell: GridCell, city_profile: Optional[Dict[str, Any]] = None) -> ImpactAnalysis:
    """
    Calculates multi-vector impacts of extreme heat for a spatial zone:
    1. Heat-driven excess electricity demand (GWh/yr), financial cost (₹), CO2 footprint (tonnes/yr)
    2. Heat-driven water demand (Million Litres/yr) with sectoral breakdown
    3. Heat Health Vulnerability Index (0-100) and risk classification
    """
    c_id = city_profile.get("id", "city") if city_profile else "city"
    c_name = city_profile.get("name", cell.city_name) if city_profile else cell.city_name
    s_name = city_profile.get("state", cell.state_name) if city_profile else cell.state_name
    
    city_base = get_city_electricity_baseline(c_id, c_name, s_name, cell.population * 15)
    total_city_gwh = float(city_base["total_electricity_gwh"])
    tariff = float(city_base["tariff_inr_kwh"])
    grid_emission_factor = float(city_base["grid_emission_factor_kg_kwh"])
    ac_pen = float(city_base["urban_ac_penetration_pct"])
    cdd = float(city_profile.get("cooling_degree_days", 3000)) if city_profile else 3000.0
    cooling_days = int(cdd / 10.0)
    
    # 1. Calibrated Zone Excess Cooling Energy
    # Zone baseline cooling share (assuming ~15 zones per city on average)
    alpha_base = 0.16 + 0.12 * (ac_pen / 100.0) * (min(cdd, 4000.0) / 3000.0)
    zone_base_gwh = (total_city_gwh * alpha_base) * (cell.population / max(100000.0, cell.population * 15)) * (cell.cooling_access_pct / 50.0)
    
    delta_air = max(0.0, cell.air_temp_c - 28.0)
    delta_lst = max(0.0, cell.surface_temp_c - 30.0)
    delta_eff = delta_air * 0.60 + delta_lst * 0.40
    thermal_mult = min(0.50, delta_eff * 0.04)
    
    excess_energy_gwh = float(round(zone_base_gwh * thermal_mult, 2))
    excess_energy_kwh = excess_energy_gwh * 1_000_000.0
    
    annual_energy_cost_inr = calculate_annual_cost_inr(excess_energy_gwh, tariff)
    co2_tonnes_yr = calculate_co2_tonnes_from_gwh(excess_energy_gwh, grid_emission_factor)
    
    # 2. Water Wastage Model (Million Litres / year)
    water_cooling_liters = excess_energy_kwh * 1.85
    water_household_liters = cell.population * delta_air * 6.5 * (cooling_days * 0.7)
    water_landscape_liters = cell.open_space_sqm * max(0.0, delta_air - 2.0) * 0.8 * (cooling_days * 0.5)
    water_other_liters = (water_cooling_liters + water_household_liters) * 0.06
    
    total_water_liters = water_cooling_liters + water_household_liters + water_landscape_liters + water_other_liters
    heat_driven_water_ml = total_water_liters / 1_000_000.0
    
    water_breakdown = {
        "cooling_hvac_ml": round(water_cooling_liters / 1_000_000.0, 2),
        "household_surge_ml": round(water_household_liters / 1_000_000.0, 2),
        "landscape_stress_ml": round(water_landscape_liters / 1_000_000.0, 2),
        "municipal_other_ml": round(water_other_liters / 1_000_000.0, 2)
    }
    
    # 3. Heat Health Risk Model (0-100)
    norm_air = (cell.air_temp_c - 28.0) / (46.0 - 28.0)
    norm_night = (cell.night_temp_c - 25.0) / (35.0 - 25.0)
    norm_lst = (cell.surface_temp_c - 28.0) / (50.0 - 28.0)
    exposure_score = (norm_air * 0.4 + norm_night * 0.35 + norm_lst * 0.25) * 100.0
    
    sensitivity_score = (
        (cell.elderly_pct / 20.0) * 0.35 +
        (cell.child_pct / 22.0) * 0.25 +
        (cell.outdoor_worker_pct / 55.0) * 0.40
    ) * 100.0
    
    lack_of_cooling = (100.0 - cell.cooling_access_pct)
    hosp_penalty = min(cell.hospital_dist_km / 5.0, 1.0) * 100.0
    adaptive_deficit = lack_of_cooling * 0.65 + hosp_penalty * 0.35
    
    health_risk_score = float(np.clip(
        exposure_score * 0.42 + sensitivity_score * 0.33 + adaptive_deficit * 0.25,
        5.0, 99.0
    ))
    
    if health_risk_score >= 75.0:
        health_class = "Critical"
    elif health_risk_score >= 55.0:
        health_class = "High"
    elif health_risk_score >= 35.0:
        health_class = "Moderate"
    else:
        health_class = "Low"
        
    drivers = []
    if cell.surface_temp_c >= 42.0:
        drivers.append(f"Extreme land surface thermal elevation ({cell.surface_temp_c}°C)")
    if cell.night_temp_c >= 31.0:
        drivers.append(f"High nocturnal heat trapping ({cell.night_temp_c}°C) preventing physiological recovery")
    if cell.outdoor_worker_pct >= 30.0:
        drivers.append(f"High outdoor workforce concentration ({cell.outdoor_worker_pct}%)")
    if cell.cooling_access_pct <= 50.0:
        drivers.append(f"Severe cooling equity deficit ({100 - int(cell.cooling_access_pct)}% without AC access)")
    if cell.elderly_pct >= 14.0:
        drivers.append(f"High elderly demographic vulnerability ({cell.elderly_pct}%)")
    if cell.hospital_dist_km >= 2.5:
        drivers.append(f"Distance to emergency trauma / cooling centers ({cell.hospital_dist_km} km)")
    if not drivers:
        drivers.append("Moderate urban heat accumulation under standard demographic conditions")

    return ImpactAnalysis(
        zone_id=cell.id,
        zone_name=cell.name,
        city_name=cell.city_name,
        state_name=cell.state_name,
        population_exposed=cell.population,
        heat_severity_score=cell.heat_severity_score,
        excess_energy_gwh_yr=round(excess_energy_gwh, 2),
        annual_energy_cost_inr=round(annual_energy_cost_inr, 0),
        co2_emissions_tonnes_yr=round(co2_tonnes_yr, 2),
        heat_driven_water_ml_yr=round(heat_driven_water_ml, 1),
        water_breakdown=water_breakdown,
        health_risk_score=round(health_risk_score, 1),
        health_risk_class=health_class,
        vulnerability_drivers=drivers
    )
