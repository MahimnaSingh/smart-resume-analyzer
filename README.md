# smart-resume-analyzer
Smart Resume Analyzer is a Streamlit-based app that analyzes resumes, predicts candidate level, and recommends skills, courses, and improvement tips. It also provides resume scores, career guidance videos, and an admin dashboard with interactive charts for user insights.

# Smart Resume Analyzer - Deployment Guide

## Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

## Local Deployment Steps

1. Clone the repository:
```bash
git clone <your-repository-url>
cd smart-resume-analyzer
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

The application should now be running on `http://localhost:5000`

## Cloud Deployment Options

### Heroku Deployment
1. Create a Heroku account and install Heroku CLI
2. Login to Heroku:
```bash
heroku login
```

3. Create a new Heroku app:
```bash
heroku create your-app-name
```

4. Deploy your application:
```bash
git push heroku main
```

### Alternative Cloud Platforms
- **AWS Elastic Beanstalk**: Suitable for production deployments
- **Google Cloud Platform**: Using App Engine or Cloud Run
- **Microsoft Azure**: Using App Service

## Environment Variables
Make sure to set up the following environment variables:
- Configure any API keys or sensitive information as environment variables
- Set `FLASK_ENV=production` for production deployment
