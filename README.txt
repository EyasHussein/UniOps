# UniOps: Smart Campus Operations System

UniOps is a comprehensive, role-based campus management web application designed to streamline university operations. Built with Django, it provides a centralized platform for handling room inventory, scheduling academic spaces, tracking facility maintenance, and managing student complaints.

By leveraging **HTMX** and **Tailwind CSS**, the system delivers a fast, single-page-application (SPA) feel while maintaining the robust security and architecture of a server-rendered Django backend[cite: 4].

---

## Tech Stack
* **Backend:** Python, Django 5.2.8[cite: 4]
* **Frontend:** HTMX (for dynamic, no-reload interactions), Tailwind CSS[cite: 4]
* **Database:** SQLite (Development) / MySQL Ready (`mysqlclient` configured)[cite: 4]
* **Asset Management:** Pillow (for image uploads)[cite: 4]

---

## Key Features

The system is divided into three primary access levels, ensuring users only see the tools relevant to their role[cite: 4]:

### Administrator Portal
* **Global Dashboard:** High-level metrics tracking pending bookings, open maintenance requests, and unresolved complaints[cite: 4].
* **Room Management:** Full CRUD (Create, Read, Update, Delete) control over campus buildings and room inventory[cite: 4].
* **Ticketing Control:** Ability to change statuses, review attached photo evidence, and manage the lifecycle of maintenance and complaint tickets[cite: 4].

### Faculty Portal
* **Smart Room Booking:** Reserve available lecture halls, labs, or meeting rooms. The system automatically hides non-bookable spaces (like cafeterias and libraries)[cite: 4].
* **Facility Maintenance:** Submit maintenance tickets (e.g., Electrical, Plumbing, HVAC) directly to the admin team with priority levels and photo attachments[cite: 4].

### Student Portal
* **Issue Reporting:** Submit complaints regarding campus facilities or cleanliness[cite: 4].
* **Status Tracking:** View the real-time status (Pending, In Progress, Resolved) of submitted issues[cite: 4].

### Core System Architecture
* **Soft Deletes & Data Recovery:** Records (bookings, maintenance, complaints) are never hard-deleted. They are archived (`is_deleted=True`), providing an "Undo" feature for safe data recovery[cite: 4].
* **HTMX Modals:** Asynchronous loading of detail views without full page reloads, keeping the user interface clean and responsive[cite: 4].

---

## Recent Updates & Fixes

This project is actively maintained. Recent architectural improvements include:

* **Calendar & Overlap Engine Fix:** Completely refactored the room booking logic. Overlap validation for reservations is now securely evaluated at the database level using Django ORM time filters, preventing double-booking and removing heavy load from Python memory.
* **Security & Access Control Refactor:** Replaced repetitive in-view permission checks with clean, reusable `@role_required` decorators to enforce strict middleware-level security for Admin, Faculty, and Student routes.
* **System Stability Patch:** Fixed a critical `UnboundLocalError` edge case that caused server crashes when attempting to delete a room that lacked a building assignment.

---

## Roadmap (Coming Soon)

* **Real-Time Notifications:** Activation of the `notifications` app to provide users with immediate alerts when a booking is approved, or a complaint is resolved[cite: 4].
* **Dashboard Pagination:** Integration of Django's `Paginator` on the Admin dashboard to lazy-load ticket histories, ensuring zero memory bottlenecks at enterprise scale.
* **Production Asset Pipeline:** Transitioning from the Tailwind CDN to compiled CSS using the integrated `django-tailwind` package for optimized production loading times[cite: 4].

---

## Local Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/uniops.git](https://github.com/yourusername/uniops.git)
   cd uniops
    ```

2. **Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
Install dependencies:
pip install -r requirements.txt

Run migrations to set up the database:
python manage.py migrate

Create a superuser (Admin account):
python manage.py createsuperuser

Start the development server:
python manage.py runserver