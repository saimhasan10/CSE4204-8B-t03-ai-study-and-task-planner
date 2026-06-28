# AI Study and Task Planner

## Team Information

| Information        | Details                   |
| ------------------ | ------------------------- |
| Course Code        | CSE4204                   |
| Course Name        | Mobile Computing Lab      |
| Section            | 8B                        |
| Team Number        | T03                       |
| Official Team Name | CSE4204-8B-T03            |
| Project Title      | AI Study and Task Planner |

## Team Members

| Role                | Name                  | Student ID  |
| ------------------- | --------------------- | ----------- |
| Team Leader         | SAIM HASAN NAHID      | 11220320897 |
| Backend Developer   | AISHA SIDDIKA OISHEE  | 11220320893 |
| Frontend Developer  | EITY                  | 11220320896 |
| AI Integration Lead | MD KHALED HASAN RIHAD | 11220320891 |

## Project Description

AI Study and Task Planner is a web-based system designed to help university students manage their study tasks, project deadlines, and academic workload in an organized way.

Students can add tasks, set deadlines, choose priority levels, and track their progress. The AI assistant helps students generate study plans, suggest task priorities, and break large tasks into smaller manageable steps.

The main goal of this project is to reduce last-minute academic pressure and improve student productivity through task management and AI-based planning support.

## Objectives

* To help university students manage study tasks and deadlines in one place.
* To provide task priority and status tracking.
* To generate AI-based study plans from user tasks.
* To help students break large tasks into smaller steps.
* To reduce last-minute pressure through better academic planning.

## Proposed Features

* User registration and login
* Student dashboard
* Course management
* Task creation and management
* Deadline tracking
* Task priority selection
* Task status tracking
* Progress overview
* AI-generated study plan
* AI-based task priority suggestion
* AI support for breaking large tasks into smaller steps
* AI chat support
* Saved AI plans

## Technology Stack

| Part                | Technology            |
| ------------------- | --------------------- |
| Frontend            | React.js              |
| Styling             | Tailwind CSS          |
| Backend             | Django                |
| API                 | Django REST Framework |
| Authentication      | JWT Authentication    |
| Database            | PostgreSQL            |
| AI Integration      | Google Gemini API     |
| API Testing         | Postman               |
| Version Control     | Git and GitHub        |
| Backend Deployment  | Render                |
| Frontend Deployment | Netlify               |
| UI/UX Design        | Figma Make            |

## Project Links

| Resource          | Link                                                                                                              |
| ----------------- | ----------------------------------------------------------------------------------------------------------------- |
| GitHub Repository | https://github.com/saimhasan10/CSE4204-8B-t03-ai-study-and-task-planner                                           |
| Live Backend      | https://ai-study-task-planner-backend.onrender.com                                                                |
| Health Check API  | https://ai-study-task-planner-backend.onrender.com/api/health/                                                    |
| Figma Design      | https://www.figma.com/make/ky0SyxVVlv5ngIhio9W96k/Design-System-for-AI-Planner?t=dYQb8xQ5SmmYDz6d-20&fullscreen=1 |

## Updated Repository Structure

```text
CSE4204-8B-t03-ai-study-and-task-planner/
│
├── backend/
│   ├── accounts/
│   ├── ai_assistant/
│   ├── config/
│   ├── courses/
│   ├── progress/
│   ├── tasks/
│   ├── manage.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
├── database/
├── documentation/
├── diagrams/
├── design/
│   └── CSE4204-8B-T03_UIDesign.pdf
├── README.md
└── .gitignore
```

## Week 05 — UI/UX Design and Development Planning

The Week 05 assignment focused on preparing the visual blueprint, user experience, development roadmap, team responsibilities, and final technology setup for the AI Study and Task Planner.

### UI/UX Design

The interface was designed using Figma with a simple, professional, consistent, and responsive design system.

The UI design includes:

* Landing Page
* Login Page
* Registration Page
* Dashboard
* Course Management
* Task Management
* Task Details
* Progress Overview
* User Profile
* AI Study Planner
* AI Priority Suggestion
* AI Task Breakdown
* AI Chat
* Saved AI Plans
* Responsive mobile design

### User Flow

```text
Landing Page
      ↓
Registration or Login
      ↓
Dashboard
      ↓
Courses and Tasks
      ↓
AI Study Planner
      ↓
Generated AI Result
      ↓
Progress Overview
      ↓
User Profile
      ↓
Logout
```

## Week 06 — Backend Development Progress

The Week 06 work focused on backend development, database implementation, authentication, API development, API testing, GitHub workflow, and backend deployment.

### Completed Backend Work

* Django backend project setup completed.
* Django REST Framework configured.
* JWT authentication system implemented.
* User registration, login, logout, and profile APIs developed.
* Course management APIs developed.
* Task management APIs developed.
* Progress overview API developed.
* AI assistant API structure implemented.
* PostgreSQL database connected for production.
* Backend deployed successfully on Render.
* APIs tested using Postman.
* Database verified using pgAdmin.
* Backend code pushed and updated on GitHub main branch.

## Backend Setup

### Local Backend Setup

```bash
cd backend
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Backend Environment Variables

The backend uses environment variables for secure configuration.

```env
SECRET_KEY=your_secret_key
DEBUG=False
ALLOWED_HOSTS=.onrender.com
USE_POSTGRES=True
DATABASE_URL=your_database_url
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash
```

> Sensitive values such as API keys, database URL, password, and secret keys are not included in the repository.

## API Endpoints

### Base URL

```text
https://ai-study-task-planner-backend.onrender.com
```

## API List

| SL | Method           | Endpoint                  | Authentication | Purpose                                      | Status               |
| -- | ---------------- | ------------------------- | -------------- | -------------------------------------------- | -------------------- |
| 1  | GET              | `/api/health/`            | Not Required   | Check if backend server is running           | Working              |
| 2  | POST             | `/api/accounts/register/` | Not Required   | Register a new user                          | Working              |
| 3  | POST             | `/api/accounts/login/`    | Not Required   | Login user and return JWT tokens             | Working              |
| 4  | GET              | `/api/accounts/profile/`  | Required       | Get logged-in user profile                   | Working              |
| 5  | PUT/PATCH        | `/api/accounts/profile/`  | Required       | Update user profile                          | Working              |
| 6  | POST             | `/api/accounts/logout/`   | Required       | Logout user / blacklist refresh token        | Working              |
| 7  | GET              | `/api/courses/`           | Required       | Get all courses of logged-in user            | Working              |
| 8  | POST             | `/api/courses/`           | Required       | Create a new course                          | Working              |
| 9  | GET              | `/api/courses/<id>/`      | Required       | Get details of a single course               | Working              |
| 10 | PUT/PATCH        | `/api/courses/<id>/`      | Required       | Update course information                    | Working              |
| 11 | DELETE           | `/api/courses/<id>/`      | Required       | Delete a course                              | Working              |
| 12 | GET              | `/api/tasks/`             | Required       | Get all tasks of logged-in user              | Working              |
| 13 | POST             | `/api/tasks/`             | Required       | Create a new task                            | Working              |
| 14 | GET              | `/api/tasks/<id>/`        | Required       | Get details of a single task                 | Working              |
| 15 | PUT/PATCH        | `/api/tasks/<id>/`        | Required       | Update task information                      | Working              |
| 16 | DELETE           | `/api/tasks/<id>/`        | Required       | Delete a task                                | Working              |
| 17 | GET              | `/api/tasks/filter/`      | Required       | Filter tasks by status, priority, or course  | Working              |
| 18 | GET              | `/api/progress/`          | Required       | Show task progress summary and statistics    | Working              |
| 19 | GET              | `/api/ai/`                | Not Required   | Show available AI API endpoints              | Working              |
| 20 | POST             | `/api/ai/study-plan/`     | Required       | Generate AI-based study plan                 | Implemented          |
| 21 | POST             | `/api/ai/priority/`       | Required       | Suggest task priority using AI               | Implemented          |
| 22 | POST             | `/api/ai/task-breakdown/` | Required       | Break large task into smaller steps using AI | Implemented          |
| 23 | POST             | `/api/ai/chat/`           | Required       | AI chat support                              | Optimization Pending |
| 24 | GET/POST         | `/api/ai/plans/`          | Required       | View or save AI-generated plans              | Implemented          |
| 25 | GET/PATCH/DELETE | `/api/ai/plans/<id>/`     | Required       | View, update, or delete saved AI plan        | Implemented          |

## API Testing

APIs were tested using Postman. The following API modules were verified:

* Health API
* User Registration API
* User Login API
* User Profile API
* Course API
* Task API
* Progress API
* AI Home API

JWT Bearer Token authentication was used for protected APIs.

## Database Implementation

PostgreSQL is used for production database hosting. The database contains tables for users, courses, tasks, progress-related data, AI saved plans, and JWT token blacklist management.

### Main Database Tables

| Table                              | Purpose                           |
| ---------------------------------- | --------------------------------- |
| `auth_user`                        | Stores user account information   |
| `courses_course`                   | Stores course information         |
| `tasks_task`                       | Stores task information           |
| `ai_assistant_savedaiplan`         | Stores saved AI-generated plans   |
| `token_blacklist_outstandingtoken` | Stores JWT outstanding tokens     |
| `token_blacklist_blacklistedtoken` | Stores blacklisted refresh tokens |
| `django_migrations`                | Stores migration history          |
| `django_session`                   | Stores session data               |

## Main Models

### Course Model

The course model stores academic course information.

| Field        | Description          |
| ------------ | -------------------- |
| user         | Owner of the course  |
| title        | Course title         |
| code         | Course code          |
| instructor   | Course instructor    |
| credit_hours | Credit value         |
| semester     | Semester information |
| description  | Course description   |
| created_at   | Creation time        |
| updated_at   | Last update time     |

### Task Model

The task model stores student study tasks and deadlines.

| Field           | Description           |
| --------------- | --------------------- |
| user            | Owner of the task     |
| course          | Related course        |
| title           | Task title            |
| description     | Task details          |
| deadline        | Task deadline         |
| priority        | Task priority         |
| status          | Task status           |
| estimated_hours | Estimated time needed |
| completed_at    | Completion time       |
| created_at      | Creation time         |
| updated_at      | Last update time      |

## Task Priority Options

```text
low
medium
high
urgent
```

## Task Status Options

```text
pending
in_progress
completed
```

## Deployment Information

The backend has been deployed on Render.

### Render Configuration

| Item                | Value                                                         |
| ------------------- | ------------------------------------------------------------- |
| Root Directory      | `backend`                                                     |
| Build Command       | `pip install -r requirements.txt && python manage.py migrate` |
| Start Command       | `gunicorn config.wsgi:application`                            |
| Database            | PostgreSQL                                                    |
| Deployment Platform | Render                                                        |

### Live Backend

```text
https://ai-study-task-planner-backend.onrender.com
```

### Health Check

```text
https://ai-study-task-planner-backend.onrender.com/api/health/
```

## GitHub Workflow

The backend development workflow was completed through GitHub.

```text
Feature Branch Development
        ↓
Backend Code Push
        ↓
Main Branch Merge
        ↓
Render Deployment
        ↓
API Testing
```

### Branch Information

| Branch                        | Purpose                      |
| ----------------------------- | ---------------------------- |
| `main`                        | Final updated project branch |
| `feature/backend-development` | Backend development branch   |

## Current Project Status

| Module               | Status               |
| -------------------- | -------------------- |
| Backend Setup        | Completed            |
| JWT Authentication   | Completed            |
| Course API           | Completed            |
| Task API             | Completed            |
| Progress API         | Completed            |
| PostgreSQL Database  | Connected            |
| Render Deployment    | Completed            |
| Postman API Testing  | Completed            |
| GitHub Update        | Completed            |
| AI API Structure     | Implemented          |
| Hosted AI Chat       | Optimization Pending |
| Frontend Integration | Next Phase           |

## Current Limitations

* Hosted AI chat response needs further optimization on Render.
* Full frontend-backend integration will be completed in the next development phase.
* Some advanced analytics features will be improved later.
* Final production security hardening will be done before final deployment.

## Development Roadmap

| Week    | Development Phase            | Main Activities                                                                                                   |
| ------- | ---------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Week 06 | Backend Development          | Django setup, authentication, course APIs, task APIs, progress API, PostgreSQL integration, and Render deployment |
| Week 07 | Frontend Development         | React interface, responsive pages, routing, and backend API connection                                            |
| Week 08 | AI Integration               | Gemini API, study-plan generation, priority suggestion, task breakdown, and AI chat improvement                   |
| Week 09 | Feature Completion           | Complete remaining features and improve frontend-backend integration                                              |
| Week 10 | Testing and Debugging        | Functional testing, responsive testing, API testing, and bug fixing                                               |
| Week 11 | Deployment and Documentation | Final deployment, documentation, and final preparation                                                            |

## Team Task Distribution

| Team Member           | Role                | Main Responsibilities                                                                                |
| --------------------- | ------------------- | ---------------------------------------------------------------------------------------------------- |
| Saim Hasan Nahid      | Team Lead           | Project planning, foundation development, module integration, testing, documentation, and deployment |
| Aisha Siddika Oishee  | Backend Developer   | Django backend verification, API testing, database checking, and backend contribution                |
| Eity                  | Frontend Developer  | Figma design review, React frontend verification, responsive testing, and frontend contribution      |
| Md Khaled Hasan Rihad | AI Integration Lead | Gemini prompt testing, AI response verification, and AI integration contribution                     |

## Expected Outcome

The system will help students plan their study tasks more effectively. It will make task management easier, improve time planning, and provide AI-based guidance for better academic productivity.

After completing the backend phase, the project now has a functional server, database, authentication system, and core APIs ready for frontend integration.

## Week 06 Submission Files

| File                                 | Description               |
| ------------------------------------ | ------------------------- |
| `CSE4204-8B-T03_BackendProgress.pdf` | Backend progress report   |
| `CSE4204-8B-T03_APICollection.json`  | Postman API collection    |
| GitHub Repository Link               | Updated source code       |
| Render Live API Link                 | Live backend testing link |


