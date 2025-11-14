# Django-project-1

# Ice Cream Shop E-Commerce Platform

A full-stack e-commerce application built with **Django** for an ice cream/sweet shop. This project features a complete ordering workflow, user-side order management, search functionality, and a dedicated admin interface for CRUD operations.

## ✨ Features

The application is designed to provide a smooth experience for both customers and administrators.

### Frontend (Customer Experience)

1.  **Product Catalog:** Displays products added by the administrator on the **Home Page**.
2.  **Ordering Workflow:**
      * Products can be added to the cart and confirmed on the **My Cart** page.
      * Users track order status on the **My Orders** page.
3.  **Order Management:** Users can **delete a pending order** (if the status has not yet been updated by the admin).
4.  **Search:** Global search implemented for finding both **products** and current **orders**.
5.  **Feedback:** The **Contact** page allows users to submit comments and feedback.

### Backend (Admin Panel)

The admin panel provides full CRUD (Create, Read, Update, Delete) capabilities across the application's core data models:

  * **Product Management:** Full control over the inventory displayed on the Home page.
  * **Order Fulfillment:** Ability to view all customer orders, order items, and update the order status (e.g., to "placed," "shipped," or "delivered").
  * **User Management:** Maintain and manage the list of registered users.
  * **Feedback Review:** Read and manage comments/feedback submitted via the Contact page.

-----

## 🚀 Local Setup & Installation

Follow these steps to get a copy of the project up and running on your local machine.

### Prerequisites

  * Python (3.x recommended)
  * Git

### Installation Steps

1.  **Clone the Repository (or initialize if this is the first commit):**

    ```bash
    git clone [YOUR_REPOSITORY_URL]
    # OR if you are starting a new project in the directory:
    git init
    ```

2.  **Create and Activate Virtual Environment:**

    ```bash
    # Create the environment
    python -m venv env

    # Activate the environment (using PowerShell)
    . .\env\Scripts\Activate.ps1
    # or (using Git Bash/Linux/macOS)
    source env/bin/activate
    ```

3.  **Install Dependencies:**

    ```bash
    # Install all required dependencies
    pip install -r requirements.txt
    ```

4.  **Run Migrations:**

    Apply the necessary database changes (which sets up the `auth`, `admin`, and custom app tables).

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Create Superuser:**

    Create an administrator account to access the Django Admin Panel (`/admin`).

    ```bash
    python manage.py createsuperuser
    ```

    *Use: Username: `admin`, Email: `admin@gmail.com`*

6.  **Run the Server:**

    ```bash
    python manage.py runserver
    ```

The application will now be running at `http://127.0.0.1:8000/`.

-----

## 🛠️ Key Technologies

  * **Backend:** Django (Python)
  * **Database:** SQLite3 (default for development)
  * **Frontend:** HTML5, CSS3, JavaScript (for client-side enhancements)
  * **Styling:** Bootstrap 5

-----

## 👨‍💻 Developer Information

**Project Name:** Ice Cream Shop
**Main App:** Ice Cream Shop
**Developer:** Md Rezaul Karim

-----

### Sample ORM Commands (for debugging/testing)

The following commands were used to test data creation and retrieval in the Django shell:

```python
# Launch the Django Shell
# python manage.py shell

# Data Retrieval Examples:
from home.models import Contact

# Retrieve all Contact objects
Contact.objects.all()

# Filter by name and phone (demonstrates filtering and saving)
ins = Contact.objects.filter(name="name", phone="9999999999")[0]
ins.phone = "0000000000"
ins.save()
```
