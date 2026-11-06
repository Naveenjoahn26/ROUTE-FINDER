import sys
import json
from services.route_service import find_route

def run_route_finder(start_lat=10.7905, start_lon=78.7047, end_lat=10.8150, end_lon=78.6920):
    print("=" * 60)
    print("           🧭 SafeRoute AI — Route Finding Engine")
    print("=" * 60)
    print(f"[*] Origin Coordinates     : Latitude {start_lat}, Longitude {start_lon}")
    print(f"[*] Destination Coordinates: Latitude {end_lat}, Longitude {end_lon}")
    print("[*] Running A* pathfinding with ML Risk Model...")
    
    results = find_route(start_lat, start_lon, end_lat, end_lon)
    
    safe = results.get("safe_route")
    short = results.get("short_route")
    
    print("\n" + "-" * 60)
    print("                        ROUTE RESULTS")
    print("-" * 60)
    
    if safe and safe.get("summary"):
        s = safe["summary"]
        coords_count = len(safe.get("coords", []))
        print(f"🛡️  SAFEST ROUTE (Recommended):")
        print(f"   • Total Distance   : {s['distance_km']} km")
        print(f"   • Risk Score       : {s['risk_percent']}%")
        print(f"   • Safety Level     : {s['safety_level']}")
        print(f"   • Waypoint Nodes   : {coords_count} GPS coordinates")
    else:
        print("🛡️  SAFEST ROUTE: No walkable path found.")
        
    print()
    if short and short.get("summary"):
        s = short["summary"]
        coords_count = len(short.get("coords", []))
        print(f"⚡ SHORTEST ROUTE (Fastest):")
        print(f"   • Total Distance   : {s['distance_km']} km")
        print(f"   • Risk Score       : {s['risk_percent']}%")
        print(f"   • Safety Level     : {s['safety_level']}")
        print(f"   • Waypoint Nodes   : {coords_count} GPS coordinates")
    else:
        print("⚡ SHORTEST ROUTE: No walkable path found.")
        
    print("-" * 60)
    if safe and short and safe.get("summary") and short.get("summary"):
        dist_diff = round(safe["summary"]["distance_km"] - short["summary"]["distance_km"], 2)
        print(f"💡 RECOMMENDATION: Safest route adds only {abs(dist_diff)} km while prioritizing safer streets.")
    print("=" * 60)

if __name__ == "__main__":
    if len(sys.argv) == 5:
        s_lat, s_lon, e_lat, e_lon = map(float, sys.argv[1:5])
        run_route_finder(s_lat, s_lon, e_lat, e_lon)
    else:
        # Default Trichy points
        run_route_finder()

