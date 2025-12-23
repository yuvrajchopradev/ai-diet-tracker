from fastapi import Request, status
from fastapi.responses import JSONResponse

async def global_expension_handler(request: Request, e: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal Server Error"
        }
    )