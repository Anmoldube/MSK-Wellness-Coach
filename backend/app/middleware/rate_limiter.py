"""
Rate limiting middleware
"""
try:
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded
    from app.core.config import settings

    # Create limiter instance
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE}/minute"] if settings.RATE_LIMIT_ENABLED else [],
        enabled=settings.RATE_LIMIT_ENABLED,
    )
    RATE_LIMITING_AVAILABLE = True
except ImportError:
    limiter = None
    _rate_limit_exceeded_handler = None
    RateLimitExceeded = None
    RATE_LIMITING_AVAILABLE = False


def get_limiter():
    """Get the rate limiter instance"""
    return limiter
