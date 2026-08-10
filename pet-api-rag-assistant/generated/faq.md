# Frequently Asked Questions

## Getting Started

**What is the base URL for the API?**
All requests must be prefixed with `https://petstore3.swagger.io/api/v3`. This applies to every endpoint documented in this guide.

**What can I do with the Petstore Pet API?**
The API supports full CRUD operations on pet records using standard HTTP methods: `GET` to retrieve pet data, `POST` to create a new pet, `PUT` to update pet info, and `DELETE` to remove a pet record.

**Can I try the API without setting up my own client?**
Yes, you can visit the interactive Swagger UI at [petstore3.swagger.io](https://petstore3.swagger.io) to test endpoints directly in your browser.

## Authentication

**Do I need to authenticate to use the API?**
Most `GET` endpoints do not require authentication. Write and delete operations may accept or require credentials in production, though the public demo environment does not enforce authentication on most routes.

**How does the `api_key` header work?**
`DELETE /pet/{petId}` accepts an optional `api_key` header for authorization, e.g. `api_key: special-key`. Production deployments should use either the API Key or OAuth 2.0 (`Authorization: Bearer <token>`) mechanisms described in the authentication reference.

**Is OAuth 2.0 supported?**
Yes, OAuth 2.0 is listed as a supported auth mechanism, using the `Authorization` header with a `Bearer <token>` value, intended for production deployments.

## Request & Response Format

**What content types does the API support?**
The API supports **JSON** (preferred) or **XML**. Set `Content-Type` and `Accept` headers to `application/json`, or to `application/xml` if you need XML support.

**What does a Pet object look like?**
A Pet object includes `id` (integer, optional), `name` (string, **required**), `category` (object with `id`/`name`, optional), `photoUrls` (array of strings, **required**), `tags` (array of objects with `id`/`name`, optional), and `status` (enum: `available`, `pending`, `sold`, optional).

**What fields are required when creating a pet?**
When calling `POST /pet`, the request body must contain at minimum the pet's `name` and at least one `photoUrls` entry.

## Endpoints

**How do I retrieve a specific pet?**
Use `GET /pet/{petId}` with the pet's numeric ID in the path, e.g. `GET /pet/12345`. It returns the full pet object on `200 OK` or `404` if the pet is not found.

**How do I search for pets by status or tags?**
Use `GET /pet/findByStatus?status=available` to filter by status (`available`, `pending`, `sold`), or `GET /pet/findByTags?tags=friendly&tags=energetic` to filter by one or more repeated `tags` query parameters.

**What's the difference between updating a pet with `PUT /pet` versus `POST /pet/{petId}`?**
`PUT /pet` updates a pet using a full JSON body where the `id` field must match an existing record. `POST /pet/{petId}` instead updates only `name` and/or `status` using URL-encoded form data (`Content-Type: application/x-www-form-urlencoded`).

**How do I delete a pet?**
Send `DELETE /pet/{petId}` with the pet's ID in the path and optionally an `api_key` header for authorization. It returns `200 OK` on success, `400` for an invalid pet ID, or `404` if the pet isn't found.

## Errors & Status Codes

**What does a `400` response mean?**
`400 Bad Request` means the input was invalid — the request syntax is malformed, a required field is missing, or an ID/value supplied (like `petId` or `status`) is not valid.

**What does a `404` response mean?**
`404 Not Found` means the requested pet resource does not exist, such as when calling `GET /pet/{petId}` or `DELETE /pet/{petId}` with an ID that isn't in the store.

**When would I get a `405` response?**
`405 Method Not Allowed` occurs when the HTTP method isn't supported for the endpoint, or in the case of `POST /pet/{petId}` and `PUT /pet`, when the submitted form data or pet data fails server-side validation.