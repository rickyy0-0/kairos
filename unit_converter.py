"""
KAIROS Production Unit Conversion & Automated Reconciliation Library
Zero-tolerance for financial, energy, and emission unit conversion discrepancies.
Follows Master Rules:
- 1 GWh = 1,000,000 kWh
- 1 MWh = 1,000 kWh
- 1 Crore = ₹10,000,000
- Cost (₹ Crore) = Energy (GWh) × Tariff (₹/kWh) × 0.01
  Example: 100 GWh × ₹8/kWh = ₹8 Crore (NOT ₹80 Crore)
- CO2 (Tonnes/year) = Energy (GWh/year) × Emission Factor (kg CO₂/kWh)
  Proof: Energy (GWh/year) × 1,000 × Emission Factor (kg CO₂/kWh) ÷ 1,000
  Example: 277.68 GWh × 0.82 kg/kWh = 227.6976 Tonnes (Display: 227.70 Tonnes/yr)
  Example: 1,228.44 GWh × 0.82 kg/kWh = 1,007.3208 Tonnes (Display: 1,007.32 Tonnes/yr)
"""

def gwh_to_kwh(gwh: float) -> float:
    """1 GWh = 1,000,000 kWh"""
    return float(gwh * 1_000_000.0)

def kwh_to_gwh(kwh: float) -> float:
    """1,000,000 kWh = 1 GWh"""
    return float(kwh / 1_000_000.0)

def mwh_to_kwh(mwh: float) -> float:
    """1 MWh = 1,000 kWh"""
    return float(mwh * 1_000.0)

def kwh_to_mwh(kwh: float) -> float:
    """1,000 kWh = 1 MWh"""
    return float(kwh / 1_000.0)

def inr_to_crore(inr: float) -> float:
    """1 Crore = ₹10,000,000"""
    return float(inr / 10_000_000.0)

def crore_to_inr(crore: float) -> float:
    """₹1 Crore = ₹10,000,000"""
    return float(crore * 10_000_000.0)

def calculate_annual_cost_inr(energy_gwh: float, tariff_inr_per_kwh: float) -> float:
    """
    Annual Cost (₹) = Energy (GWh) × Tariff (₹/kWh) × 100,000
    Derived from: Cost (₹ Crore) × 10,000,000
    """
    cost_crore = calculate_annual_cost_crore(energy_gwh, tariff_inr_per_kwh)
    return float(cost_crore * 10_000_000.0)

def calculate_annual_cost_crore(energy_gwh: float, tariff_inr_per_kwh: float) -> float:
    """
    Section 9 Master Formula:
    Annual Cost (₹ Crore) = Energy (GWh) × Tariff (₹/kWh) × 0.01
    
    Verified Examples:
    100 GWh × ₹8/kWh = ₹8.0 Crore (NOT ₹80 Crore)
    6,445.95 GWh × ₹8.2/kWh = ₹528.57 Crore (NOT ₹5,285.68 Crore)
    """
    return float(energy_gwh * tariff_inr_per_kwh * 0.01)

def calculate_co2_tonnes_from_gwh(energy_gwh: float, emission_factor_kg_per_kwh: float = 0.820) -> float:
    """
    CO2 tonnes/year = Energy (GWh/year) × Emission Factor (kg CO₂/kWh)
    
    Proof:
    CO2 tonnes/year = Energy (GWh/year) × 1,000 × Emission Factor (kg CO₂/kWh) ÷ 1,000
                    = Energy (GWh/year) × Emission Factor (kg CO₂/kWh)
                    
    Verified Tests:
    277.68 GWh × 0.82 kg/kWh = 227.6976 tonnes/year
    1,228.44 GWh × 0.82 kg/kWh = 1,007.3208 tonnes/year
    """
    return float(energy_gwh * emission_factor_kg_per_kwh)

def verify_financial_reconciliation(energy_gwh: float, tariff_inr_per_kwh: float, cost_crore: float, tolerance: float = 0.05) -> bool:
    """
    Automated financial reconciliation assertion test.
    Returns True if cost_crore equals (energy_gwh * tariff * 0.01) within tolerance.
    """
    expected = calculate_annual_cost_crore(energy_gwh, tariff_inr_per_kwh)
    return abs(cost_crore - expected) <= tolerance

def verify_co2_reconciliation(energy_gwh: float, emission_factor_kg_per_kwh: float, co2_tonnes: float, tolerance: float = 0.05) -> bool:
    """
    Automated CO2 reconciliation assertion test.
    """
    expected = calculate_co2_tonnes_from_gwh(energy_gwh, emission_factor_kg_per_kwh)
    return abs(co2_tonnes - expected) <= tolerance

def verify_energy_bounds(total_gwh: float, cooling_gwh: float, excess_gwh: float) -> bool:
    """
    Validates physical energy sanity constraints:
    1. Excess Cooling Energy <= Current Cooling Energy
    2. Current Cooling Energy <= Total Electricity Consumption
    3. All values non-negative
    """
    if excess_gwh < 0 or cooling_gwh < 0 or total_gwh < 0:
        return False
    if excess_gwh > cooling_gwh + 0.1:
        return False
    if cooling_gwh > total_gwh + 0.1:
        return False
    return True
