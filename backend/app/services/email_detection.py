import re
from typing import List, Tuple

class EmailDetectionService:
    """
    Simple rule-based engine for Phase 0/2.
    Later can be replaced by ML.
    """
    
    def analyze_email(self, sender: str, subject: str, body: str, links: List[str]) -> Tuple[str, float, str]:
        """
        Returns: (Attack Type, Confidence, Severity)
        If no attack, returns (None, 0.0, "low")
        """
        severity = "low"
        confidence = 0.0
        attack_type = None

        # 1. Phishing Keywords
        phishing_keywords = ["reset password", "urgent", "verify account", "bank", "invoice"]
        keyword_hits = sum(1 for k in phishing_keywords if k in subject.lower() or k in body.lower())
        
        if keyword_hits >= 2:
            confidence += 0.4
            attack_type = "Potential Phishing"
            severity = "medium"

        # 2. Suspicious Links
        suspicious_domains = ["bit.ly", "tinyurl.com", ".xyz", ".top"]
        for link in links:
            if any(d in link for d in suspicious_domains):
                confidence += 0.5
                attack_type = "Malicious Link"
                severity = "high"
                break
        
        # 3. Spoofing Check (Simplified)
        # If sender says "paypal" but domain is not paypal.com
        if "paypal" in sender.lower() and "paypal.com" not in sender.lower():
             confidence = 0.9
             attack_type = "Brand Spoofing"
             severity = "critical"

        if confidence > 0.0 and attack_type is None:
            attack_type = "Suspicious Content"
            
        return attack_type, min(confidence, 1.0), severity

email_detector = EmailDetectionService()
