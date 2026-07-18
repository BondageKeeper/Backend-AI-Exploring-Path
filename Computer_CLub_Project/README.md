# PC_Bang-Website

## Introduction:
So, I was so curious to create my own website from scratch recently and it turns out to be very interesting. First of all I understood many things about docker 
and what the container simply means. Futhermore I improved my Backend-skills significantly and learned how to work with Frontend using html language. Of course 
I had a bunch of troubles but over time I resolved them and now can avoid some stupid mistakes - this experience is definitely priceless.

## 📷How the it looks:
<img width="1918" height="978" alt="first_site_cover" src="https://github.com/user-attachments/assets/f548971a-9247-4740-802e-e8267ce69f6e" />

## 🛠️ Used tools(crucial libraries):
* **SQLAlchemy** - The most important tool to create tables , to make relationships between tables via ORM and to store users data. 
* **FastAPI** - The API structured user input over HTTP POST, validates the payload, and returns a JSON response with status and details.
* **Pydantic** - This is very incredible tool to validate email,phone_number,unique nickname or other fields.
* **Loguru** - This can represent something like a dashboard of the server , it can store some errors in files and this library automatically updates these files.
* **FastAPI-Swagger UI** - It provides Swagger UI where you can check Backend part - find errors and correct them. 
* **CORSMiddleware** - It is used to create new configuration for the favorable connection between the API and Frontend. 
* **Datetime** - I used it to establish time intervals including timedelta method.
* **Regex(re)** - My favourite tool to parse and to validate data.
* **SQLAlchemy.ext.asyncio** - Almost all functions are asynchronous, therefore asyncio is one of the fundamental tools as well.

## ⚡ Key Features:
* **Real-time PC Availability** - Displays a live list of available gaming rigs, from Lenovo Legion to custom RTX 4090 setups.
* **Smart Time-Slot Booking** - Implements a robust validation system that prevents double-booking; once a PC is reserved for a specific time interval, other users cannot book it.
* **User Data Validation** - Validates user details on the fly, including nicknames, emails, and phone numbers before confirming the reservation.
* **Flexible Booking Options** - Allows users to choose specific computers, select the desired number of gaming hours, and opt for additional services.
* **Live Deployment** - The project is fully configured, production-ready, and deployed on a custom domain.
 
# 🔄 The Sequence of the Process (Workflow):
1. **User Access & Input** - The user visits the live website via the custom domain `http://first-pattern.website` and fills out the registration form (Nickname, Email, Phone number) along with the booking details (Selected PC, desired hours, arrival time, and additional services).
2. **Frontend Validation & Payloads** - Before any network requests are sent, the frontend ensures that all basic fields are filled out. Once verified, it dispatches an asynchronous `fetch` request containing the booking payload to the FastAPI backend.
3. **Backend & Pydantic Validation** - The backend intercepts the request and passes the incoming data through Pydantic models. It strictly validates data formats (such as correct email syntax, phone number lengths, and string patterns via Regex).
4. **Time-Slot & Availability Check** - The core business logic kicks in using SQLAlchemy. The system queries the database to check existing reservations for the requested PC. It verifies that the new arrival time and duration interval do not overlap with any already booked slots.
5. **Database Persistence** - If all validation checks pass and the time-slot is completely free, the new booking instance is safely written and committed to the database using asynchronous operations (`SQLAlchemy.ext.asyncio`).
6. **API Response** - Finally, the server returns a successful JSON response back to the client's `fetch` request, triggering a UI update on the website to confirm the reservation to the user. If any step fails, an appropriate error status and detail message are returned instead.

## 📂 Project Structure:

```text
my_project/
├── PC_Bang/                         # Backend application directory
│   └── app/
│       ├── routers/
│       │   └── booking_storage.py   # API endpoints for handling book requests
│       ├── crud.py                  # Database operations (Create, Read, Update, Delete)
│       ├── main.py                  # FastAPI application entry point & initialization
│       ├── validation.py            # Pydantic models and custom data validation logic
│       └── Users_registration_errors.log # Loguru file for tracking registration issues
├── frontend/
│   └── main_cover.html              # Main frontend UI for the booking service
├── Dockerfile                       # Containerization setup for the backend environment
├── compose.yml                      # Docker Compose configuration for easy multi-container launch
└── requirements.txt                 # List of backend Python dependencies and libraries
```

## 🌐 Deployment & Server Management

The application is fully deployed on a virtual private server (**VPS**) provided by **Beget.com**. Below are the essential steps and commands used to connect to the server and manage the application containers.

### 🔑 Connecting to the VPS
To manage the project, open your terminal (cmd, PowerShell, or Bash) and connect to the remote server via SSH:
```bash
ssh root@your_server_ip
```
*(Replace `your_server_ip` with the actual IP address of your Beget VPS).*

### 🐳 Managing Application Containers (Docker)
Once connected to the server, navigate to the project directory:
```bash
cd my_project
```

Use the following commands to control the application deployment:

* **Stop and remove containers** - To safely bring down the running service without deleting data:
  ```bash
  docker compose down
  ```
* **Start and build containers** - To build the environment from scratch, install dependencies, and run the service in the background (detached mode):
  ```bash
  docker compose up --build -d
  ```
* **Check running services** - To verify that both backend and frontend environments are active and healthy:
  ```bash
  docker compose ps
  ```

## 🎯 Conclusion:
This project was quite complex to build from scratch without a mentor, pushing me to rely heavily on documentation, community forums, and AI assistance. While overcoming deployment and validation hurdles felt intense at times, the final result was worth every struggle. It successfully proved my ability to build, debug, and ship production-ready applications autonomously.
