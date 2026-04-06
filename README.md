# NyumbaHub Backend

Django + Django REST Framework backend for the NyumbaHub rental property management system.

---

## Requirements

- Python 3.10+
- MySQL 8.0+
- pip

---

## Setup (Mac)

### 1. Clone and enter the project
```bash
cd nyumbahub_backend
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```
> If mysqlclient fails, install MySQL first: `brew install mysql pkg-config`

### 4. Create the MySQL database
```sql
mysql -u root -p
CREATE DATABASE nyumbahub_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 5. Configure settings
Edit `nyumbahub/settings.py` and update the DATABASES block with your MySQL credentials.

### 6. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create a superuser (admin)
```bash
python manage.py createsuperuser
```

### 8. Start the development server
```bash
python manage.py runserver
```

API is now available at: `http://localhost:8000/api/`
Admin panel: `http://localhost:8000/admin/`

---

## API Endpoints Reference

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login/` | Login — returns access + refresh tokens |
| POST | `/api/auth/logout/` | Logout (blacklists refresh token) |
| POST | `/api/auth/token/refresh/` | Get new access token using refresh token |
| GET | `/api/auth/me/` | Get current user profile |
| PATCH | `/api/auth/me/` | Update current user profile |
| POST | `/api/auth/change-password/` | Change password |
| GET | `/api/auth/users/` | List all users (admin only) |
| POST | `/api/auth/users/` | Create user (admin only) |
| GET/PATCH/DELETE | `/api/auth/users/<id>/` | Manage user (admin only) |

### Properties
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/properties/houses/` | List all houses |
| POST | `/api/properties/houses/` | Create a house |
| GET | `/api/properties/houses/<id>/` | Get house + all its rooms |
| PATCH/PUT | `/api/properties/houses/<id>/` | Update house |
| DELETE | `/api/properties/houses/<id>/` | Delete house |
| GET | `/api/properties/houses/<id>/rooms/` | List rooms for a house |
| GET | `/api/properties/rooms/` | List all rooms (filterable by status, house) |
| POST | `/api/properties/rooms/` | Create a room |
| GET/PATCH/DELETE | `/api/properties/rooms/<id>/` | Manage a room |
| PATCH | `/api/properties/rooms/<id>/status/` | Quick status update (vacant/occupied/maintenance) |
| GET | `/api/properties/occupancy/` | Full occupancy overview for dashboard |

### Tenants
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tenants/` | List tenants (filter by status, room, house) |
| POST | `/api/tenants/` | Register new tenant (auto-sets room to occupied) |
| GET | `/api/tenants/<id>/` | Get tenant detail + payment history |
| PATCH/PUT | `/api/tenants/<id>/` | Update tenant (setting status=former auto-vacates room) |
| DELETE | `/api/tenants/<id>/` | Delete tenant |

### Payments
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/payments/` | List payments (filter by month, year, status, tenant) |
| POST | `/api/payments/` | Record a payment |
| GET/PATCH/DELETE | `/api/payments/<id>/` | Manage a payment |
| GET | `/api/payments/summary/?month=6&year=2025` | Monthly totals + all payment records |
| GET | `/api/payments/unpaid/?month=6&year=2025` | Tenants with unpaid/partial rent |
| GET | `/api/payments/expenses/` | List expenses (filter by category, house, year, month) |
| POST | `/api/payments/expenses/` | Add an expense |
| GET/PATCH/DELETE | `/api/payments/expenses/<id>/` | Manage an expense |

### Reports
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/reports/dashboard/` | Main dashboard — occupancy + this month's income/expenses |
| GET | `/api/reports/monthly/?year=2025` | Monthly income vs expenses for a year |
| GET | `/api/reports/yearly/` | Year-by-year financial summary |
| GET | `/api/reports/by-house/?year=2025` | Per-house income, expenses, occupancy |
| GET | `/api/reports/expenses/by-category/?year=2025` | Expense breakdown by category |
| GET | `/api/reports/room/<id>/history/` | All tenants who ever occupied a room |

---

## Authentication Flow (for React frontend)

```
1. POST /api/auth/login/ → { access, refresh, user }
2. Store access token in memory (or localStorage)
3. Add header to every request: Authorization: Bearer <access_token>
4. When access token expires (8h), POST /api/auth/token/refresh/ with { refresh }
5. On logout, POST /api/auth/logout/ with { refresh } to blacklist token
```

---

## Filtering Examples

```
GET /api/properties/rooms/?status=vacant
GET /api/properties/rooms/?house=2&status=occupied
GET /api/tenants/?status=active&search=john
GET /api/payments/?payment_month=6&payment_year=2025&status=unpaid
GET /api/payments/expenses/?category=maintenance&year=2025
```

---

## Project Structure

```
nyumbahub_backend/
├── nyumbahub/          # Project config
│   ├── settings.py
│   └── urls.py
├── accounts/           # Auth + user management
├── properties/         # Houses + rooms
├── tenants/            # Tenant management
├── payments/           # Rent payments + expenses
├── reports/            # Dashboard + financial reports
├── requirements.txt
└── manage.py
```
