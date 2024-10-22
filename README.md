# 📝 Task Management System with Subscription Tiers

Welcome to the Task Management System! This web application is built using Django and offers a comprehensive solution for managing tasks with various subscription models (Bronze, Silver, and Gold). 

With this system, users can create, organize, and complete tasks, view statistics, manage their profiles, and even purchase in-app currency called **Rubies** to unlock extra features.

## 🚀 Features

### ✅ Task Management
- **Create, delete, and complete tasks**: Stay on top of your to-do list by managing tasks easily.
- **Categorize tasks**: Organize your tasks into custom categories like work, leisure, etc.
- **Prioritize tasks**: Focus on what's important by setting task priorities (available in Silver and Gold tiers).

### 💎 Subscription Tiers
- **Bronze**: Basic access, allowing you to create, complete, and organize tasks with limited functionality.
- **Silver**: Unlock advanced task management features like priorities, additional categories, and task filtering.
- **Gold**: Gain full access to the system, including detailed task statistics, customizable profiles, and more.

### 📊 User Profiles and Statistics
- **Track your progress**: Get insights into your task completion rates and overall productivity.
- **Customize your profile**: Gold-tier users can personalize their experience.
- **View statistics**: Gold-tier users get access to in-depth task statistics.

### 💰 In-app Currency: Rubies
- **Purchase Rubies**: Users can buy Rubies to unlock premium features or boost their profile.
- **Spend Rubies**: Rubies can be used for additional customizations and task management perks.

## 🛠️ Technologies Used

- **Django**: The main framework used for the backend development of the project.
- **HTML, CSS, JavaScript**: Standard technologies used for the frontend design and interactivity.
- **Django Time**: Provides time-based task and user statistics management.
- **Bootstrap**: Used for responsive and modern UI components throughout the site.

## 📦 Installation

Follow these steps to set up the project on your local machine:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-usern
ame/your-repo-name.git
2. **Install the required dependencies: Make sure you have pip installed, and run:**:

    ```bash
    pip install -r requirements.txt
A   pply migrations to set up the database:
 
```bash
 python manage.py migrate
 Create a superuser to access the admin panel:


 python manage.py createsuperuser
 Run the development server:


 python manage.py runserver 
 ```

# 🔧 Libraries and Dependencies
Django: Web framework for rapid development.
Django Time: Time and statistics management for tasks.
Bootstrap: Modern CSS framework for creating responsive and attractive UI.
🎯 Future Features
Recurring tasks: Set tasks that repeat daily, weekly, or monthly.
Notifications: Get reminders for upcoming or overdue tasks.
Task Sharing: Share tasks with other users for collaboration.
Additional Analytics: Provide more detailed insights on productivity and task completion patterns.
