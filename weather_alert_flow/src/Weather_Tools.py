"""
Weather_Tools.py

Enhanced weather tools for a multi-agent workflow:

User Query
    -> Guardrail Agent
    -> Weather Agent (this module)
    -> Email Composer Agent
    -> Email Delivery Service

These tools return normalized JSON-friendly structures aligned with the
Weather Agent output schema.
"""

from __future__ import annotations

from typing import Any
import requests
from agents import function_tool

BASE_WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
BASE_GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"

TIMEOUT = 10


WEATHER_CODES = {
    0: ("Clear", "Clear sky"),
    1: ("Mainly Clear", "Mostly sunny"),
    2: ("Partly Cloudy", "Partly cloudy"),
    3: ("Overcast", "Cloudy"),
    45: ("Fog", "Foggy conditions"),
    48: ("Fog", "Dense fog"),
    51: ("Drizzle", "Light drizzle"),
    53: ("Drizzle", "Moderate drizzle"),
    55: ("Drizzle", "Heavy drizzle"),
    61: ("Rain", "Light rain"),
    63: ("Rain", "Moderate rain"),
    65: ("Rain", "Heavy rain"),
    71: ("Snow", "Light snowfall"),
    73: ("Snow", "Moderate snowfall"),
    75: ("Snow", "Heavy snowfall"),
    80: ("Rain Showers", "Light showers"),
    81: ("Rain Showers", "Moderate showers"),
    82: ("Rain Showers", "Violent showers"),
    95: ("Thunderstorm", "Thunderstorm"),
    96: ("Thunderstorm", "Thunderstorm with hail"),
    99: ("Thunderstorm", "Severe thunderstorm with hail"),
}


REGION_MAP = {
    "india": ["Delhi", "Mumbai", "Kolkata", "Chennai", "Bengaluru"],
    "andhra pradesh": ["Visakhapatnam", "Vijayawada", "Tirupati"],
    "south india": ["Hyderabad", "Chennai", "Bengaluru", "Kochi"],
    "japan": ["Tokyo", "Osaka", "Sapporo", "Fukuoka"],
    "california": ["Los Angeles", "San Francisco", "San Diego", "Sacramento"],
}


def _get(url: str, params: dict[str, Any]) -> dict[str, Any]:
    response = requests.get(url, params=params, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def _build_alerts(weather: dict[str, Any]) -> list[dict[str, str]]:
    alerts = []

    if weather.get("rainfall_mm", 0) >= 20:
        alerts.append({
            "severity": "moderate",
            "title": "Heavy Rain Alert",
            "description": "Heavy rainfall is expected. Carry an umbrella and allow extra travel time."
        })

    if weather.get("uv_index", 0) >= 8:
        alerts.append({
            "severity": "moderate",
            "title": "High UV Alert",
            "description": "Limit prolonged sun exposure and use sunscreen."
        })

    if weather.get("wind_speed_kph", 0) >= 50:
        alerts.append({
            "severity": "severe",
            "title": "Strong Wind Alert",
            "description": "Strong winds may affect outdoor activities."
        })

    return alerts


def _build_recommendations(weather: dict[str, Any]) -> list[str]:
    recommendations = []

    if weather.get("temperature_c", 0) >= 35:
        recommendations.append(
            "Stay hydrated and avoid prolonged exposure to direct sunlight."
        )

    if weather.get("rainfall_mm", 0) > 0:
        recommendations.append(
            "Carry an umbrella or rain jacket when going outside."
        )

    if weather.get("uv_index", 0) >= 8:
        recommendations.append(
            "Apply sunscreen and wear protective clothing."
        )

    if weather.get("wind_speed_kph", 0) >= 30:
        recommendations.append(
            "Secure loose outdoor items and use caution while driving."
        )

    return recommendations


@function_tool
def resolve_location(query: str) -> dict[str, Any]:
    """
    Resolve a city, region, postal code, or landmark into coordinates.
    """

    data = _get(
        BASE_GEOCODE_URL,
        {
            "name": query,
            "count": 1,
            "language": "en",
            "format": "json",
        },
    )

    results = data.get("results")

    if not results:
        raise ValueError(f"No location found for '{query}'.")

    result = results[0]

    return {
        "name": result["name"],
        "state": result.get("admin1"),
        "country": result.get("country"),
        "latitude": result["latitude"],
        "longitude": result["longitude"],
        "timezone": result.get("timezone"),
    }


@function_tool
def get_current_weather(latitude: float, longitude: float) -> dict[str, Any]:
    """
    Retrieve normalized current weather information.
    """

    data = _get(
        BASE_WEATHER_URL,
        {
            "latitude": latitude,
            "longitude": longitude,
            "timezone": "auto",
            "current": ",".join([
                "temperature_2m",
                "apparent_temperature",
                "relative_humidity_2m",
                "precipitation",
                "wind_speed_10m",
                "wind_direction_10m",
                "weather_code",
                "visibility",
                "uv_index",
            ]),
        },
    )

    current = data["current"]

    condition, description = WEATHER_CODES.get(
        current["weather_code"],
        ("Unknown", "Unknown weather condition"),
    )

    return {
        "observation_time": current["time"],
        "weather": {
            "condition": condition,
            "description": description,
            "temperature_c": current["temperature_2m"],
            "feels_like_c": current["apparent_temperature"],
            "humidity_percent": current["relative_humidity_2m"],
            "rainfall_mm": current["precipitation"],
            "wind_speed_kph": current["wind_speed_10m"],
            "wind_direction": current["wind_direction_10m"],
            "visibility_km": round(current["visibility"] / 1000, 1),
            "uv_index": current["uv_index"],
        },
    }


@function_tool
def get_weather_forecast(
    latitude: float,
    longitude: float,
    days: int = 3,
) -> list[dict[str, Any]]:
    """
    Return daily forecast records instead of columnar arrays.
    """

    data = _get(
        BASE_WEATHER_URL,
        {
            "latitude": latitude,
            "longitude": longitude,
            "timezone": "auto",
            "forecast_days": max(1, min(days, 7)),
            "daily": ",".join([
                "weather_code",
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_probability_max",
            ]),
        },
    )

    daily = data["daily"]
    forecast = []

    for i, date in enumerate(daily["time"]):
        condition, _ = WEATHER_CODES.get(
            daily["weather_code"][i],
            ("Unknown", ""),
        )

        forecast.append({
            "date": date,
            "condition": condition,
            "min_temp_c": daily["temperature_2m_min"][i],
            "max_temp_c": daily["temperature_2m_max"][i],
            "rain_probability_percent": daily["precipitation_probability_max"][i],
        })

    return forecast


@function_tool
def get_weather_report(
    location: str,
    forecast_days: int = 3,
) -> dict[str, Any]:
    """
    Return a complete weather report aligned with the Weather Agent schema.
    Preferred tool for the Weather Agent.
    """

    resolved = resolve_location(location)

    current = get_current_weather(
        resolved["latitude"],
        resolved["longitude"],
    )

    forecast = get_weather_forecast(
        resolved["latitude"],
        resolved["longitude"],
        forecast_days,
    )

    alerts = _build_alerts(current["weather"])
    recommendations = _build_recommendations(current["weather"])

    return {
        "status": "success",
        "request_type": "forecast" if forecast_days > 1 else "current_weather",
        "location": resolved,
        "observation_time": current["observation_time"],
        "weather": current["weather"],
        "forecast": forecast,
        "alerts": alerts,
        "recommendations": recommendations,
    }


@function_tool
def get_regional_weather(region: str) -> list[dict[str, Any]]:
    """
    Get weather reports for representative locations in a region.
    """

    locations = REGION_MAP.get(region.lower())

    if not locations:
        raise ValueError(
            f"No representative locations configured for '{region}'."
        )

    return [get_weather_report(city, forecast_days=1) for city in locations]


@function_tool
def get_representative_locations(region: str) -> list[str]:
    """
    Return representative cities for a country, state, or region.
    """

    locations = REGION_MAP.get(region.lower())

    if not locations:
        raise ValueError(
            f"No representative locations found for '{region}'."
        )

    return locations
