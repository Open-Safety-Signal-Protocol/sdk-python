# OSSP Python SDK (Reference)

CloudEvents-first client for emitting OSSP events.

## Install

```bash
pip install ossp-sdk
```

## Quick Start

```python
from ossp_sdk.client import OSSPClient

client = OSSPClient(
    source_uri="urn:example:app:chatbot-prod",
    collector_endpoint=None  # If None, events are logged locally
)

event = client.emit(
    event_type="ai.safety.guardrail.interaction",
    resource={"model_id": "gpt-4o", "environment": "production"},
    data={"action_taken": "block", "reason": "PII detected", "severity": "high"},
    subject="urn:model:gpt-4o"
)
print(event)
```

## CLI Example

You can emit the sample event directly from the repository:

```bash
python sdk-python/examples/send_event.py --print
```

Use `--collector-endpoint` (and optional `--auth-token`) to forward the CloudEvent to a collector, and `--log-level` to adjust verbosity.

## Validation (optional)

```bash
pip install "ossp-sdk[validate]"
```

Set the `OSSP_VALIDATE` environment variable and point `OSSP_SCHEMA_DIR` to the spec repository path `schema/v1.0.0` to validate payloads locally.

If offline, pre-load draft 2020-12 metaschema or vendor the metas under specification/schema/meta/2020-12/.
