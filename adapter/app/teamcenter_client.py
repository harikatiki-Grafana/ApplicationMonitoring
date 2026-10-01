import httpx
from .config import settings
class TeamcenterClient:
    def __init__(self):
        self.client = httpx.Client(base_url=settings.teamcenter_base_url, verify=settings.teamcenter_verify_tls, timeout=10)
    def health(self):
        return self.client.get(settings.teamcenter_health_path).json()
    def statistics(self):
        return self.client.get(settings.teamcenter_stats_path).json()
