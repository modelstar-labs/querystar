from posthog import Posthog
from querystar.settings import settings

posthog: Posthog = Posthog(settings.posthog_api_key,
                           host=settings.posthog_api_host)
