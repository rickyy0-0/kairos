import numpy as np
from typing import Optional, Dict, Any
from backend.models.schemas import GridCell, SimulationInput, SimulationOutput
from backend.data.state_electricity_db import get_city_electricity_baseline
from backend.utils.unit_converter import calculate_annual_cost_inr

def simulate_interventions(cell: GridCell, params: SimulationInput, city_profile: Optional[Dict[str, Any]] = None) -> SimulationOutput:
    """
    Deterministically simulates the thermodynamic and socioeconomic impact of user-selected
    intervention levels for any specific spatial zone in India.
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
    
    # 1. Physics-based Temperature Reduction Model (°C)
    delta_t_tree = params.tree_coverage * 4.2
    delta_t_cool_roof = params.cool_roof_coverage * 2.8
    delta_t_refl_pave = params.reflective_pavement * 2.2
    delta_t_green_roof = params.green_roof * 3.4
    delta_t_shade = params.shade_structures * 1.9
    
    raw_delta_t = delta_t_tree + delta_t_cool_roof + delta_t_refl_pave + delta_t_green_roof + delta_t_shade
    total_delta_t = float(round(-1.0 * (1.0 - np.exp(-raw_delta_t / 3.8)) * 4.8, 2))
    
    new_surface_temp = round(max(24.0, cell.surface_temp_c + total_delta_t), 1)
    
    # 2. Heat Severity Score Delta
    heat_score_reduction = round(abs(total_delta_t) * 11.2 + (params.tree_coverage * 15.0) + (params.cool_roof_coverage * 8.0), 1)
    new_heat_score = round(max(5.0, cell.heat_severity_score - heat_score_reduction), 1)
    
    # 3. Financial Costs
    roof_area = cell.roof_area_sqm
    pave_area = cell.pavement_area_sqm
    
    cost_trees = (params.tree_coverage * (cell.open_space_sqm / 35.0)) * 3200.0
    cost_cool_roof = (params.cool_roof_coverage * roof_area) * 110.0
    cost_refl_pave = (params.reflective_pavement * pave_area) * 520.0
    cost_green_roof = (params.green_roof * roof_area) * 1850.0
    cost_shade = (params.shade_structures * (cell.population / 2000.0)) * 48000.0
    
    total_impl_cost = float(round(cost_trees + cost_cool_roof + cost_refl_pave + cost_green_roof + cost_shade, 0))
    
    maint_trees = cost_trees * 0.12
    maint_cool_roof = cost_cool_roof * 0.07
    maint_refl_pave = cost_refl_pave * 0.06
    maint_green_roof = cost_green_roof * 0.08
    maint_shade = cost_shade * 0.05
    total_maint_cost = float(round(maint_trees + maint_cool_roof + maint_refl_pave + maint_green_roof + maint_shade, 0))
    
    # 4. Energy Savings (kWh / year)
    alpha_base = 0.16 + 0.12 * (ac_pen / 100.0) * (min(cdd, 4000.0) / 3000.0)
    zone_base_gwh = (total_city_gwh * alpha_base) * (cell.population / max(100000.0, cell.population * 15)) * (cell.cooling_access_pct / 50.0)
    delta_eff = max(0.0, cell.air_temp_c - 28.0) * 0.60 + max(0.0, cell.surface_temp_c - 30.0) * 0.40
    zone_excess_gwh = zone_base_gwh * min(0.50, delta_eff * 0.04)
    zone_excess_kwh = zone_excess_gwh * 1_000_000.0
    
    energy_savings_pct = min(65.0, (abs(total_delta_t) / max(1.0, delta_eff)) * 50.0) if delta_eff > 0 else 10.0
    energy_savings_kwh = float(round(zone_excess_kwh * (energy_savings_pct / 100.0), 0))
    energy_savings_gwh = energy_savings_kwh / 1_000_000.0
    
    annual_financial_savings = float(round(calculate_annual_cost_inr(energy_savings_gwh, tariff), 0))
    co2_reduction_kg = float(round((energy_savings_kwh / 1000.0) * (grid_emission_factor * 1000.0) + (params.tree_coverage * 12000.0), 0))
    
    # 5. Water Balance Delta (Liters / year)
    water_saved_cooling = energy_savings_kwh * 1.85
    water_consumed_trees = (params.tree_coverage * (cell.open_space_sqm / 35.0)) * 1800.0
    water_consumed_green_roof = (params.green_roof * roof_area) * 650.0
    net_water_change = float(round(-water_saved_cooling + water_consumed_trees + water_consumed_green_roof, 0))
    
    # 6. People Protected and Health Risk Improvement
    pop_protected = int(round(cell.population * (abs(total_delta_t) / 4.5) * 0.85))
    pop_protected = min(cell.population, pop_protected)
    
    health_risk_delta = round(-1.0 * (abs(total_delta_t) * 9.5 + (params.shade_structures * 12.0) + (params.tree_coverage * 10.0)), 1)
    new_health_risk_score = float(np.clip(cell.heat_severity_score + health_risk_delta, 10.0, 99.0))
    
    # 7. Payback calculation
    if annual_financial_savings > 0 and total_impl_cost > 0:
        payback_years = round(total_impl_cost / annual_financial_savings, 1)
        if payback_years <= 15.0:
            payback_str = f"~{payback_years} years"
        else:
            payback_str = "Long-term resilience benefit — financial payback not directly measurable"
            payback_years = None
    else:
        payback_years = None
        payback_str = "Long-term resilience benefit — financial payback not directly measurable"
        
    return SimulationOutput(
        zone_id=cell.id,
        zone_name=cell.name,
        city_name=cell.city_name,
        temperature_change_c=total_delta_t,
        new_temperature_c=new_surface_temp,
        heat_score_change=-heat_score_reduction,
        new_heat_score=new_heat_score,
        energy_savings_kwh=energy_savings_kwh,
        energy_savings_pct=round(energy_savings_pct, 1),
        annual_financial_savings_inr=annual_financial_savings,
        water_change_liters=net_water_change,
        co2_reduction_kg=co2_reduction_kg,
        population_protected=pop_protected,
        health_risk_change=health_risk_delta,
        new_health_risk_score=new_health_risk_score,
        implementation_cost_inr=total_impl_cost,
        annual_maintenance_cost_inr=total_maint_cost,
        payback_period_years=payback_years,
        payback_display=payback_str,
        confidence_level="High" if cell.data_completeness >= 90 else "Medium"
    )
