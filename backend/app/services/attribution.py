from typing import Dict, Any

class AttributionService:
    def get_ip_details(self, ip: str) -> Dict[str, Any]:
        """
        Mock GeoIP for Phase 0.
        Real implementation would use `geoip2` database.
        """
        # Simulated data
        if ip.startswith("10.") or ip.startswith("192.") or ip == "127.0.0.1":
            return {"country": "Internal", "city": "Local API", "isp": "Private Network"}
        
        # Random mock for external IPs
        return {
            "country": "Unknown", 
            "city": "Unknown", 
            "isp": "ISP-Placeholder",
            "vpn": False,
            "tor": False
        }

attribution_service = AttributionService()
