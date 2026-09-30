from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import (
    auth_routes,
    property_routes,
    apartment_routes,
    tenant_routes,
    rental_routes,
    rent_routes,
    payment_routes,
    maintenance_routes,
    technician_routes,
    audit_routes,
    sla_routes,
    role_routes,
    report_routes
)

from app.core.exceptions import AppError, app_error_handler


app = FastAPI(
    title="Smart Property Rental & Maintenance API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://smart-prop-client-3pq7y2ntk-raghava-narne.vercel.app",
        "https://smart-prop-client.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_exception_handler(
    AppError,
    app_error_handler,
)

# Authentication
app.include_router(auth_routes.router)

# Application APIs
app.include_router(property_routes.router)
app.include_router(apartment_routes.router)
app.include_router(tenant_routes.router)
app.include_router(rental_routes.router)
app.include_router(rent_routes.router)
app.include_router(report_routes.router)
app.include_router(payment_routes.router)
app.include_router(maintenance_routes.router)
app.include_router(technician_routes.router)
app.include_router(audit_routes.router)
app.include_router(sla_routes.router)
app.include_router(role_routes.router)


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }

