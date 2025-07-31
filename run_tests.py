#!/usr/bin/env python3
"""
Test runner for the VineSight exercise integration test.

This script runs the automated integration test that:
1. Bootstraps a fresh database
2. Loads mock data from CSV
3. Sends a request to /stats endpoint
4. Verifies the response with specific assertions

Usage:
    python run_tests.py
"""

import subprocess
import sys

def main():
    """Run the integration test"""
    print("Running VineSight Integration Test...")
    print("=" * 50)
    
    try:
        # Run pytest with the integration test
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/test_integration.py::TestIntegration::test_stats_endpoint_with_mock_data",
            "-v", "-s"
        ], capture_output=False, text=True)
        
        if result.returncode == 0:
            print("\n" + "=" * 50)
            print("✅ Test PASSED!")
            print("The integration test successfully:")
            print("- Created a fresh database")
            print("- Loaded mock data from CSV")
            print("- Made a request to /stats endpoint")
            print("- Verified the response with specific assertions")
            print("=" * 50)
        else:
            print("\n" + "=" * 50)
            print("❌ Test FAILED!")
            print("Check the output above for details.")
            print("=" * 50)
            sys.exit(1)
            
    except Exception as e:
        print(f"Error running test: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 