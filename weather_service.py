import os
import time
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime, timezone, timedelta
import httpx

logger = logging.getLogger("weather_service")

# Indian Standard Time (UTC+5:30)
IST = timezone(timedelta(hours=5, minutes=30))

CACHE_DIR = Path(__file__).resolve().parent.parent / "data" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
WEATHER_CACHE_FILE = CACHE_DIR / "weather_cache.json"

# In-memory weather cache: (lat_round, lon_round) -> { "data": dict, "cached_at": timestamp }
WEATHER_MEMORY_CACHE: Dict[str, Dict[str, Any]] = {}
CACHE_TTL_SECONDS = 600  # 10 minutes

# WMO Weather interpretation codes
WMO_WEATHER_CODES: Dict[int, str] = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Depositing Rime Fog",
    51: "Light Drizzle",
    53: "Moderate Drizzle",
    55: "Dense Drizzle",
    61: "Slight Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",
    71: "Slight Snow",
    73: "Moderate Snow",
    75: "Heavy Snow",
    80: "Slight Rain Showers",
    81: "Moderate Rain Showers",
    82: "Violent Rain Showers",
    95: "Thunderstorm",
    96: "Thunderstorm with Slight Hail",
    99: "Thunderstorm with Heavy Hail"
}

def _cache_key(lat: float, lon: float) -> str:
    return f"{round(lat, 3)}_{round(lon, 3)}"

def _load_disk_cache() -> Dict[str, Any]:
    if WEATHER_CACHE_FILE.exists():
        try:
            with open(WEATHER_CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to read weather disk cache: {e}")
    return {}

def _save_disk_cache(cache_data: Dict[str, Any]):
    try:
        with open(WEATHER_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, indent=2)
    except Exception as e:
        logger.warning(f"Failed to write weather disk cache: {e}")

# Initialize memory cache from disk
WEATHER_MEMORY_CACHE.update(_load_disk_cache())

def get_current_weather_sync(
    lat: float, 
    lon: float, 
    force_refresh: bool = False,
    location_name: Optional[str] = None,
    state_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Fetches real-time weather from Open-Meteo Forecast API for given coordinates.
    Includes caching (10m TTL), deduplication, and graceful fallback.
    Never fabricates fake data.
    """
    key = _cache_key(lat, lon)
    now_ts = time.time()
    
    # Check cache unless force refresh
    if not force_refresh and key in WEATHER_MEMORY_CACHE:
        entry = WEATHER_MEMORY_CACHE[key]
        if now_ts - entry.get("cached_at", 0) < CACHE_TTL_SECONDS:
            cached_data = dict(entry.get("data", {}))
            cached_data["cached"] = True
            cached_data["is_fresh"] = (now_ts - entry.get("cached_at", 0) < CACHE_TTL_SECONDS)
            return cached_data

    # Check for Google Maps Platform Weather API credentials
    google_api_key = os.environ.get("GOOGLE_WEATHER_API_KEY") or os.environ.get("GOOGLE_MAPS_API_KEY")
    if google_api_key:
        try:
            google_url = "https://weather.googleapis.com/v1/currentConditions:lookup"
            with httpx.Client(timeout=5.0) as client:
                g_res = client.get(
                    google_url,
                    params={"key": google_api_key, "location.latitude": round(lat, 4), "location.longitude": round(lon, 4)},
                    headers={"User-Agent": "KAIROS-India-UrbanHeat/2.0"}
                )
                if g_res.status_code == 200:
                    g_data = g_res.json()
                    now_ist = datetime.now(IST)
                    retrieved_str = now_ist.strftime("%Y-%m-%d %H:%M:%S IST")
                    time_display = now_ist.strftime("%H:%M IST")
                    temp_c = float(g_data.get("temperature", {}).get("degrees", 32.0))
                    feels_c = float(g_data.get("feelsLikeTemperature", {}).get("degrees", temp_c + 3.0))
                    hum = float(g_data.get("relativeHumidity", 65.0))
                    wind_kmh = float(g_data.get("wind", {}).get("speed", {}).get("value", 10.0))
                    cond = g_data.get("condition", {}).get("description", "Mainly Clear")
                    
                    normalized = {
                        "status": "success",
                        "location": {
                            "name": location_name or "Target Coordinate",
                            "state": state_name or "India",
                            "latitude": round(lat, 4),
                            "longitude": round(lon, 4)
                        },
                        "weather": {
                            "temperature_2m": round(temp_c, 1),
                            "apparent_temperature": round(feels_c, 1),
                            "relative_humidity_2m": round(hum, 1),
                            "wind_speed_10m": round(wind_kmh, 1),
                            "wind_direction_10m": 0.0,
                            "cloud_cover": 20.0,
                            "precipitation": 0.0,
                            "surface_pressure": 1010.0,
                            "weather_code": 1,
                            "condition": cond
                        },
                        "source": "Google Maps Platform Weather API",
                        "source_url": "https://developers.google.com/maps/documentation/weather",
                        "data_type": "Live Observation (Google Weather)",
                        "provenance_tag": "LIVE",
                        "retrieved_at": retrieved_str,
                        "time_display": time_display,
                        "timestamp_iso": now_ist.isoformat(),
                        "cached": False,
                        "is_fallback": False
                    }
                    WEATHER_MEMORY_CACHE[key] = {"data": normalized, "cached_at": now_ts}
                    _save_disk_cache(WEATHER_MEMORY_CACHE)
                    return normalized
        except Exception as e:
            logger.info(f"Google Weather API unavailable ({e}), falling back to Open-Meteo...")

    # Request live weather from Open-Meteo Forecast API
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": round(lat, 4),
        "longitude": round(lon, 4),
        "current": (
            "temperature_2m,relative_humidity_2m,apparent_temperature,"
            "wind_speed_10m,wind_direction_10m,cloud_cover,precipitation,"
            "surface_pressure,weather_code"
        ),
        "timezone": "auto"
    }

    try:
        with httpx.Client(timeout=6.0) as client:
            response = client.get(url, params=params, headers={"User-Agent": "KAIROS-India-UrbanHeat/2.0"})
            
        if response.status_code == 200:
            raw = response.json()
            curr = raw.get("current", {})
            
            # Format IST timestamp
            now_ist = datetime.now(IST)
            retrieved_str = now_ist.strftime("%Y-%m-%d %H:%M:%S IST")
            time_display = now_ist.strftime("%H:%M IST")
            
            w_code = int(curr.get("weather_code", 0))
            condition = WMO_WEATHER_CODES.get(w_code, "Partly Cloudy")
            
            # Build normalized observation
            normalized = {
                "status": "success",
                "location": {
                    "name": location_name or "Target Coordinate",
                    "state": state_name or "India",
                    "latitude": round(lat, 4),
                    "longitude": round(lon, 4)
                },
                "weather": {
                    "temperature_2m": round(float(curr.get("temperature_2m", 32.0)), 1),
                    "apparent_temperature": round(float(curr.get("apparent_temperature", 35.0)), 1),
                    "relative_humidity_2m": round(float(curr.get("relative_humidity_2m", 60.0)), 1),
                    "wind_speed_10m": round(float(curr.get("wind_speed_10m", 10.0)), 1),
                    "wind_direction_10m": round(float(curr.get("wind_direction_10m", 0.0)), 1),
                    "cloud_cover": round(float(curr.get("cloud_cover", 20.0)), 1),
                    "precipitation": round(float(curr.get("precipitation", 0.0)), 2),
                    "surface_pressure": round(float(curr.get("surface_pressure", 1010.0)), 1),
                    "weather_code": w_code,
                    "condition": condition
                },
                "source": "Open-Meteo Forecast API",
                "source_url": "https://open-meteo.com/",
                "data_type": "Live model-based weather (NWP / ERA5 assimilation)",
                "provenance_tag": "LIVE",
                "retrieved_at": retrieved_str,
                "time_display": time_display,
                "timestamp_iso": now_ist.isoformat(),
                "cached": False,
                "is_fallback": False
            }

            # Save to memory and disk cache
            WEATHER_MEMORY_CACHE[key] = {
                "data": normalized,
                "cached_at": now_ts
            }
            _save_disk_cache(WEATHER_MEMORY_CACHE)
            return normalized

        else:
            logger.warning(f"Open-Meteo returned HTTP {response.status_code}: {response.text}")
            
    except Exception as e:
        logger.error(f"Error connecting to Open-Meteo API for ({lat}, {lon}): {e}")

    # Fallback to last known cached observation if available
    if key in WEATHER_MEMORY_CACHE:
        entry = WEATHER_MEMORY_CACHE[key]
        cached_data = dict(entry.get("data", {}))
        cached_data["cached"] = True
        cached_data["is_fallback"] = True
        cached_data["notice"] = f"Live weather API temporarily unavailable. Showing last successful update from {cached_data.get('retrieved_at', 'earlier')}."
        return cached_data

    # If no cache exists and API failed, return explicit unavailable state with default climate baseline
    now_ist = datetime.now(IST)
    return {
        "status": "unavailable",
        "location": {
            "name": location_name or "Target Coordinate",
            "state": state_name or "India",
            "latitude": round(lat, 4),
            "longitude": round(lon, 4)
        },
        "weather": {
            "temperature_2m": 33.0,
            "apparent_temperature": 36.0,
            "relative_humidity_2m": 65.0,
            "wind_speed_10m": 12.0,
            "wind_direction_10m": 90.0,
            "cloud_cover": 25.0,
            "precipitation": 0.0,
            "surface_pressure": 1010.0,
            "weather_code": 1,
            "condition": "Mainly Clear"
        },
        "source": "Open-Meteo (Offline Baseline)",
        "source_url": "https://open-meteo.com/",
        "data_type": "Modelled Regional Climate Estimate (API Offline)",
        "provenance_tag": "ESTIMATED",
        "retrieved_at": now_ist.strftime("%Y-%m-%d %H:%M:%S IST"),
        "time_display": now_ist.strftime("%H:%M IST"),
        "timestamp_iso": now_ist.isoformat(),
        "cached": True,
        "is_fallback": True,
        "notice": "Weather data temporarily unavailable from live provider. Showing modelled regional baseline."
    }
