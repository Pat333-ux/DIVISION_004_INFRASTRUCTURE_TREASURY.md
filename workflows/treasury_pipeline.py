Python
#!/usr/bin/env python3
"""
Division 004 — Treasury Allocation & Compute Provisioning Pipeline
BEAST System 3.0
"""

import json
import uuid
from datetime import datetime, timezone
from jsonschema import validate, ValidationError

class Division004Pipeline:
    def __init__(self, schema_path="schemas/treasury_schema.json"):
        with open(schema_path, "r", encoding="utf-8") as f:
            self.schema = json.load(f)

    def process_allocation_request(self, requesting_division: str, allocation_type: str, resource_units: int, compliance_approval_hash: str) -> dict:
        """Processes and validates a resource or treasury allocation request."""
        request_record = {
            "request_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "requesting_division": requesting_division,
            "allocation_type": allocation_type,
            "resource_units": resource_units,
            "compliance_approval_hash": compliance_approval_hash
        }

        # Validate against Division 004 treasury schema
        try:
            validate(instance=request_record, schema=self.schema)
            print(f"[+] SUCCESS: Allocation request {request_record['request_id']} approved and dispatched.")
            return request_record
        except ValidationError as e:
            print(f"[!] REJECTED: Request violates treasury schema constraints: {e.message}")
            raise e

if __name__ == "__main__":
    print("[*] Initializing Division 004 Treasury & Compute Pipeline...")
    pipeline = Division004Pipeline()
    
    # Sample valid allocation payload with dummy Division 003 approval hash
    dummy_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    
    try:
        sample_request = pipeline.process_allocation_request(
            requesting_division="DIV_001",
            allocation_type="COMPUTE_CPU_HOURS",
            resource_units=500,
            compliance_approval_hash=dummy_hash
        )
        print(json.dumps(sample_request, indent=2))
    except Exception:
        print("[!] Pipeline test execution halted due to validation failure.")
File Name: tests/test_infrastructure.py
Python
import json
import os
import pytest
from jsonschema import validate, ValidationError

def test_treasury_schema_exists():
    assert os.path.exists("schemas/treasury_schema.json"), "treasury_schema.json is missing"

def test_valid_treasury_request():
    schema_path = "schemas/treasury_schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    valid_request = {
        "request_id": "c9bf9e57-1685-4c89-bafb-ff58a36bfba1",
        "timestamp": "2026-10-22T14:30:00Z",
        "requesting_division": "DIV_002",
        "allocation_type": "TREASURY_ESCROW_DISBURSEMENT",
        "resource_units": 10000,
        "compliance_approval_hash": "a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890"
    }

    # Should validate without raising an error
    validate(instance=valid_request, schema=schema)

def test_invalid_compliance_hash_fails():
    schema_path = "schemas/treasury_schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    invalid_request = {
        "request_id": "c9bf9e57-1685-4c89-bafb-ff58a36bfba1",
        "timestamp": "2026-10-22T14:30:00Z",
        "requesting_division": "DIV_003",
        "allocation_type": "NODE_PROVISIONING",
        "resource_units": 5,
        "compliance_approval_hash": "invalid-short-hash" # Fails regex pattern check
    }

    with pytest.raises(ValidationError):
        validate(instance=invalid_request, schema=schema)
