#!/usr/bin/env python3
import sys
import urllib.request
import json


def check_url(url: str, expected_status: int = 200) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "HealthCheck/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.getcode()
            if status == expected_status:
                print(f"✔ [PASS] {url} returned HTTP {status}")
                return True
            else:
                print(f"✖ [FAIL] {url} returned HTTP {status} (expected {expected_status})")
                return False
    except Exception as e:
        print(f"✖ [ERROR] {url} failed with error: {e}")
        return False


def main():
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    print(f"Executing Deep System Health Check against: {base_url}")
    
    health_ok = check_url(f"{base_url}/health")
    ready_ok = check_url(f"{base_url}/ready")
    latest_ok = check_url(f"{base_url}/api/v1/latest")
    forecast_ok = check_url(f"{base_url}/api/v1/forecast?quarters=8&model_type=ARIMA-LSTM")

    if health_ok and ready_ok and latest_ok and forecast_ok:
        print("\n🎉 ALL HEALTH CHECKS PASSED!")
        sys.exit(0)
    else:
        print("\n❌ SYSTEM HEALTH CHECK FAILED!")
        sys.exit(1)


if __name__ == "__main__":
    main()
