# Find Pets by Tags

<span class="api-method get">GET</span> `/pet/findByTags`

Returns pets that match one or more specified tags. Tag values are passed as repeated query parameters.

## Query Parameters

| Name | Type | Required | Description |
|---|---|---|---|
| `tags` | array[string] | **Required** | One or more tag names to filter by |

## Example Request

```http
GET /pet/findByTags?tags=friendly&tags=energetic
```

## Responses

| Status | Meaning |
|---|---|
| `200 OK` | Successful. Returns an array of matching pets. |
| `400` | Invalid tag value supplied |

---

<span class="next-link">→ [Find Pet by ID (GET)](find-by-id.md)</span>
