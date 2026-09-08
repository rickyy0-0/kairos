import numpy as np
from typing import List, Dict, Any, Optional
from backend.models.schemas import GridCell, OptimizationRequest, OptimizationResponse, AllocatedIntervention
from backend.services.intervention_engine import generate_recommendations

def optimize_city_budget(cells: List[GridCell], request: OptimizationRequest, city_profile: Optional[Dict[str, Any]] = None) -> OptimizationResponse:
    """
    Greedy multi-objective knapsack optimizer that allocates a municipal cooling budget (e.g. ₹5 Crore)
    across hotspots for ANY Indian city.
    """
    city_name = city_profile["name"] if city_profile else (cells[0].city_name if cells else "City")
    tariff = float(city_profile.get("electricity_tariff_inr", 8.20)) if city_profile else 8.20
    
    budget_remaining = float(request.budget_inr)
    allocated_list: List[AllocatedIntervention] = []
    candidates = []
    
    for cell in cells:
        if cell.heat_severity_score < 45.0:
            continue
            
        recs = generate_recommendations(cell, city_profile)
        
        for rec in recs:
            cost = rec.estimated_cost_inr
            if cost <= 0 or cost > budget_remaining * 0.40:
                cost = min(cost, budget_remaining * 0.30)
                
            cooling = rec.estimated_cooling_impact_c
            people = int(cell.population * (cooling / 4.0) * 0.75)
            energy_mwh = rec.estimated_energy_savings_kwh / 1000.0
            co2_tonnes = rec.estimated_co2_reduction_kg / 1000.0
            water_ml = rec.estimated_water_impact_liters / 1_000_000.0
            health_red_pct = min(40.0, (cooling / 3.5) * 28.0)
            
            if request.objective == "maximum_cooling":
                utility = cooling * 1000.0 + (cell.heat_severity_score * 5.0)
            elif request.objective == "maximum_population_protected":
                utility = people * 2.0 + (cooling * 200.0)
            elif request.objective == "maximum_energy_savings":
                utility = energy_mwh * 150.0 + (rec.annual_financial_savings_inr / 1000.0)
            elif request.objective == "maximum_health_benefit":
                utility = (health_red_pct * 10.0) + (people * 1.5) + (cell.elderly_pct * 20.0)
            else:  # best_overall_impact
                utility = (
                    cooling * 300.0 +
                    (people / 50.0) +
                    (energy_mwh * 50.0) +
                    (cell.heat_severity_score * 8.0) +
                    (health_red_pct * 15.0)
                )
                
            efficiency_ratio = utility / max(10000.0, cost)
            
            candidates.append({
                "cell": cell,
                "rec": rec,
                "cost": cost,
                "cooling": cooling,
                "people": people,
                "energy_mwh": energy_mwh,
                "co2_tonnes": co2_tonnes,
                "water_ml": water_ml,
                "health_red_pct": health_red_pct,
                "utility": utility,
                "efficiency": efficiency_ratio
            })
            
    candidates.sort(key=lambda x: x["efficiency"], reverse=True)
    
    chosen_zones = set()
    total_cost_allocated = 0.0
    
    for cand in candidates:
        zone_id = cand["cell"].id
        if zone_id in chosen_zones:
            continue
            
        if cand["cost"] <= budget_remaining:
            budget_remaining -= cand["cost"]
            total_cost_allocated += cand["cost"]
            chosen_zones.add(zone_id)
            
            allocated_list.append(AllocatedIntervention(
                zone_id=zone_id,
                zone_name=cand["cell"].name,
                intervention_id=cand["rec"].intervention_id,
                intervention_name=cand["rec"].intervention_name,
                cost_inr=round(cand["cost"], 0),
                cooling_impact_c=round(cand["cooling"], 1),
                people_protected=cand["people"],
                energy_saved_mwh=round(cand["energy_mwh"], 1),
                co2_avoided_tonnes=round(cand["co2_tonnes"], 1),
                water_impact_ml=round(cand["water_ml"], 2),
                health_risk_reduction_pct=round(cand["health_red_pct"], 1)
            ))
            
            if len(chosen_zones) >= request.target_zones_count:
                break
                
    total_people_prot = sum(a.people_protected for a in allocated_list)
    total_energy_saved_mwh = sum(a.energy_saved_mwh for a in allocated_list)
    total_co2_tonnes = sum(a.co2_avoided_tonnes for a in allocated_list)
    total_water_ml = sum(a.water_impact_ml for a in allocated_list)
    avg_cooling_drop = float(np.mean([a.cooling_impact_c for a in allocated_list])) if allocated_list else 0.0
    avg_health_red = float(np.mean([a.health_risk_reduction_pct for a in allocated_list])) if allocated_list else 0.0
    
    resilience_before = 54.2
    resilience_after = float(np.clip(resilience_before + (len(allocated_list) * 1.6) + (total_energy_saved_mwh / 100.0), 54.2, 88.5))
    
    city_impact = {
        "total_population_protected": total_people_prot,
        "total_energy_saved_mwh_yr": round(total_energy_saved_mwh, 1),
        "total_financial_savings_inr_yr": round(total_energy_saved_mwh * 1000.0 * tariff, 0),
        "total_co2_avoided_tonnes_yr": round(total_co2_tonnes, 1),
        "total_water_impact_ml_yr": round(total_water_ml, 2),
        "avg_hotspot_temperature_reduction_c": round(avg_cooling_drop, 2),
        "avg_health_risk_reduction_pct": round(avg_health_red, 1),
        "heat_exposure_reduction_pct": round(min(45.0, (total_people_prot / max(1, sum(c.population for c in cells if c.heat_severity_score >= 51.0))) * 100.0), 1)
    }
    
    before_metrics = {
        "city_avg_heat_risk": 68.4,
        "high_risk_population": sum(c.population for c in cells if c.heat_severity_score >= 51.0),
        "annual_energy_waste_gwh": 41.2,
        "annual_cooling_cost_cr": round((41.2 * 1000.0 * tariff) / 10000.0, 2),
        "health_vulnerability_index": 72.1
    }
    
    after_metrics = {
        "city_avg_heat_risk": round(68.4 - (avg_cooling_drop * 6.5), 1),
        "high_risk_population": max(0, before_metrics["high_risk_population"] - total_people_prot),
        "annual_energy_waste_gwh": round(max(0.0, 41.2 - (total_energy_saved_mwh / 1000.0)), 2),
        "annual_cooling_cost_cr": round(max(0.0, (41.2 * 1000.0 * tariff / 10000.0) - (total_energy_saved_mwh * 1000.0 * tariff / 10_000_000.0)), 2),
        "health_vulnerability_index": round(max(10.0, 72.1 - avg_health_red * 0.7), 1)
    }

    return OptimizationResponse(
        city_name=city_name,
        total_budget_inr=request.budget_inr,
        total_allocated_inr=round(total_cost_allocated, 0),
        unused_reserve_inr=round(budget_remaining, 0),
        objective_used=request.objective,
        zones_intervened_count=len(allocated_list),
        allocations=allocated_list,
        city_impact=city_impact,
        before_metrics=before_metrics,
        after_metrics=after_metrics,
        resilience_score_before=round(resilience_before, 1),
        resilience_score_after=round(resilience_after, 1)
    )
