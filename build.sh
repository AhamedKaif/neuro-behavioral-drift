#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Building frontend..."
cd frontend
npm install
npm run build
cd ..

echo "Installing backend dependencies..."
cd backend
pip install -r requirements.txt
pip install gunicorn

echo "Initializing database..."
python db.py

echo "Training Machine Learning Model..."
cd ../ml-model
python generate_dataset.py
python train.py

echo "Build process complete!"
