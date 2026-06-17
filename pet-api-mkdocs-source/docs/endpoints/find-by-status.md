# Find Pets by Status

<span class="api-method get">GET</span> `/pet/findByStatus`

Returns pets filtered by their availability status. Multiple statuses can be supplied.

## Query Parameters

| Name | Type | Required | Description |
|---|---|---|---|
| `status` | string (enum) | Optional | Filter by status: `available`, `pending`, `sold` |

## Example Request

```http
GET /pet/findByStatus?status=available
```

## Example Response (200 OK)

```json
[
  {
    "id": 12345,
    "name": "Rover",
    "status": "available",
    "photoUrls": ["https://example.com/rover.jpg"]
  },
  {
    "id": 67890,
    "name": "Bella",
    "status": "available",
    "photoUrls": ["https://example.com/bella.jpg"]
  }
]
```

## Responses

| Status | Meaning |
|---|---|
| `200 OK` | Successful. Returns an array of pets. |
| `400` | Invalid status value supplied |

---

<span class="next-link">→ [Find Pets by Tags (GET)](find-by-tags.md)</span>
