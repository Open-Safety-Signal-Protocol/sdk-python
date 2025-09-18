"""Example script to emit an OSSP event."""

from __future__ import annotations

import argparse
import json
import logging

from ossp_sdk.client import OSSPClient


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Emit a sample OSSP guardrail event.")
    parser.add_argument(
        "--collector-endpoint",
        dest="collector_endpoint",
        help="Optional collector endpoint to POST the CloudEvent to.",
    )
    parser.add_argument(
        "--auth-token",
        dest="auth_token",
        help="Optional bearer token for authenticated collectors.",
    )
    parser.add_argument(
        "--print",
        dest="print_event",
        action="store_true",
        help="Pretty-print the emitted CloudEvent to stdout.",
    )
    parser.add_argument(
        "--log-level",
        dest="log_level",
        default="INFO",
        help="Logging level (default: INFO).",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.INFO))

    client = OSSPClient(
        source_uri="urn:example:app:chatbot-prod",
        collector_endpoint=args.collector_endpoint,
        auth_token=args.auth_token,
    )

    event = client.emit(
        event_type="ai.safety.guardrail.interaction",
        resource={"model_id": "gpt-4o", "environment": "production"},
        data={"action_taken": "block", "reason": "PII detected", "severity": "high"},
        subject="urn:model:gpt-4o",
    )

    if args.print_event:
        print(json.dumps(event, indent=2))


if __name__ == "__main__":
    main()
