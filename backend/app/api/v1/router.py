from fastapi import APIRouter
from app.api.v1.endpoints import auth, orgs, email, web, training, reporting, enterprise, anomaly, incidents, threat, prediction, deception, profiling, playbooks, forensic, autonomous, defense, login

api_router = APIRouter()

api_router.include_router(login.router, prefix="/auth", tags=["auth"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(orgs.router, prefix="/orgs", tags=["organizations"])
api_router.include_router(email.router, prefix="/email", tags=["email"])
api_router.include_router(web.router, prefix="/monitor", tags=["monitor"])
api_router.include_router(training.router, prefix="/training", tags=["training"])
api_router.include_router(reporting.router, prefix="/reporting", tags=["reporting"])
api_router.include_router(enterprise.router, prefix="/enterprise", tags=["enterprise"])
api_router.include_router(anomaly.router, prefix="/anomaly", tags=["anomaly"])
api_router.include_router(incidents.router, prefix="/incidents", tags=["incidents"])
api_router.include_router(threat.router, prefix="/threat", tags=["threat"])
api_router.include_router(prediction.router, prefix="/predictions", tags=["predictions"])
api_router.include_router(deception.router, prefix="/deception", tags=["deception"])
api_router.include_router(profiling.router, prefix="/profiling", tags=["profiling"])
api_router.include_router(playbooks.router, prefix="/playbooks", tags=["playbooks"])
api_router.include_router(forensic.router, prefix="/forensic", tags=["forensic"])
api_router.include_router(autonomous.router, prefix="/autonomous", tags=["autonomous"])
api_router.include_router(defense.router, prefix="/defense", tags=["defense"])
