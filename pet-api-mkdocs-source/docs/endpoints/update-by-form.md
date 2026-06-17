# Update Pet with Form Data

<span class="api-method post">POST</span> `/pet/{petId}`

Updates an existing pet's `name` or `status` using URL-encoded form data rather than a JSON body.

## Path Parameters

| Name | Type | Required | Description |
|---|---|---|---|
| `petId` | integer (int64) | **Required** | ID of the pet to update |

## Form Parameters

| Name | Type | Required | Description |
|---|---|---|---|
| `name` | string | Optional | Updated name of the pet |
| `status` | string | Optional | Updated status: `available`, `pending`, `sold` |

## Example Request

```http
POST /pet/12345
Content-Type: application/x-www-form-urlencoded

name=Rover+Jr&status=pending
```

## Responses

| Status | Meaning |
|---|---|
| `200 OK` | Pet updated successfully |
| `405` | Invalid input. The form data failed validation. |

---

<span class="next-link">→ [Delete a Pet (DELETE)](delete-pet.md)</span>
