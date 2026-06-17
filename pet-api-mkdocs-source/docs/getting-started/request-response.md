# Request and Response Format

All request and response bodies use **JSON** (preferred) or **XML**. Include the appropriate `Content-Type` and `Accept` headers with each request.

```http
Content-Type: application/json
Accept:       application/json
```

All endpoint examples in this guide use JSON. If you need XML support, set the `Content-Type` and `Accept` headers to `application/xml` instead.
