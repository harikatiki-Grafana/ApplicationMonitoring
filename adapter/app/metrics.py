from prometheus_client import Gauge, Counter
from .config import settings
from .teamcenter_client import TeamcenterClient

service_up = Gauge("tc_service_up", "Teamcenter service availability", ["service"])
queue_depth = Gauge("tc_job_queue_depth", "Teamcenter job queue depth", ["queue"])
http_requests = Counter("tc_http_requests_total", "Teamcenter HTTP requests", ["status_class"])

client = TeamcenterClient()

def collect():
    data = client.statistics()
    for item in data.get("services", []):
        service_up.labels(item["name"]).set(1 if item.get("up") else 0)
    for queue, depth in data.get("job_queues", {}).items():
        queue_depth.labels(queue).set(depth)
