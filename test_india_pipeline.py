import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from backend.main import app

def test_pipeline():
    client = TestClient(app)
    
    # 1. Health
    r = client.get("/api/health")
    assert r.status_code == 200, f"Health failed: {r.text}"
    print("✓ /api/health OK")
    
    # 2. States
    r = client.get("/api/states")
    assert r.status_code == 200, f"States failed: {r.text}"
    data = r.json()
    assert len(data) >= 36, f"Expected 36 states/UTs, got {len(data)}"
    print(f"✓ /api/states OK ({len(data)} states & UTs)")
    
    # 3. Cities
    r = client.get("/api/cities")
    assert r.status_code == 200, f"Cities failed: {r.text}"
    cities = r.json()
    assert len(cities) >= 10, f"Expected 10+ cities, got {len(cities)}"
    print(f"✓ /api/cities OK ({len(cities)} pre-calibrated cities)")
    
    # 4. Multi-city overview tests (Chennai, Bengaluru, Jaipur, Delhi)
    for cid in ["chennai", "bengaluru", "jaipur", "delhi"]:
        r = client.get(f"/api/city/{cid}/overview")
        assert r.status_code == 200, f"City overview for {cid} failed: {r.text}"
        cov = r.json()
        print(f"✓ /api/city/{cid}/overview OK -> {cov['city_name']} ({cov['state_name']}), Avg Temp: {cov['city_avg_temperature_c']}°C, Resilience: {cov['city_resilience_score']}")
        
        r = client.get(f"/api/city/{cid}/hotspots")
        assert r.status_code == 200
        cells = r.json()
        assert len(cells) > 0
        first_cell_id = cells[0]["id"]
        
        # Test hotspot detail, causes, impact
        r_det = client.get(f"/api/city/{cid}/hotspots/{first_cell_id}")
        assert r_det.status_code == 200
        
        # Test energy overview
        r_eng = client.get(f"/api/city/{cid}/energy")
        assert r_eng.status_code == 200
        
        # Test water overview
        r_wat = client.get(f"/api/city/{cid}/water")
        assert r_wat.status_code == 200
        
        # Test health overview
        r_hlth = client.get(f"/api/city/{cid}/health")
        assert r_hlth.status_code == 200
        
    # 5. Multi-city comparison
    r = client.get("/api/compare?cities=chennai,bengaluru,jaipur,delhi")
    assert r.status_code == 200, f"Comparison failed: {r.text}"
    comp = r.json()
    assert len(comp["cities"]) == 4
    print(f"✓ /api/compare OK -> Compared {len(comp['cities'])} cities, Insight length: {len(comp['comparative_ai_insight'])}")
    
    # 6. Ask Assistant
    r = client.post("/api/ask", json={"query": "Which area should we cool first?", "city_id": "bengaluru"})
    assert r.status_code == 200
    ans = r.json()
    print(f"✓ /api/ask OK -> Key data points: {ans['key_data_points']}")
    
    print("\nALL BACKEND PIPELINE TESTS PASSED!")

if __name__ == "__main__":
    test_pipeline()
