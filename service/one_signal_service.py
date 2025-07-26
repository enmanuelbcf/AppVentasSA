import httpx

ONESIGNAL_APP_ID = "9c4538f3-c341-4376-82eb-e879d731f17e"
ONESIGNAL_REST_API_KEY = "os_v2_app_trctr46difbxnaxl5b45omprp3iedxhtksruizul3iacpogjklroqvup5qlutbpjwtfkd2midhjepiwftzsrvtdix4pj5u4ttssjbyi"
ONESIGNAL_API_URL = "https://onesignal.com/api/v1/notifications"

async def send_push_notification(player_ids: list[str], heading: str, content: str):
    if not player_ids:
        raise ValueError("La lista de player_ids no puede estar vacía")

    payload = {
        "app_id": ONESIGNAL_APP_ID,
        "include_external_user_ids": player_ids,
        "headings": {"en": heading},
        "contents": {"en": content}
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {ONESIGNAL_REST_API_KEY}"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(ONESIGNAL_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as exc:
        return {
            "error": "HTTP error",
            "status_code": exc.response.status_code,
            "details": exc.response.text
        }
    except httpx.RequestError as exc:
        return {
            "error": "Request error",
            "details": str(exc)
        }
    except Exception as exc:
        return {
            "error": "Unexpected error",
            "details": str(exc)
        }
