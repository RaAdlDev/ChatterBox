# ChatterBox 📩

ChattBox is a robust RESTful API designed for real-time communication using WebSockets. It provides a secure environment for user messaging, featuring role-based access control, persistent chat history, and seamless data management.

---


## Key Features

* **Real-Time Messaging:** Bidirectional communication via WebSockets for an instantaneous chat experience.
* **Data Persistence:** Full storage of chat rooms and message history using PostgreSQL.
* **Secure Authentication:** Implementation of JSON Web Tokens (JWT) for secure route and connection handling.
* **Role-Based Access Control (RBAC):** Integrated permission system with `admin` and `user` roles.
* **Comprehensive CRUD:** Full management capabilities for users, messages, and chat rooms.
* **Clean Architecture:** Highly maintainable and scalable code organized into layers (routes, services, models, and schemas).


---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Auth | JSON Web Tokens (JWT) |
| Server | Uvicorn |
| Hashing | bcrypt |
| Database | PostgreSQL |

---

 **Live Demo:** (https://chatterboxapiwebsovcketsraadldev.onrender.com)
 
 **Register Example**
 <img width="711" height="394" alt="example chattbox" src="https://github.com/user-attachments/assets/4e0c7036-41c7-45e3-bbc8-72382950c7d2" />

## Getting Started

### Prerequisites


- Python 3.10 or higher
- `pip` package manager


### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/RaAdlDev/ChatterBox.git

   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate        # Linux / macOS
   venv\Scripts\activate           # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the root directory:

   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/chattbox_db
   SECRET_KEY=your_supersecret_key
   TOKEN_DURATION=your_token_duration
   ALGORITHM=HS256
   
   ```

5. **Run the development server**

   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at `http://127.0.0.1:8000`.

---

## API Overview

- You have access to each message an conversation
- Endpoints for Delete and Promote are exclusive to admins

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/register` | Register a new user |
| `POST` | `/login` | Login and receive a JWT token |
| `GET` | `/users` | A list with all the users |
| `GET` | `/users/me` | Your user information |
| `DELETE` | `/users/delete/{user_id}` | Delete one user |
| `PATCH` | `/users/promote/{user_id}` | Promote one user to admin |


### Conversations

| Method | Endpoint | Description |
|--------|----------|-------------|
| `WebSocket` | `/ws/{user_id}` | Start a conversation |
| `GET` | `/conversation/{user_id}` | Get messages in a conversation |
| `GET` | `/conversations` | Get all your conversations |



---

## Interactive API Docs

FastAPI generates interactive documentation automatically. Once the server is running, visit:

- **Swagger UI** → `http://127.0.0.1:8000/docs`
- **ReDoc** → `http://127.0.0.1:8000/redoc`

---

## Project Structure

```
ChattBox/
├── main.py               # App entry point
├── database/             # Database connection and session, SQLAlchemy models
│   ├── models.py
│   └── connection.py           
├── schemas/              # Pydantic schemas
│   ├── User.py
├── routers/              # API route handlers
│   ├── auth.py
│   └── chat.py
├── core/                 # JWT logic and dependencies
│   ├── security.py
│   └── settings.py
├── services/             # Business logic and database operations
│   ├── auth_services.py
│   └── chat_services.py
├── requirements.txt
└── .env
└── .gitignore

```

---

## License

This project is licensed under the MIT License.
