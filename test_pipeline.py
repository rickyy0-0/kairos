import sys
import os

# Add root to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.data.city_generator import generate_city_grid
from backend.data.location_registry import get_or_generate_city_profile
from backend.services.heat_engine import compute_city_overview, calculate_cell_heat_score
from backend.services.cause_engine import calculate_cause_profile
from backend.services.impact_engine import calculate_impact_profile
from backend.services.intervention_engine import generate_recommendations
from backend.services.simulation_engine import simulate_interventions
from backend.services.optimizer_engine import optimize_city_budget
from backend.services.ai_assistant import answer_city_query
from backend.models.schemas import SimulationInput, OptimizationRequest, AskRequest

def test_full_pipeline():
    print("=== Testing KAIROS Backend Decision Intelligence Pipeline ===")
    
    # 1. Grid generation
    profile = get_or_generate_city_profile("chennai")
    cells = generate_city_grid(city_profile=profile)
    print(f"[✓] Generated {len(cells)} spatial grid cells across Chennai.")
    assert len(cells) >= 15, "Should generate >= 15 administrative zones"
    
    # 2. City Overview
    overview = compute_city_overview(cells, city_profile=profile)
    print(f"[✓] City Overview: Avg Temp = {overview.city_avg_temperature_c}°C, Hotspots = {overview.hotspots_count}, Resilience Score = {overview.city_resilience_score}")
    assert overview.hotspots_count > 0, "Should detect hotspots"
    assert overview.city_resilience_score > 0, "Resilience score should be positive"
    
    # 3. Hotspot deep dive
    target_cell = sorted(cells, key=lambda c: c.heat_severity_score, reverse=True)[0]
    print(f"\n--- Testing Hotspot Deep Dive: {target_cell.name} ({target_cell.id}) ---")
    
    # 4. Cause Contribution Profile
    causes = calculate_cause_profile(target_cell)
    pct_sum = sum(c.percentage for c in causes.causes)
    print(f"[✓] Dominant Cause: {causes.dominant_cause} | Causes count: {len(causes.causes)} | Sum: {pct_sum}%")
    for c in causes.causes:
        print(f"    • {c.name}: {c.percentage}% ({c.indicator_description})")
    assert abs(pct_sum - 100.0) < 0.01, f"Cause percentages must sum to 100.0%, got {pct_sum}"
    
    # 5. Multi-Vector Impact
    impact = calculate_impact_profile(target_cell, city_profile=profile)
    print(f"[✓] Impact Analysis:")
    print(f"    • Population Exposed: {impact.population_exposed:,}")
    print(f"    • Excess Energy Wastage: {impact.excess_energy_gwh_yr} GWh/yr (₹{impact.annual_energy_cost_inr:,.0f}/yr)")
    print(f"    • CO2 Emissions: {impact.co2_emissions_tonnes_yr} tonnes/yr")
    print(f"    • Water Excess: {impact.heat_driven_water_ml_yr} ML/yr")
    print(f"    • Health Risk Score: {impact.health_risk_score}/100 ({impact.health_risk_class})")
    
    # 6. 'What Should We Do Here?' Recommendations
    recs = generate_recommendations(target_cell, city_profile=profile)
    print(f"[✓] Recommendations ({len(recs)} received):")
    for r in recs:
        print(f"    Rank {r.rank}: {r.intervention_name} | Scale: {r.recommended_scale} | Cost: ₹{r.estimated_cost_inr:,.0f} | ΔT: -{r.estimated_cooling_impact_c}°C | Payback: {r.payback_display}")
    assert len(recs) == 3, "Must return top-3 recommendations"
    
    # 7. Digital Intervention Simulator
    sim_input = SimulationInput(
        zone_id=target_cell.id,
        tree_coverage=0.25,
        cool_roof_coverage=0.50,
        reflective_pavement=0.30,
        green_roof=0.10,
        shade_structures=0.40
    )
    sim_res = simulate_interventions(target_cell, sim_input)
    print(f"[✓] Simulation Results:")
    print(f"    • Temp Change: {sim_res.temperature_change_c}°C (New: {sim_res.new_temperature_c}°C)")
    print(f"    • Heat Score Change: {sim_res.heat_score_change} (New: {sim_res.new_heat_score})")
    print(f"    • Energy Savings: {sim_res.energy_savings_kwh:,.0f} kWh ({sim_res.energy_savings_pct}%)")
    print(f"    • People Protected: {sim_res.population_protected:,}")
    print(f"    • Implementation Cost: ₹{sim_res.implementation_cost_inr:,.0f}")
    assert sim_res.temperature_change_c < 0, "Simulation should reduce temperature"
    
    # 8. City Cooling Budget Optimizer
    opt_req = OptimizationRequest(budget_inr=50000000.0, objective="best_overall_impact")
    opt_res = optimize_city_budget(cells, opt_req, city_profile=profile)
    print(f"[✓] Optimizer (Budget: ₹{opt_res.total_budget_inr:,.0f}):")
    print(f"    • Allocated: ₹{opt_res.total_allocated_inr:,.0f} | Reserve: ₹{opt_res.unused_reserve_inr:,.0f}")
    print(f"    • Intervened Zones: {opt_res.zones_intervened_count}")
    print(f"    • City Resilience Score: {opt_res.resilience_score_before} → {opt_res.resilience_score_after} (Δ +{round(opt_res.resilience_score_after - opt_res.resilience_score_before, 1)})")
    assert opt_res.total_allocated_inr <= opt_res.total_budget_inr, "Must not exceed budget"
    assert opt_res.zones_intervened_count > 0, "Must allocate to zones"
    
    # 9. Ask the City AI Engine
    ask_res = answer_city_query(f"Why is {cells[0].id} hotter than {cells[-1].id}?", cells, city_profile=profile, overview=overview)
    print(f"[✓] AI Query Test ('Why is {cells[0].id} hotter than {cells[-1].id}?'):")
    print(f"    Answer excerpt: {ask_res.answer[:150]}...")
    assert len(ask_res.key_data_points) > 0, "Should return grounded data points"
    
    print("\n>>> ALL BACKEND PIPELINE TESTS PASSED SUCCESSFULLY! <<<\n")

if __name__ == "__main__":
    test_full_pipeline()
