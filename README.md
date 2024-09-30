# StudyBuddy 🎓

**StudyBuddy** is a dynamic chatroom application built using Python Django and SQLite (for local development) and PostgreSQL (for production). It provides a platform for users to create and join chatrooms, engage in discussions, and connect with others on various topics. The project is designed with a user-friendly interface, offering seamless CRUD (Create, Read, Update, Delete) functionality and RESTful API integration.

## Features 🌟

- **Create, Update, Delete Chatrooms**: Users can easily create their own chatrooms, update existing ones, or delete them when no longer needed.
- **Profile Management**: Each user can manage their own profile, including updating personal information and customizing their chatroom experience.
- **Join and Engage**: Users can join available chatrooms and participate in discussions on a wide range of topics.
- **RESTful API**: The application is powered by RESTful APIs, ensuring smooth and efficient communication between the frontend and backend.
- **Aesthetic User Interface**: The UI is designed to be both functional and visually appealing, enhancing the overall user experience.

## Technologies Used 🛠️

- **Backend**: Python Django
- **Database**: SQLite (Local Development), PostgreSQL (Production)
- **Frontend**: HTML, CSS, JavaScript
- **Media Storage**: Cloudinary for storing and delivering user profile images and other media files
- **APIs**: RESTful API for data handling
- **CI/CD**: Continuous Integration and Continuous Deployment tested with staging, feature addition, and merging

## Deployment 🌐

The StudyBuddy chatroom application is deployed on Render.com, which simplifies the server setup, scaling, and deployment process.

- **Live Server**: [StudyBuddy Live](https://studybuddy-7hed.onrender.com/)
- **Media Storage**: Cloudinary is used to efficiently manage and serve media content like user profile images.

## How to Set Up and Run Locally ⚙️

### Prerequisites

- Python (3.x)
- Django
- PostgreSQL
- Cloudinary account (for media storage)
- Render account (for deployment, if required)

### Setup Steps

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/studybuddy.git
   cd studybuddy
   ```

2. **Set up a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure PostgreSQL (for production)**:

   - Set up a PostgreSQL database.
   - Update your `settings.py` file with the PostgreSQL configuration:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_db_name',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. **Run migrations**:

   ```bash
   python manage.py migrate
   ```

6. **Configure Cloudinary for media storage**:

   - Add Cloudinary credentials in your `settings.py` file:

   ```python
   CLOUDINARY_STORAGE = {
       'CLOUD_NAME': 'your_cloud_name',
       'API_KEY': 'your_api_key',
       'API_SECRET': 'your_api_secret',
   }
   DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
   ```

7. **Create a superuser**:

   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

Now, you should be able to access the application at `http://127.0.0.1:8000/`.

## CI/CD Implementation 🔄

StudyBuddy incorporates a basic CI/CD pipeline, where features are staged, tested, and merged into production. This ensures that updates and new features can be reliably added with minimal disruption to the live environment.
