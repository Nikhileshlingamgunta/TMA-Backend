# TMA-Backend
# Task Management Application 
# Backend (Flask) 
# 1. Navigate to the backend directory:
cd ../backend
# 2. Set up a virtual environment:
python -m venv venv

source venv/bin/activate
# 3. Install dependencies:
pip install -r requirements.txt
# 4. Download the necessary spaCy model:
python -m spacy download en_core_web_sm
# 5. Start the Flask server:
python app.py
