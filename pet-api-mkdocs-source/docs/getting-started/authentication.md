# Authentication

Certain endpoints (such as `DELETE /pet/{petId}`) accept an optional `api_key` header for authorization. While the Petstore demo environment does not enforce authentication on most routes, production deployments should use the **OAuth 2.0** or **API Key** mechanisms described in the following table.

| Auth Type | Header / Field | Example |
|---|---|---|
| API Key | `api_key` (header) | `api_key: special-key` |
| OAuth 2.0 | `Authorization` (header) | `Bearer <token>` |

!!! note
    Most read endpoints (`GET`) in this guide do not require authentication. Write and delete operations may require an API key in production environments even though the public demo does not enforce it.
