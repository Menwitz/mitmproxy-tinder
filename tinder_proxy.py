# tinder_proxy.py
# This mitmproxy add-on intercepts Tinder API requests to modify geolocation data.
# Specifically, when a JSON payload contains "lat" and "lon", it replaces them
# with coordinates for Williamsburg, Brooklyn: 40.7081 (lat) and -73.9571 (lon).

from mitmproxy import http
import json

class TinderInterceptor:
    def request(self, flow: http.HTTPFlow) -> None:
        # Only process requests to the Tinder API (adjust the domain if needed).
        if "api.gotinder.com" in flow.request.pretty_url:
            print(f"Intercepted Tinder API request: {flow.request.pretty_url}")

            # Only target POST requests with JSON bodies.
            if flow.request.method.upper() == "POST":
                content_type = flow.request.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    try:
                        # Parse the JSON payload.
                        data = json.loads(flow.request.get_text())
                        
                        # Check if the payload contains geolocation keys.
                        # Adjust the key names if necessary.
                        if "lat" in data and "lon" in data:
                            original_lat = data["lat"]
                            original_lon = data["lon"]
                            
                            # Set new coordinates for Williamsburg, Brooklyn.
                            data["lat"] = 40.7081
                            data["lon"] = -73.9571
                            
                            # Replace the request body with the updated JSON.
                            flow.request.set_text(json.dumps(data))
                            
                            print(f"Modified geolocation: ({original_lat}, {original_lon}) -> (40.7081, -73.9571)")
                    except Exception as e:
                        # Log errors in JSON processing.
                        print(f"Error processing JSON payload: {e}")

# Register the interceptor as a mitmproxy add-on.
addons = [
    TinderInterceptor()
]
