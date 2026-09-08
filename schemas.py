from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class WeatherDetail(BaseModel):
    temperature_2m: float
    apparent_temperature: float
    relative_humidity_2m: float
    wind_speed_10m: float
    wind_direction_10m: float
    cloud_cover: float
    precipitation: float
    surface_pressure: float
    weather_code: int
    condition: str

class WeatherLocation(BaseModel):
    name: str
    state: str
    latitude: float
    longitude: float
    district: Optional[str] = None

class WeatherObservation(BaseModel):
    status: str
    location: WeatherLocation
    weather: WeatherDetail
    source: str = "Open-Meteo Forecast API"
    source_url: str = "https://open-meteo.com/"
    data_type: str = "Live model-based weather (NWP / ERA5 assimilation)"
    provenance_tag: str = "LIVE"
    retrieved_at: str
    time_display: str
    timestamp_iso: str
    cached: bool = False
    is_fallback: bool = False
    notice: Optional[str] = None

class HeatRiskBreakdown(BaseModel):
    total_score: float
    risk_classification: str
    model_version: str = "Heat Risk Model v2.0"
    formula: str = "Score = 0.35·T_air + 0.20·T_apparent + 0.15·Veg_Deficit + 0.15·Built_Density + 0.15·Pop_Exposure"
    temperature_contribution: float
    apparent_temp_contribution: float
    vegetation_deficit_contribution: float
    built_density_contribution: float
    population_exposure_contribution: float
    wind_ventilation_modifier: float
    air_temp_c: float
    lst_surface_c: float
    humidity_pct: float
    provenance_tag: str = "MODELLED"

class CityProfile(BaseModel):
    id: str
    name: str
    state: str
    district: Optional[str] = None
    zone_prefix: str
    center_lat: float
    center_lon: float
    bounds: List[List[float]]
    climate_zone: str
    base_air_temp_c: float
    base_surface_temp_c: float
    base_humidity_pct: float
    water_stress_index: float
    base_vegetation_pct: float
    base_impervious_pct: float
    electricity_tariff_inr: float
    grid_carbon_intensity: float
    cooling_degree_days: int
    data_mode: str = "LIVE"
    admin_type: str = "Municipal Area"
    lgd_code: Optional[str] = None

class StateInfo(BaseModel):
    name: str
    type: str  # "State" or "UT"
    cities: List[str]

class GridCell(BaseModel):
    id: str
    name: str
    city_name: str
    state_name: str
    district_name: Optional[str] = None
    admin_level: str = "Analysis Grid Sector"  # "Municipal Zone" | "Ward" | "Analysis Grid Sector"
    is_official_boundary: bool = False
    lat: float
    lon: float
    bounds: List[List[float]]  # [[min_lat, min_lon], [max_lat, max_lon]]
    surface_temp_c: float
    air_temp_c: float
    lst_source: str = "Modelled Surface Energy Balance (Landsat / MODIS Calibrated)"
    lst_acquisition_date: str = "2026-09-07"
    ndvi: float
    vegetation_pct: float
    building_density_pct: float
    road_asphalt_pct: float
    impervious_pct: float
    population: int
    population_source: str = "Census of India / GHS-POP Estimate"
    population_density: float
    humidity_pct: float
    elevation_m: float
    historical_temp_trend: float
    night_temp_c: float
    cooling_access_pct: float
    hospital_dist_km: float
    elderly_pct: float
    child_pct: float
    outdoor_worker_pct: float
    soil_moisture_pct: float
    traffic_intensity: float
    area_sqm: float
    roof_area_sqm: float
    pavement_area_sqm: float
    open_space_sqm: float
    heat_severity_score: float
    heat_classification: str
    data_completeness: float
    confidence_level: str
    heat_breakdown: Optional[HeatRiskBreakdown] = None

class CauseItem(BaseModel):
    id: str
    name: str
    percentage: float
    contribution_score: float
    indicator_description: str
    evidence_text: str

class CauseAnalysis(BaseModel):
    zone_id: str
    zone_name: str
    city_name: str
    state_name: str
    dominant_cause: str
    causes: List[CauseItem]
    zone_vs_city: Dict[str, Any]  # Zone vs City average differentials
    qualitative_narrative: str
    confidence_level: str
    data_completeness: float
    provenance_tag: str = "MODELLED"

class ImpactAnalysis(BaseModel):
    zone_id: str
    zone_name: str
    city_name: str
    state_name: str
    population_exposed: int
    heat_severity_score: float
    excess_energy_gwh_yr: float
    annual_energy_cost_inr: float
    co2_emissions_tonnes_yr: float
    heat_driven_water_ml_yr: float
    water_breakdown: Dict[str, float]
    health_risk_score: float
    health_risk_class: str
    vulnerability_drivers: List[str]
    provenance_tag: str = "MODELLED ESTIMATE"

class InterventionDetail(BaseModel):
    id: str
    name: str
    category: str
    description: str
    unit_cost_inr: float
    cost_unit: str
    expected_cooling_c_min: float
    expected_cooling_c_max: float
    energy_savings_pct: float
    water_impact_type: str
    water_consumption_liters_yr: float
    co2_benefit_tonnes_yr: float
    lifespan_years: int
    maintenance_cost_annual_inr: float
    implementation_difficulty: str
    implementation_time_months: int

class RecommendationItem(BaseModel):
    rank: int
    intervention_id: str
    intervention_name: str
    category: str
    suitability_score: float
    reason: str
    recommended_scale: str
    estimated_cost_inr: float
    cost_label: str = "Estimated Implementation Cost (Modelled)"
    estimated_cooling_impact_c: float
    estimated_energy_savings_kwh: float
    annual_financial_savings_inr: float
    estimated_water_impact_liters: float
    estimated_co2_reduction_kg: float
    implementation_time: str
    payback_period_years: Optional[float] = None
    payback_display: str
    confidence_level: str
    recommendation_score: float
    provenance_tag: str = "MODELLED ESTIMATE"

class HotspotDetail(BaseModel):
    cell: GridCell
    causes: CauseAnalysis
    impact: ImpactAnalysis
    recommendations: List[RecommendationItem]

class SimulationInput(BaseModel):
    zone_id: str
    tree_coverage: float = Field(0.0, ge=0.0, le=0.50)
    cool_roof_coverage: float = Field(0.0, ge=0.0, le=1.0)
    reflective_pavement: float = Field(0.0, ge=0.0, le=1.0)
    green_roof: float = Field(0.0, ge=0.0, le=0.50)
    shade_structures: float = Field(0.0, ge=0.0, le=1.0)

class SimulationOutput(BaseModel):
    zone_id: str
    zone_name: str
    city_name: str
    temperature_change_c: float
    new_temperature_c: float
    heat_score_change: float
    new_heat_score: float
    energy_savings_kwh: float
    energy_savings_pct: float
    annual_financial_savings_inr: float
    water_change_liters: float
    co2_reduction_kg: float
    population_protected: int
    health_risk_change: float
    new_health_risk_score: float
    implementation_cost_inr: float
    annual_maintenance_cost_inr: float
    payback_period_years: Optional[float] = None
    payback_display: str
    confidence_level: str
    outcome_label: str = "Projected Reduction (Simulated Outcome)"
    provenance_tag: str = "SIMULATED"

class OptimizationRequest(BaseModel):
    budget_inr: float = Field(50000000.0, ge=1000000.0)  # Default ₹5 Crore
    objective: str = "best_overall_impact"
    target_zones_count: int = 15

class AllocatedIntervention(BaseModel):
    zone_id: str
    zone_name: str
    intervention_id: str
    intervention_name: str
    cost_inr: float
    cooling_impact_c: float
    people_protected: int
    energy_saved_mwh: float
    co2_avoided_tonnes: float
    water_impact_ml: float
    health_risk_reduction_pct: float

class OptimizationResponse(BaseModel):
    city_name: str
    total_budget_inr: float
    total_allocated_inr: float
    unused_reserve_inr: float
    objective_used: str
    zones_intervened_count: int
    allocations: List[AllocatedIntervention]
    city_impact: Dict[str, Any]
    before_metrics: Dict[str, Any]
    after_metrics: Dict[str, Any]
    resilience_score_before: float
    resilience_score_after: float
    provenance_tag: str = "MODELLED OPTIMIZATION"

class CityComparisonMetric(BaseModel):
    city_id: str
    city_name: str
    state_name: str
    climate_zone: str
    avg_temperature_c: float
    max_surface_temp_c: float
    hotspots_count: int
    severe_hotspots_count: int
    people_exposed: int
    avg_vegetation_pct: float
    avg_impervious_pct: float
    excess_energy_gwh_yr: float
    annual_cooling_cost_cr: float
    water_stress_index: float
    excess_water_ml_yr: float
    avg_health_risk_score: float
    city_resilience_score: float
    estimated_intervention_need_cr: float
    primary_heat_driver: str
    live_weather: Optional[WeatherDetail] = None

class CityComparisonResponse(BaseModel):
    cities: List[CityComparisonMetric]
    comparative_ai_insight: str
    key_differentiators: List[str]

class AskRequest(BaseModel):
    query: str
    city_id: Optional[str] = "chennai"
    zone_id: Optional[str] = None

class AskResponse(BaseModel):
    query: str
    answer: str
    key_data_points: List[str]
    referenced_zones: List[str]
    suggested_followups: List[str]

class ConfigWeights(BaseModel):
    weight_air_temp: float = 0.35
    weight_surface_temp: float = 0.20
    weight_vegetation_deficit: float = 0.15
    weight_built_density: float = 0.15
    weight_population_exposure: float = 0.15

class ProvenanceMetricItem(BaseModel):
    metric_id: str
    metric_name: str
    value_display: str
    status: str = "OFFICIAL"  # "OFFICIAL" | "LIVE" | "DERIVED" | "MODELLED" | "DATA UNAVAILABLE"
    category: Optional[str] = "OFFICIAL"  # "OFFICIAL" | "LIVE" | "DERIVED" | "MODELLED" | "DATA UNAVAILABLE"
    source_organization: str
    dataset_name: str
    dataset_year: str
    geographic_level: Optional[str] = "Municipal Corporation"
    geographic_name: Optional[str] = None
    source_url: str
    exact_input_value: str
    unit: str
    formula: str
    model_assumptions: str
    uncertainty_range: Optional[str] = None
    confidence: Optional[str] = "HIGH"  # "HIGH" | "MEDIUM" | "LOW" | "UNAVAILABLE"
    retrieved_at: Optional[str] = None
    vintage_year: Optional[str] = None
    validation_status: str

class CityOverview(BaseModel):
    city_id: str
    city_name: str
    state_name: str
    district_name: Optional[str] = None
    climate_zone: str
    data_mode: str = "LIVE"
    last_updated: str
    weather_source: str = "Open-Meteo Forecast API"
    total_zones: int
    hotspots_count: int
    severe_hotspots_count: int
    city_avg_temperature_c: float  # Live Air Temp
    city_max_temperature_c: float  # Modelled Peak LST
    current_weather: Optional[WeatherDetail] = None
    people_exposed_high_risk: int
    excess_electricity_gwh_yr: float
    excess_water_ml_yr: float
    annual_cooling_cost_inr: float
    excess_co2_tonnes_yr: float
    city_resilience_score: float
    water_stress_score: float
    high_priority_zones: List[Dict[str, Any]]
    key_city_action: Dict[str, Any]
    score_breakdown: Optional[HeatRiskBreakdown] = None
    provenance_details: Optional[List[ProvenanceMetricItem]] = None
    data_status: Optional[str] = "OFFICIAL / LIVE / MODELLED MULTI-SOURCE"
    provenance_tag: Optional[str] = "Evidence-backed multi-source dataset"

class EnergyOverview(BaseModel):
    city_name: str
    state_name: str
    total_electricity_gwh: float = 3606.0
    baseline_cooling_gwh: float = 691.6
    total_excess_energy_gwh: float
    current_cooling_gwh: float = 969.28
    other_electricity_gwh: float = 2636.72
    annual_cost_cr: float
    excess_co2_tonnes: float
    peak_demand_risk_score: float
    electricity_tariff_inr: float
    grid_emission_factor: float
    top_energy_zones: List[Dict[str, Any]]
    heat_vs_energy_curve: List[Dict[str, Any]]
    baseline_details: Optional[Dict[str, Any]] = None
    provenance_details: Optional[List[ProvenanceMetricItem]] = None
    data_status: str = "OFFICIAL CEA DATA"
    provenance_tag: str = "Model estimate • CEA electricity baseline"

class WaterOverview(BaseModel):
    city_name: str
    state_name: str
    observed_water_supply_mld: float = 0.0
    observed_water_supply_range_mld: str = "N/A"
    annual_observed_supply_ml: float = 0.0
    stage_of_groundwater_extraction_pct: float = 0.0
    groundwater_category: str = "Unassessed"
    annual_groundwater_extraction_mcm: float = 0.0
    annual_extractable_groundwater_mcm: float = 0.0
    normal_annual_rainfall_mm: float = 0.0
    derived_water_stress_index: float = 0.0
    water_stress_index: float = 0.0
    heat_associated_water_mld: float = 0.0
    heat_associated_water_range_mld: str = "0.0 MLD"
    annual_heat_water_ml: float = 0.0
    total_excess_water_ml: float = 0.0
    domestic_base_demand_mld: float = 0.0
    domestic_heat_surge_mld: float = 0.0
    cooling_tower_water_status: str = "City-wide cooling-tower water consumption: Insufficient public data"
    cooling_tower_metering_available: bool = False
    water_breakdown: Dict[str, Any]
    trade_off_matrix: List[Dict[str, Any]]
    highest_water_stress_zones: List[Dict[str, Any]]
    baseline_details: Optional[Dict[str, Any]] = None
    provenance_details: Optional[List[ProvenanceMetricItem]] = None
    data_status: str = "OFFICIAL WATER DATA (MUNICIPAL UTILITY/CGWB)"
    provenance_tag: str = "Model estimate • Municipal Utility & CGWB baseline"

class HealthOverview(BaseModel):
    city_name: str
    state_name: str
    avg_health_risk_score: float
    total_vulnerable_exposed: int
    critical_zones_count: int
    high_zones_count: int
    demographic_breakdown: Dict[str, Any]
    highest_risk_zones: List[Dict[str, Any]]
    provenance_tag: str = "MODELLED V-INDEX"

class DataSourceItem(BaseModel):
    metric: str
    source: str
    data_type: str  # "Live" | "Observed" | "Modelled" | "Estimated" | "Historical"
    update_frequency: str
    resolution: str
    description: str

class LocationSearchCard(BaseModel):
    id: str
    name: str
    state: str
    district: Optional[str] = None
    latitude: float
    longitude: float
    current_temp_c: float
    feels_like_c: float
    humidity_pct: float
    heat_risk_score: float
    heat_risk_tier: str
    population_exposed_est: int
    last_updated: str
    source: str
    admin_type: str
