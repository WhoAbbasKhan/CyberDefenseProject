from enum import Enum
from typing import Dict, List, Any

class SubscriptionTier(str, Enum):
    TRIAL = "trial"
    STARTER = "starter"
    PRO = "pro"
    ENTERPRISE = "enterprise"

class PlanFeatures:
    def __init__(self, max_users: int, modules: List[str]):
        self.max_users = max_users
        self.modules = modules

PLANS: Dict[str, PlanFeatures] = {
    SubscriptionTier.TRIAL: PlanFeatures(max_users=5, modules=["all"]),
    SubscriptionTier.STARTER: PlanFeatures(max_users=10, modules=["email", "web"]),
    SubscriptionTier.PRO: PlanFeatures(max_users=50, modules=["all"]),
    SubscriptionTier.ENTERPRISE: PlanFeatures(max_users=9999, modules=["all", "brand_monitoring"]),
}

def get_plan_features(tier: str) -> PlanFeatures:
    return PLANS.get(tier, PLANS[SubscriptionTier.TRIAL])
