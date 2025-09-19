"""Tests for OSSP client."""

import json
import pytest
from ossp_sdk.client import OSSPClient


def test_client_initialization():
    """Test client can be initialized."""
    client = OSSPClient(
        source_uri="urn:test:app",
        collector_endpoint=None
    )
    assert client.source_uri == "urn:test:app"
    assert client.collector_endpoint is None


def test_emit_event_structure():
    """Test that emitted events have correct CloudEvents structure."""
    client = OSSPClient(
        source_uri="urn:test:app",
        collector_endpoint=None
    )

    event = client.emit(
        event_type="ai.safety.guardrail.interaction",
        resource={"model_id": "test-model", "environment": "test"},
        data={"action_taken": "block", "reason": "test", "severity": "high"}
    )

    # Check CloudEvents required fields
    assert event["specversion"] == "1.0"
    assert "id" in event
    assert event["source"] == "urn:test:app"
    assert event["type"] == "ai.safety.guardrail.interaction"
    assert "time" in event
    assert event["datacontenttype"] == "application/json"
    assert "dataschema" in event

    # Check data structure
    assert "data" in event
    assert "resource" in event["data"]
    assert event["data"]["resource"]["model_id"] == "test-model"
    assert event["data"]["action_taken"] == "block"


def test_schema_url_format():
    """Test that schema URLs point to ossp.io."""
    client = OSSPClient(source_uri="urn:test:app")

    event = client.emit(
        event_type="ai.safety.guardrail.interaction",
        resource={"model_id": "test", "environment": "test"},
        data={"action_taken": "warn"}
    )

    expected_schema = "https://ossp.io/schema/v1.0.0/ai.safety.guardrail.interaction.schema.json"
    assert event["dataschema"] == expected_schema


def test_custom_dataschema():
    """Test custom dataschema override."""
    client = OSSPClient(source_uri="urn:test:app")

    custom_schema = "https://example.com/custom.schema.json"
    event = client.emit(
        event_type="ai.safety.guardrail.interaction",
        resource={"model_id": "test", "environment": "test"},
        data={"action_taken": "warn"},
        dataschema=custom_schema
    )

    assert event["dataschema"] == custom_schema


def test_subject_field():
    """Test subject field is included when provided."""
    client = OSSPClient(source_uri="urn:test:app")

    event = client.emit(
        event_type="ai.safety.guardrail.interaction",
        resource={"model_id": "test", "environment": "test"},
        data={"action_taken": "warn"},
        subject="urn:model:test-model"
    )

    assert event["subject"] == "urn:model:test-model"


def test_json_serializable():
    """Test that events can be JSON serialized."""
    client = OSSPClient(source_uri="urn:test:app")

    event = client.emit(
        event_type="ai.safety.guardrail.interaction",
        resource={"model_id": "test", "environment": "test"},
        data={"action_taken": "warn"}
    )

    # Should not raise exception
    json_str = json.dumps(event)
    parsed = json.loads(json_str)
    assert parsed["type"] == "ai.safety.guardrail.interaction"