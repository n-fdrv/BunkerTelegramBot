"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.config.settings_base")

django_application = get_asgi_application()


async def application(scope, receive, send):
    """Точка входа для ASGI приложения."""
    if scope["type"] in {"http", "lifespan"}:
        await django_application(scope, receive, send)
    else:
        raise NotImplementedError(f"Unknown scope type {scope['type']}")
