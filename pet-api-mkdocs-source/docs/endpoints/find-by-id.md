# Find Pet by ID

<span class="api-method get">GET</span> `/pet/{petId}`

Retrieves a single pet by its unique numeric ID.

## Path Parameters

| Name | Type | Required | Description |
|---|---|---|---|
| `petId` | integer (int64) | **Required** | Unique ID of the pet to retrieve |

## Example Request

```http
GET /pet/12345
```

## Example Response (200 OK)

```json
{
  "id": 12345,
  "name": "Rover",
  "category": { "id": 1, "name": "Dogs" },
  "photoUrls": ["https://example.com/rover.jpg"],
  "tags": [{ "id": 1, "name": "friendly" }],
  "status": "available"
}
```

## Responses

| Status | Meaning |
|---|---|
| `200 OK` | Successful. Returns the pet object. |
| `400` | Invalid ID supplied. The ID must be a positive integer. |
| `404` | Pet not found |

---

<span class="next-link">→ [Update Pet with Form Data (POST)](update-by-form.md)</span>
