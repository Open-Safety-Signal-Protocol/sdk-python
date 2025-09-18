"""Example script to emit an OSSP event."""

from ossp_sdk.client import OSSPClient


def main() -> None:
    client = OSSPClient(source_uri="urn:example:app:chatbot-prod")
    client.emit(
        event_type="ai.safety.guardrail.interaction",
        resource={"model_id": "gpt-4o", "environment": "production"},
        data={"action_taken": "block", "reason": "PII detected", "severity": "high"},
        subject="urn:model:gpt-4o",
    )


if __name__ == "__main__":
    main()
