from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time


# Define Metrics
REQUEST_COUNT = Counter('http_requets_total', 'Total_HTTP_Requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP_Request_Latency', ['method', 'endpoint'])

class PrometheusMiddleware(BaseHTTPMiddleware):  #el function el bnady 3leha ba3d ma anady 3al endpoint 3la tool
    async def dispatch(self, request:Request, call_next):

        start_time = time.time()

        response = await call_next(request)

        #Record metrics after request is processed
        duration = time.time() - start_time
        endpoint = request.url.path  #eg: process/1

        REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, status=response.status_code).inc()
        REQUEST_LATENCY.labels(method=request.method, endpoint=endpoint).observe(duration)                                   

        return response

def setup_metrics(app: FastAPI):
        """
        Setup Prometheus metrics middleware and endpoint
        """
        # Add Prometheus middleware
        app.add_middleware(PrometheusMiddleware)
                  #bnediha esm 34wa2y 34an yb2a sa3b 7ad ywslha
        @app.get("/TrhBVe_m5gg2002_E5VVqS", include_in_schema=False)
        def metrics():       #btbos 3la a5r e7sa2yat prometheus client lmaha w tedihalo fe sora y2blha
            return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
