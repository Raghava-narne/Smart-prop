from fastapi import HTTPException


def ok_or_raise(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as exc:
        from app.core.exceptions import AppError
        if isinstance(exc, AppError):
            raise HTTPException(exc.status_code, exc.message)
        raise
