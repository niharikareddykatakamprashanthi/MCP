from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get("event", "Unknown")}
Area: {props.get("areaDesc", "Unknown")}
Severity: {props.get("severity", "Unknown")}
Description: {props.get("description", "No description available")}
Instructions: {props.get("instruction", "No specific instructions provided")}
"""

@mcp.tool()
async def get_weather_alerts(latitude: float, longitude: float) -> str:
    """Get weather alerts for a given location."""
    url = f"{NWS_API_BASE}/points/{latitude},{longitude}/forecast/alerts"
    data = await make_nws_request(url)
    if not data:
        return "No weather alerts found for this location."
    alerts = data.get("features", [])
    if not alerts:
        return "No weather alerts found for this location."
    return "\n\n".join(format_alert(alert) for alert in alerts)

#@mcp.resource("config://app")
#def get_config() -> str:
#    """Static Configuration data"""
#    return """App Configuration data"""

@mcp.tool()
def echo(message: str) -> str:
    """A simple echo tool"""
    return f"Echo: {message}"