# 💰 FinGenius AI: Your Automated Personal CFO

## Project Title: FinGenius AI

## Brief Description

FinGenius AI is a revolutionary AI-powered personal finance assistant designed to truly automate your financial life. Going beyond simple tracking, FinGenius AI intelligently learns from your unique spending habits, income patterns, and evolving financial goals to proactively automate budgeting, optimize savings contributions, and strategically manage your investments. Think of it as your personal Chief Financial Officer, working tirelessly to grow your wealth and secure your financial future, with full transparency and consent.

Our MVP focuses on delivering core automation capabilities across budgeting, savings, and basic investment strategies, providing actionable insights and automated actions (with user approval thresholds) to help you achieve financial mastery effortlessly.

## MVP Features

The FinGenius AI MVP aims to deliver the following core functionalities:

*   **Secure User Authentication & Profile:** Robust user registration, login, and profile management.
*   **Bank Account Aggregation:** Seamless and secure connection to multiple bank accounts, credit cards, and investment accounts via Plaid.
*   **AI-Powered Transaction Categorization:** Automatically categorize transactions with high accuracy, learning from your corrections.
*   **Automated Budgeting:** AI-driven budget creation and dynamic adjustment based on real-time spending behavior. Users can set flexible thresholds for automated adjustments or receive proactive suggestions.
*   **Intelligent Savings Automation:** AI identifies optimal amounts to save and initiates transfers to your designated savings goals, adapting to your cash flow.
*   **Basic Investment Strategy Automation:** AI recommends diversified investment portfolios based on user goals and risk tolerance, with options for automated contributions and rebalancing suggestions.
*   **Financial Goal Setting & Tracking:** Define short-term and long-term financial goals (e.g., emergency fund, down payment, retirement), with AI providing progress tracking and optimized paths.
*   **Consolidated Financial Dashboard:** A clear, intuitive overview of your financial health, net worth, cash flow, and automated actions.
*   **Automation Console:** A central hub to review, approve, or adjust AI-suggested financial actions, ensuring full user control.

## Tech Stack

The FinGenius AI platform is built with a modern, scalable, and AI-centric tech stack:

*   **Backend & AI Engine:**
    *   **Language:** Python 3.9+
    *   **Web Framework:** FastAPI
    *   **Database:** PostgreSQL
    *   **ORM:** SQLAlchemy 2.0
    *   **Asynchronous Task Queue:** Celery with Redis (Broker)
    *   **Caching:** Redis
    *   **AI/ML Libraries:** Pandas, NumPy, Scikit-learn (TensorFlow/PyTorch for future deep learning)
    *   **External APIs:** Plaid

*   **Frontend:**
    *   **Framework:** React
    *   **State Management:** React Query
    *   **Styling:** Tailwind CSS
    *   **Charting:** Recharts / Chart.js

*   **DevOps & Infrastructure (for production):**
    *   **Cloud Provider:** AWS
    *   **Containerization:** Docker
    *   **CI/CD:** GitHub Actions
    *   **Infrastructure as Code:** Terraform

## Setup Instructions

Follow these steps to set up and run FinGenius AI locally for development.

### Prerequisites

Ensure you have the following installed on your system:

*   **Docker & Docker Compose:** For running the application services.
*   **Node.js (LTS version) & npm/yarn:** For the frontend development.
*   **Python 3.9+:** (Optional, if you prefer to run backend services outside Docker for deeper debugging). We recommend using a tool like [Poetry](https://python-poetry.org/) or [Rye](https://rye-up.com/) for Python dependency management.

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/fingenius-ai.git
cd fingenius-ai
```

### 2. Configure Environment Variables

Create `.env` files based on the provided examples in both `backend/` and `frontend/` directories.

**`backend/.env` (example content):**

```
DATABASE_URL="postgresql://user:password@db:5432/fingenius_db"
REDIS_URL="redis://redis:6379/0"
SECRET_KEY="YOUR_SUPER_SECRET_KEY_FOR_JWT_AND_SESSIONS"
PLAID_CLIENT_ID="your_plaid_client_id"
PLAID_SECRET="your_plaid_secret"
PLAID_ENV="sandbox" # or development, production
# Add other Plaid settings as needed (e.g., PLAID_PRODUCTS, PLAID_COUNTRY_CODES)
```

**`frontend/.env` (example content):**

```
REACT_APP_API_BASE_URL="http://localhost:8000/api/v1"
REACT_APP_PLAID_PUBLIC_KEY="your_plaid_public_key"
REACT_APP_PLAID_ENV="sandbox"
```

*   **Important:** Replace placeholder values with your actual secrets and API keys. For local development, `YOUR_SUPER_SECRET_KEY_FOR_JWT_AND_SESSIONS` can be a random string. For Plaid, you'll need to create a developer account to get your keys.

### 3. Run with Docker Compose (Recommended for Local Dev)

This will set up the PostgreSQL database, Redis, Celery worker, and both the FastAPI backend and React frontend services.

```bash
docker-compose up --build -d
```

*   `--build`: Rebuilds images (useful if you made changes to Dockerfiles).
*   `-d`: Runs containers in detached mode (in the background).

Wait a few moments for all services to start. You can check the status with `docker-compose ps`.

### 4. Apply Database Migrations

Once the backend service is up (you can check its logs with `docker-compose logs backend`), apply the database migrations:

```bash
docker-compose exec backend sh /app/scripts/apply_migrations.sh
```

This script typically runs `alembic upgrade head` inside the backend container.

### 5. Access the Application

*   **Frontend:** Open your web browser and navigate to `http://localhost:3000`
*   **Backend API Docs:** The FastAPI interactive API documentation will be available at `http://localhost:8000/docs`

### Running Backend/Frontend Separately (Advanced)

If you need to run specific services outside Docker for detailed debugging:

**Backend:**

```bash
cd backend
# Using Poetry for dependency management (install if you don't have it)
# poetry install
# poetry run alembic upgrade head
# poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend:**

```bash
cd frontend
npm install # or yarn install
npm start   # or yarn start
```

### Running Tests

**Backend Tests:**

```bash
docker-compose exec backend poetry run pytest
# Or if running locally:
# cd backend
# poetry run pytest
```

**Frontend Tests:**

```bash
cd frontend
npm test # or yarn test
```

## Contributing

We welcome contributions! Please see our `CONTRIBUTING.md` file for details on how to get started, our code of conduct, and submission process.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
