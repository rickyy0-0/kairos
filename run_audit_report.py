import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.data.location_registry import get_or_generate_city_profile
from backend.data.city_generator import generate_city_grid
from backend.services.heat_engine import (
    compute_city_overview, compute_energy_overview, compute_water_overview
)
from backend.services.validation_engine import run_full_16_city_audit

def get_grid(cid: str):
    profile = get_or_generate_city_profile(cid)
    cells = generate_city_grid(profile)
    return profile, cells

def main():
    result = run_full_16_city_audit(
        get_grid_fn=get_grid,
        overview_fn=compute_city_overview,
        energy_fn=compute_energy_overview,
        water_fn=compute_water_overview
    )
    
    matrix = result["audit_matrix"]
    summary = result["summary_counts"]
    
    print(f"Total Records: {len(matrix)}")
    print("\nSummary Counts:")
    for k, v in summary.items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
