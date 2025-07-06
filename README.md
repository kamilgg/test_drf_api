# Wallet API

A REST API service for managing wallets and transactions, built with Django REST Framework.

## Features

- **Wallet Management**: Create, read, update, and delete wallet entities
- **Transaction Processing**: Record transactions that affect wallet balances
- **JSON:API Specification**: Follows the JSON:API standard for consistent API design
- **Filtering & Sorting**: Filter transactions by various parameters and sort results
- **Pagination**: Paginated API responses for better performance
- **API Documentation**: Swagger and ReDoc interfaces for exploring the API
- **Comprehensive Test Coverage**: Extensive test suite for models and API endpoints

## Technologies

- Python 3.12
- Django 5.2
- Django REST Framework
- PostgreSQL
- Docker & Docker Compose
- JSON:API specification
- Swagger/ReDoc for API documentation

## Requirements

- Docker and Docker Compose

## Quick Start

1. Clone the repository
2. Run the application using the provided script:

For Unix/Linux/macOS:
```bash
chmod +x run.sh  # Make the script executable (first time only)
./run.sh
```

For Windows:
```cmd
run.bat
```

These scripts will start the application using Docker Compose.

## Manual Setup

If you prefer to run commands manually:

1. Clone the repository
2. Start the services:

```bash
docker-compose up -d
```

3. The API will be available at http://localhost:8000/api/
4. API documentation is available at:
   - Swagger UI: http://localhost:8000/api/docs/
   - ReDoc: http://localhost:8000/api/redoc/

## API Endpoints

### Wallets

- `GET /api/wallets/` - List all wallets
- `POST /api/wallets/` - Create a new wallet
- `GET /api/wallets/{id}/` - Get a specific wallet
- `PATCH /api/wallets/{id}/` - Update a wallet
- `DELETE /api/wallets/{id}/` - Delete a wallet

### Transactions

- `GET /api/transactions/` - List all transactions
- `POST /api/transactions/` - Create a new transaction
- `GET /api/transactions/{id}/` - Get a specific transaction
- `PATCH /api/transactions/{id}/` - Update a transaction
- `DELETE /api/transactions/{id}/` - Delete a transaction

## Filtering and Sorting

### Transaction Filters

- `filter[wallet]` - Filter by wallet ID
- `filter[txid]` - Filter by transaction ID (partial match)
- `filter[amount_min]` - Filter by minimum amount
- `filter[amount_max]` - Filter by maximum amount

### Sorting

- `sort=amount` - Sort by amount (ascending)
- `sort=-amount` - Sort by amount (descending)
- `sort=created_at` - Sort by creation date (ascending)
- `sort=-created_at` - Sort by creation date (descending)

## Business Rules

- Wallet balance is calculated as the sum of all related transactions
- Wallet balance cannot be negative
- Transaction IDs (txid) must be unique

## Testing

The project includes comprehensive tests for models, business logic, and API endpoints. To run tests:

```bash
docker-compose exec web pytest
```

OR

```bash
pip install -r requirements.txt

pytest
```

## Development

The project uses:
- Black for code formatting
- Flake8 for linting
- Pytest for testing
