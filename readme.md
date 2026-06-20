# AI Study and Task Planner

## Team Information

| Information | Details |
|---|---|
| Course Code | CSE4204 |
| Section | 8B |
| Team Number | T03 |
| Official Team Name | CSE4204-8B-T03 |
| Project Title | AI Study and Task Planner |

## Team Members

| Role | Name | Student ID |
|---|---|---|
| Team Leader | SAIM HASAN NAHID | 11220320897 |
| Backend Developer | AISHA SIDDIKA OISHEE | 11220320893 |
| Frontend Developer | EITY | 11220320896 |
| AI Integration Lead | MD KHALED HASAN RIHAD | 11220320891 |

## Project Description

AI Study and Task Planner is a web-based system designed to help university students manage their study tasks, project deadlines, and academic workload in an organized way.

Students can add tasks, set deadlines, choose priority levels, and track their progress. The AI assistant will help students generate study plans, suggest task priority, and break large tasks into smaller steps.

The main goal of this project is to reduce last-minute pressure and improve student productivity through simple task management and AI-based planning support.

## Proposed Features

- User registration and login
- Student dashboard
- Task creation and management
- Deadline tracking
- Task priority selection
- Task status tracking
- AI-generated study plan
- AI-based task priority suggestion
- AI support for breaking large tasks into smaller steps
- Progress overview

## Technology Stack

| Part | Technology |
|---|---|
| Frontend | React.js |
| Styling | Tailwind CSS |
| Backend | Django |
| API | Django REST Framework |
| Database | PostgreSQL |
| AI Integration | Gemini API |
| Version Control | GitHub |
| Frontend Deployment | Vercel |
| Backend Deployment | Render / Railway |
| Database Hosting | Supabase / Neon |

## Expected Outcome

The system will help students plan their study tasks more effectively. It will make task management easier, improve time planning, and provide AI-based guidance for better academic productivity.

## Objectives

- To help university students manage study tasks and deadlines in one place.
- To provide task priority and status tracking.
- To generate AI-based study plans from user tasks.
- To help students break large tasks into smaller steps.
- To reduce last-minute pressure through better academic planning.

````markdown
## Week 05 — UI/UX Design and Development Planning

The Week 05 assignment focused on preparing the visual blueprint, user experience, development roadmap, team responsibilities, and final technology setup for the **AI Study and Task Planner**.

### UI/UX Design

The interface was designed using **Figma** with a simple, professional, consistent, and responsive design system.

The UI design includes:

- Landing Page
- Login Page
- Registration Page
- Dashboard
- Course Management
- Task Management
- Task Details
- Progress Overview
- User Profile
- AI Study Planner
- AI Priority Suggestion
- AI Task Breakdown
- AI Chat
- Saved AI Plans
- Responsive mobile design

### Design Resources

- [View Figma Design](https://www.figma.com/make/ky0SyxVVlv5ngIhio9W96k/Design-System-for-AI-Planner?t=dYQb8xQ5SmmYDz6d-20&fullscreen=1)
- [View UI/UX Design Document](design/CSE4204-8B-T03_UIDesign.pdf)

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

### Development Roadmap

| Week | Development Phase | Main Activities |
|---|---|---|
| Week 06 | Backend Development | Django setup, authentication, course APIs, task APIs, progress API, and PostgreSQL integration |
| Week 07 | Frontend Development | React interface, responsive pages, routing, and backend API connection |
| Week 08 | AI Integration | Gemini API, study-plan generation, priority suggestion, task breakdown, and AI chat |
| Week 09 | Feature Completion | Complete remaining features and improve frontend-backend integration |
| Week 10 | Testing and Debugging | Functional testing, responsive testing, API testing, and bug fixing |
| Week 11 | Deployment and Documentation | Render deployment, Netlify deployment, documentation, and final preparation |

### Team Task Distribution

| Team Member | Role | Main Responsibilities |
|---|---|---|
| Saim Hasan Nahid | Team Lead | Project planning, foundation development, module integration, testing, documentation, and deployment |
| Aisha Siddika Oishee | Backend Developer | Django backend verification, API testing, database checking, and backend contribution |
| Eity | Frontend Developer | Figma design review, React frontend verification, responsive testing, and frontend contribution |
| Md Khaled Hasan Rihad | AI Integration Lead | Gemini prompt testing, AI response verification, and AI integration contribution |

### Final Technology Stack

| Area | Technology |
|---|---|
| Frontend | React.js, and Tailwind CSS |
| Backend | Django and Django REST Framework |
| Authentication | JWT Authentication |
| Database | PostgreSQL |
| AI Service | Google Gemini API |
| API Testing | Postman |
| Version Control | Git and GitHub |
| Backend Deployment | Render |
| Frontend Deployment | Netlify |
| UI/UX Design | Figma Make |

### Project Setup Plan

#### Backend

```bash
cd backend
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

Environment variables and deployment configuration will be documented during the development and deployment phases.

### Updated Repository Structure

```text
CSE4204-8B-t03-ai-study-and-task-planner/
│
├── backend/
├── frontend/
├── database/
├── documentation/
│   ├── proposal/
│   ├── srs/
│   └── system-design/
├── diagrams/
│   ├── use-case/
│   ├── er-diagram/
│   ├── architecture/
│   └── activity-diagram/
├── design/
│   └── CSE4204-8B-T03_UIDesign.pdf
├── README.md
└── .gitignore
```

