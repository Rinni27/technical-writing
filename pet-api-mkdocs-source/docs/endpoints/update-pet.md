# Update an Existing Pet

<span class="api-method put">PUT</span> `/pet`

Updates an existing pet's data. The `id` field in the request body must match an existing pet record.

## Request Body

```json title="application/json"
{
  "id": 12345,
  "name": "Rover Updated",
  "category": { "id": 1, "name": "Dogs" },
  "photoUrls": ["https://example.com/rover2.jpg"],
  "tags": [{ "id": 2, "name": "energetic" }],
  "status": "sold"
}
```

## Responses

| Status | Meaning | Notes |
|---|---|---|
| `200 OK` | Pet updated successfully | Returns updated pet object |
| `400` | Invalid ID supplied | Verify the pet ID is a valid integer |
| `404` | Pet not found | No pet matches the given ID |
| `405` | Validation exception | Data failed server-side validation |

---

<span class="next-link">→ [Find Pets by Status (GET)](find-by-status.md)</span>
