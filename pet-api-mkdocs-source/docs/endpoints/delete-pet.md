# Delete a Pet

<span class="api-method delete">DELETE</span> `/pet/{petId}`

Permanently removes a pet record from the store by its ID. An optional `api_key` header can be passed for authorization purposes.

## Path Parameters

| Name | Type | Required | Description |
|---|---|---|---|
| `petId` | integer (int64) | **Required** | ID of the pet to delete |

## Header Parameters

| Name | Type | Required | Description |
|---|---|---|---|
| `api_key` | string | Optional | API key for authorization |

## Example Request

```http
DELETE /pet/12345
api_key: special-key
```

## Responses

| Status | Meaning |
|---|---|
| `200 OK` | Pet deleted successfully |
| `400` | Invalid pet ID supplied |
| `404` | Pet not found |

---

<span class="next-link">→ [Endpoint Summary](../reference/summary.md)</span>
