# API Endpoint Summary

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| <span class="api-method post small">POST</span> | `/pet` | [Add a new pet](../endpoints/add-pet.md) | Optional |
| <span class="api-method put small">PUT</span> | `/pet` | [Update an existing pet](../endpoints/update-pet.md) | Optional |
| <span class="api-method get small">GET</span> | `/pet/findByStatus` | [Find pets by status](../endpoints/find-by-status.md) | No |
| <span class="api-method get small">GET</span> | `/pet/findByTags` | [Find pets by tags](../endpoints/find-by-tags.md) | No |
| <span class="api-method get small">GET</span> | `/pet/{petId}` | [Find pet by ID](../endpoints/find-by-id.md) | No |
| <span class="api-method post small">POST</span> | `/pet/{petId}` | [Update pet via form data](../endpoints/update-by-form.md) | Optional |
| <span class="api-method delete small">DEL</span> | `/pet/{petId}` | [Delete a pet](../endpoints/delete-pet.md) | Optional (api_key) |
