# Pet Data Model

The following describes the full **Pet** object returned or accepted by the API.

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | integer (int64) | Optional | Unique identifier for the pet |
| `name` | string | **Required** | Name of the pet (e.g., "Rover") |
| `category` | object | Optional | Category object: `{ id, name }` |
| `photoUrls` | array[string] | **Required** | List of photo URLs for the pet |
| `tags` | array[object] | Optional | List of tag objects: `[ { id, name } ]` |
| `status` | string (enum) | Optional | Pet availability: `available` \| `pending` \| `sold` |

## Full Schema Example

```json
{
  "id": 12345,
  "name": "Rover",
  "category": {
    "id": 1,
    "name": "Dogs"
  },
  "photoUrls": [
    "https://example.com/photos/rover_main.jpg"
  ],
  "tags": [
    { "id": 1, "name": "friendly" },
    { "id": 2, "name": "trained" }
  ],
  "status": "available"
}
```

!!! tip "Need help?"
    Visit the interactive Swagger UI at [petstore3.swagger.io](https://petstore3.swagger.io) to test endpoints live in your browser.
