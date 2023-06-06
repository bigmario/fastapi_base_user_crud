# FastAPI Base User CRUD
FastAPI REST API for user management with email/password & JWT authentication
<br>
Github actions support (Linting with flake8 y testing with pytest)

### 1. Set Environmient Variables
```bash
#create a new  environment variables file 
$ cp .env.example .env
```
then set the corresponding values to:
```text
DB_PASSWORD=
ADMIN_PASSWORD=

MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_FROM=
MAIL_TO=
MAIL_PORT=
MAIL_SERVER=
MAIL_FROM_NAME=
```

### 2. Deployment on Docker
```bash
# run all services
$ docker compose up --build -d
```

### OpenAPI Documentation
`http://localhost:8000/docs`

### Testing
```bash
$ pytest -vv
```

### Testing Coverage
```bash
$ coverage run -m pytest 
$ coverage report 
```

