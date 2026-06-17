# Add a New Pet

<span class="api-method post">POST</span> `/pet`

Adds a new pet record to the store. The request body must contain the pet's name and at least one photo URL. Returns the created pet object on success.

## Request Body

```json title="application/json"
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

| Status | Meaning | Notes |
|---|---|---|
| `200 OK` | Pet added successfully | Returns the pet object |
| `400` | Invalid input | Check required fields |

---

<span class="next-link">→ [Update an Existing Pet (PUT /pet)](update-pet.md)</span>
