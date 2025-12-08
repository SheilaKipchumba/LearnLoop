LearnLoop - Peer-to-Peer Micro-Learning Platform

Overview
LearnLoop is a Django-based peer-to-peer micro-learning platform that enables students to create, share, and monetize bite-sized educational content called "Loops". The platform facilitates direct student-to-student learning while aligning with UN Sustainable Development Goal 4: Quality Education.

Core Problem & Solution
Problem: Students struggle with complex topics, knowledge sharing is fragmented, and students with expertise lack monetization channels.

Solution: A centralized platform where:

Students create 5-15 minute focused micro-lessons

Learners access content from peers who explain concepts in student-friendly language

Creators monetize quality educational content through M-Pesa integration

Community-driven knowledge sharing flourishes

SDG Alignment
Primary: SDG 4 - Quality Education
4.1: Ensure inclusive and equitable quality education

4.4: Increase youth with relevant skills for employment

4.7: Education for sustainable development

Impact Metrics:
 Accessibility: Free basic content with affordable premium options

 Peer Learning: Students teaching students in accessible language

 Economic Empowerment: Students earn from their expertise

 Community Building: Collaborative learning environment

 Features
Core Features
User Authentication: Registration, login, profile management

Loop Creation: Create micro-lessons with text, images, videos

Content Browsing: Search and filter by category/difficulty

Social Features: Likes, comments, and ratings

Monetization: M-Pesa integration for premium content

Responsive Design: Mobile-friendly Bootstrap interface

Admin Dashboard: Content moderation and user management

 Technology Stack
Backend
Django 4.2 (Python web framework)

SQLite (development) / PostgreSQL (production)

Django REST Framework (API endpoints)

Frontend
Bootstrap 5 (responsive CSS framework)

JavaScript (ES6+) for interactivity

Font Awesome & Bootstrap Icons

Payment Integration
Safaricom M-Pesa Daraja API (STK Push)

RESTful APIs for payment processing

Development Tools
Git & GitHub for version control

Python Virtualenv for environment isolation

VS Code / PyCharm for development

 Installation Guide
Prerequisites
Python 3.8 or higher

pip (Python package manager)

Git

Web browser (Chrome, Firefox, etc.)

Step-by-Step Setup
1. Clone the Repository
bash
git clone https://github.com/SheilaKipchumba/learnloop.git
cd learnloop
2. Create Virtual Environment
bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
bash
pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file in the project root:

env
# .env file
DEBUG=True
SECRET_KEY=your-secret-key-change-in-production
ALLOWED_HOSTS=127.0.0.1,localhost

# M-Pesa Sandbox Credentials (get from Safaricom Developer Portal)
MPESA_CONSUMER_KEY=your_sandbox_consumer_key
MPESA_CONSUMER_SECRET=your_sandbox_consumer_secret
MPESA_SHORTCODE=174379
MPESA_PASSKEY=your_sandbox_passkey
MPESA_CALLBACK_URL=http://localhost:8000/payments/callback/
5. Run Database Migrations
bash
python manage.py makemigrations
python manage.py migrate
6. Create Superuser
bash
python manage.py createsuperuser --username admin --email admin@learnloop.com --noinput
python -c "from django.contrib.auth.models import User; user = User.objects.get(username='admin'); user.set_password('admin123'); user.save(); print('Admin created: admin / admin123')"
7. Run Development Server
bash
python manage.py runserver
Visit http://127.0.0.1:8000 in your browser!



 Project Structure
text
learnloop/
├── manage.py
├── requirements.txt
├── .env
├── .gitignore
├── learnloop/          # Main project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── loops/              # Core learning content app
│   ├── models.py      # Loop, Comment, Like, Rating models
│   ├── views.py       # Business logic
│   ├── urls.py        # URL routing
│   ├── forms.py       # Loop creation/editing forms
│   └── templates/loops/ # Loop templates
├── users/              # User management app
│   ├── models.py      # User Profile model
│   ├── views.py       # Authentication views
│   ├── urls.py        # User URLs
│   ├── forms.py       # Registration forms
│   └── templates/users/ # User templates
├── payments/           # Payment processing app
│   ├── models.py      # Payment models
│   ├── views.py       # Payment views
│   ├── urls.py        # Payment URLs
│   ├── mpesa.py       # M-Pesa API integration
│   └── templates/payments/ # Payment templates
|
├── templates/          # Base templates
│   └── base.html      # Main template with 
 User Guide
For Learners (Students)
Getting Started
Register: Click "Sign Up" and fill in your details

Verify Email: Check your email for verification

Complete Profile: Add a profile picture and bio

Browse Loops: Explore content by category or search

Learning Process
Search: Use the search bar to find specific topics

Filter: Narrow results by category and difficulty

Access: Click on a loop to view content

Engage: Like, comment, and rate helpful content

Upgrade: Use M-Pesa to access premium loops

Key Features
Free Loops: Unlimited access to free content

Premium Access: Pay per premium loop

Learning History: Track your progress

Saved Loops: Bookmark loops for later

For Creators (Teachers or students)
Creating Loops
Navigate: Click "Create Loop" in the navbar

Fill Details:

Title and description

Content (main educational material)

Category and difficulty level

Optional: Video URL or attachment

Set Pricing: Choose free or set a price (50-500 KES)

Publish: Submit for review

Monetization
Revenue Split: 80% to creator, 20% platform fee

Pricing Strategy: Set your own prices

Payment Method: M-Pesa integration

Earnings Tracking: View your earnings in dashboard

Best Practices
Create clear, concise content

Use relevant examples

Add helpful media (images, videos)

Set appropriate difficulty levels

Engage with learner comments

For Administrators
Admin Access
Login with superuser credentials

Access admin panel at /admin/

Use sidebar to navigate sections

Key Admin Tasks
User Management: Approve registrations, manage accounts

Content Moderation: Review loops, handle reports

Payment Monitoring: Track transactions

Platform Analytics: Monitor usage metrics

Admin Dashboard Features
User management interface

Content approval system

Payment transaction logs

Platform analytics

System configuration

 M-Pesa API Documentation
Overview
LearnLoop integrates with Safaricom's M-Pesa Daraja API for seamless mobile payments in Kenya.



Support Resources
GitHub Issues: Report bugs and request features

Documentation: Check this README and code comments

Community Forum: Get help from other developers

Email Support: Contact for critical issues

 Contributing
We welcome contributions! Here's how:

Fork the repository

Create a feature branch (git checkout -b feature/AmazingFeature)

Commit changes (git commit -m 'Add AmazingFeature')

Push to branch (git push origin feature/AmazingFeature)

Open a Pull Request

Development Guidelines
Follow PEP 8 Python style guide

Write meaningful commit messages

Add tests for new features

Update documentation accordingly

Ensure code is well-commented


 License
This project is licensed under the MIT License - see the LICENSE file for details.

text
MIT License

Copyright (c) 2024 LearnLoop

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
 Acknowledgments
Django Software Foundation for the amazing web framework

Bootstrap Team for the responsive CSS framework

Safaricom PLC for the M-Pesa API

UN Sustainable Development Goals for inspiration

All Contributors who helped build LearnLoop

Open Source Community for countless tools and libraries

 Project Status
Component	Status
Core Platform	✅ Production Ready 

M-Pesa Integration	✅ Production Ready

User Authentication	✅ Complete

Content Management	✅ Complete

Payment System	✅ Complete

Admin Dashboard	✅ Complete

Mobile Responsive	✅ Complete

Testing Suite	⚠️ In Progress

Performance Optimization	⚠️ In Progress

 Future Roadmap
Phase 1 (Q1 2025)
Advanced analytics dashboard

Real-time notifications

Enhanced search functionality

Learning paths and collections

Phase 2 (Q2 2025)
Mobile app (React Native)

Video upload and processing

Peer review system

Certificate generation

Phase 3 (Q3 2025)
Multi-language support

AI-powered recommendations

Advanced monetization options

Integration with learning institutions


 LearnLoop
Making Quality Education Accessible to All

Part of the solution for UN Sustainable Development Goal 4



Last Updated: December 2024
Version: 1.0.0
Status: Production Ready

 
