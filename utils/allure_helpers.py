from __future__ import annotations

import json

import allure
import requests


def attach_api_response(response: requests.Response, name: str = "API response") -> None:
    request = response.request
    request_body = _format_body(request.body)
    response_body = _format_body(response.text)

    allure.attach(
        "\n".join(
            [
                f"{request.method} {request.url}",
                "",
                "Request headers:",
                _format_headers(dict(request.headers)),
                "",
                "Request body:",
                request_body or "<empty>",
                "",
                f"Status code: {response.status_code}",
                "",
                "Response headers:",
                _format_headers(dict(response.headers)),
                "",
                "Response body:",
                response_body or "<empty>",
            ]
        ),
        name=name,
        attachment_type=allure.attachment_type.TEXT,
    )


def _format_headers(headers: dict[str, str]) -> str:
    return "\n".join(f"{key}: {value}" for key, value in sorted(headers.items()))


def _format_body(body: bytes | str | None) -> str:
    if body is None:
        return ""

    text = body.decode("utf-8") if isinstance(body, bytes) else body
    try:
        return json.dumps(json.loads(text), indent=2, sort_keys=True)
    except (TypeError, ValueError):
        return text
