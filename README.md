# Portfolio Backend

This is the backend for my portfolio built with Django and Django REST Framework.

## Features
- **API**: Provides RESTful endpoints for the portfolio frontend.
- **Media Storage**: Integrated with Cloudinary for image and file uploads.
- **Background Tasks**: Uses Celery and Redis for asynchronous task processing (e.g., sending emails).
- **Deployment Ready**: Configured for GitHub and AWS (PostgreSQL, Gunicorn, WhiteNoise).

## Tech Stack
- Django 6.0.1
- Django REST Framework
- PostgreSQL (Production) / SQLite (Local)
- Cloudinary (Media Storage)
- Celery & Redis (Task Queue)
- WhiteNoise (Static Files)
- Gunicorn (WSGI Server)

## Local Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd backend-for-portfolio/core
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the `core` directory and add the following:
   ```env
   SECRET_KEY=your_secret_key
   DEBUG=True
   ALLOWED_HOSTS=*
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   EMAIL_HOST_USER=your_email
   EMAIL_HOST_PASSWORD=your_email_password
   CELERY_BROKER_URL=redis://127.0.0.1:6379/1
   ```

5. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

7. **Start Celery Worker (In another terminal)**:
   ```bash
   celery -A core worker --loglevel=info
   ```

## Deployment on AWS

1. **Database**: Use Amazon RDS (PostgreSQL).
2. **Hosting**: Can be deployed on AWS Elastic Beanstalk, EC2, or AWS App Runner.
3. **Environment Variables**: Set the environment variables in the AWS console (Configuration -> Software) or via a `.env` file on the server.
4. **Static Files**: Run `python manage.py collectstatic` during the build process. WhiteNoise will serve them.

## GitHub
Make sure to initialized a git repository and commit your changes:
```bash
git init
git add .
git commit -m "Initial commit - project ready for deployment"
```
DONT forget to keep your `.env` file secret and never commit it to GitHub! (It's already added to `.gitignore`).
