from fastapi import FastAPI

app = FastAPI(
    title="Smart Property Rental & Maintenance Platform"
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
