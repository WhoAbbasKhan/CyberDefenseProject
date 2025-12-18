from datetime import datetime, timedelta
from typing import Optional, Tuple
# In a real app, this would query Redis/DB for rate limiting and history
# For Phase 0, we'll use simple in-memory or rule logic assuming the input has context, or just return basic classification

class WebDetectionService:
    def detect_web_attack(self, method: str, url: str, user_agent: str, payload: str = "") -> Tuple[Optional[str], str]:
        """
        Returns (Attack Type, Severity)
        """
        # SQL Injection (Basic)
        sql_patterns = ["UNION SELECT", "OR 1=1", "DROP TABLE"]
        if any(p in payload.upper() or p in url.upper() for p in sql_patterns):
            return "SQL Injection", "critical"
            
        # XSS
        if "<script>" in payload or "<script>" in url:
            return "XSS Attempt", "high"
            
        # Scanners
        scanners = ["sqlmap", "nikto", "nmap"]
        if any(s in user_agent.lower() for s in scanners):
            return "Vulnerability Scanner", "high"
            
        return None, "low"

class LoginDetectionService:
    # We ideally need state (Redis) to detect brute force (N failed attempts)
    # This service will be called AFTER database insert usually to check windows
    
    def detect_login_anomaly(self, username: str, success: bool, ip: str) -> Tuple[Optional[str], str]:
        """
        In a real implementation, we would check Redis for fail count.
        For now, we just return None unless we simulate.
        """
        # Placeholder for Brute Force Logic (implemented in API or here via Redis)
        return None, "low"

web_detector = WebDetectionService()
login_detector = LoginDetectionService()
