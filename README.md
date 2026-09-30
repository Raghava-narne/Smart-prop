# Smart Property Rental & Maintenance Platform

A Python-based backend system for property owners and property management companies to manage apartments, tenants, rental agreements, rent payments, maintenance requests, technician assignments, and financial reporting.

This project follows the Weekly Project-2 requirements and is designed as a real-world rental and maintenance management platform using FastAPI, SQLAlchemy, PostgreSQL, MongoDB, and REST APIs.

## Project Objective

Build a centralized backend API that helps property managers handle the complete rental and maintenance lifecycle, including:

- Property and apartment registration
- Tenant onboarding and status tracking
- Rental agreement creation and termination
- Monthly rent obligation generation and payment tracking
- Maintenance complaint logging and technician assignment
- SLA tracking for repair performance
- Audit logging and event tracking

## Features

The running application currently exposes endpoints for:

- User registration and login with JWT access-token issuance.
- Property and apartment management.
- Tenant management.
- Rental agreements and rent obligations.
- Manual payments and Razorpay payment endpoints.
- Maintenance tickets and technician management.
- Health check and interactive API documentation.

Audit history, financial reports, role-based access, SLA tracking, and scheduled
rent processing are planned improvements and are not fully implemented.

## Technology

- Python
- FastAPI and Uvicorn
- Pydantic
- SQLAlchemy
- PostgreSQL with `psycopg2`
- `python-jose` for JWT creation
- Razorpay Python SDK
- Pytest and HTTPX for testing

## Project structure

text
app/
├── api/ # API routes and request dependencies
├── core/ # Settings, token creation, and application errors
├── db/ # SQLAlchemy base, engine, and session setup
├── models/ # Database models
├── repositories/ # Database access
├── schemas/ # Request and response schemas
├── services/ # Business logic
└── main.py # FastAPI application
requirements.txt
README.md

Getting started

Requirements

- Python 3.10 or newer
- PostgreSQL
- A PostgreSQL database with tables provisioned for the application models

Install dependencies

From the project root, create and activate a virtual environment, then install
the dependencies:

powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

Configure environment

Create a `.env` file in the project root or in the `app/` directory:

dotenv
DATABASE_URL=postgresql://<user>:<password>@localhost:5432/<database>
JWT_SECRET_KEY=<replace-with-a-long-random-secret>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

Optional: required only for Razorpay payment endpoints.
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=

Create the PostgreSQL database and provision the tables before calling
database-backed endpoints. User registration also requires a role record to
already exist.

### Start the server

powershell
uvicorn app.main:app --reload

Once the server is running:

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>
- OpenAPI schema: <http://127.0.0.1:8000/openapi.json>
- Health check: <http://127.0.0.1:8000/health>

## Frontend

The React/Vite application is in `frontend/`. From PowerShell:

```powershell
Set-Location frontend
Copy-Item .env.example .env
npm install
npm run dev
```

Set `VITE_API_BASE_URL` in `frontend/.env` to the FastAPI origin. The default
is `http://localhost:8000`. The frontend signs in through `/auth/login`, reads
the JWT `sub` and `role_id` claims, resolves the role with
`GET /roles/{role_id}`, and uses the registration response or login form email
for the account display. The current API does not expose a current-user
endpoint. Login passwords must be 6–20 characters, as required by the API's
`LoginRequest` schema.

Roles are records in the database; the API does not publish role permissions.
The running API's `/roles` endpoint returned `Admin`, `ADMIN`,
`Property Manager`, `Owner`, `Tenant`, and `Technician`. The frontend uses
case-insensitive UI permission presets for those exact role names: admins
receive all exposed management modules, property managers receive operational
modules, owners get read-only property and rent summaries, tenants get
email-matched rent and maintenance views plus maintenance request creation,
and technicians get a maintenance dashboard and start action. Unknown roles
continue to fail closed. These presets only control frontend presentation and
are not a backend authorization policy. To customize them, set
`VITE_ROLE_PERMISSIONS_JSON` to a JSON object keyed by the exact `role_name`
values returned by `GET /roles`. Permission strings follow
`<module>:<action>` (for example, `dashboard:view`, `properties:view`,
`properties:create`, `properties:update`, `properties:delete`,
`agreements:terminate`, `maintenance:assign`, or `maintenance:start`). For
example, replace the placeholder key below with a role name actually returned
by the API:

```dotenv
VITE_ROLE_PERMISSIONS_JSON={"<exact role_name>":["dashboard:view","properties:view"]}
```

Restart Vite after changing the environment. The maintenance API returns an
unfiltered ticket list and does not expose a current-user-to-technician
association, so the frontend cannot limit a technician to only their assigned
tickets.

The current API does not consistently enforce authentication or role-based
authorization: only selected routes require a JWT, and the maintenance start
service checks for the `TECHNICIAN` role. In particular, role-based frontend
visibility is not a security boundary. Public registration accepts a caller
provided `role_id` and the API does not enforce role assignment policy. Secure
deployment requires backend authorization and registration policy; these are
not changed by this frontend.

The payment API has no payment collection endpoint, so the frontend supports
recording a payment and looking one up by payment ID rather than inventing a
list route. The API allows CORS requests from `http://localhost:5173` and
`http://127.0.0.1:5173`, with all methods and headers.
The API does not expose a `/users` route or a direct user-to-tenant ID link.
The tenant dashboard matches the authenticated account email to the tenant
record email and uses the matched ID only with tenant-scoped rent and ticket
routes. A tenant account whose email does not exactly match a tenant profile
is shown a profile-linking message and is not shown another tenant's records.
Tenant accounts have separate `My rent`, `Maintenance requests`, and
`Payments` navigation entries. These pages show a profile-linking prompt until
the account email matches the correct tenant record; selecting an arbitrary
tenant is intentionally not allowed.

## API endpoints

These endpoints are mounted by the current application. Use `/docs` to inspect
the request and response schemas.

| Area              | Method                   | Endpoint                                      |
| ----------------- | ------------------------ | --------------------------------------------- |
| Health            | `GET`                    | `/health`                                     |
| Authentication    | `POST`                   | `/auth/register`                              |
| Authentication    | `POST`                   | `/auth/login`                                 |
| Properties        | `GET`, `POST`            | `/properties`                                 |
| Properties        | `GET`, `PATCH`, `DELETE` | `/properties/{property_id}`                   |
| Apartments        | `GET`, `POST`            | `/properties/{property_id}/apartments`        |
| Apartments        | `GET`, `PATCH`           | `/apartments/{apartment_id}`                  |
| Apartments        | `GET`                    | `/apartments?status=AVAILABLE`                |
| Tenants           | `GET`, `POST`            | `/tenants`                                    |
| Tenants           | `GET`, `PATCH`           | `/tenants/{tenant_id}`                        |
| Tenants           | `PATCH`                  | `/tenants/{tenant_id}/deactivate`             |
| Rental agreements | `GET`, `POST`            | `/rental-agreements`                          |
| Rental agreements | `GET`                    | `/rental-agreements/{agreement_id}`           |
| Rental agreements | `PATCH`                  | `/rental-agreements/{agreement_id}/terminate` |
| Rental agreements | `GET`                    | `/apartments/{apartment_id}/current-tenant`   |
| Rent              | `POST`                   | `/rent-obligations/generate`                  |
| Rent              | `GET`                    | `/rent-obligations`                           |
| Rent              | `GET`                    | `/tenants/{tenant_id}/rent`                   |
| Payments          | `POST`                   | `/payments`                                   |
| Payments          | `GET`                    | `/payments/{payment_id}`                      |
| Payments          | `POST`                   | `/payments/razorpay/orders`                   |
| Payments          | `POST`                   | `/payments/razorpay/verify`                   |
| Maintenance       | `GET`, `POST`            | `/maintenance-tickets`                        |
| Maintenance       | `GET`                    | `/maintenance-tickets/{ticket_id}`            |
| Maintenance       | `PATCH`                  | `/maintenance-tickets/{ticket_id}/assign`     |
| Maintenance       | `PATCH`                  | `/maintenance-tickets/{ticket_id}/start`      |
| Maintenance       | `PATCH`                  | `/maintenance-tickets/{ticket_id}/resolve`    |
| Maintenance       | `PATCH`                  | `/maintenance-tickets/{ticket_id}/close`      |
| Maintenance       | `GET`                    | `/tenants/{tenant_id}/maintenance-tickets`    |
| Technicians       | `GET`, `POST`            | `/technicians`                                |
| Technicians       | `GET`                    | `/technicians/{technician_id}`                |
| Technicians       | `PATCH`                  | `/technicians/{technician_id}/availability`   |

### Authentication flow

1. Ensure the database contains a valid role.
2. Send `POST /auth/register` with `full_name`, `email`, `password`, and
   `role_id`.
3. Send `POST /auth/login` with the registered email and password.
4. Copy the returned `access_token`. For routes that require authentication,
   send it in the header as `Authorization: Bearer <access_token>`.

## Notes

This is a backend-first system intended to model a real-world property management platform. It follows the project brief for Weekly Project-2 and can be extended with authentication, role-based access control, advanced reports, and more business logic in later phases.
