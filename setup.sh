# Initialize git if not already done
git init
git add .
git commit -m "Initial commit"

# Create Heroku app
heroku create RockPaperScissors

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=HRKU-AA7GoieTSqkJnA7rq5_cubkA6rUkGiTdKsTHrfjHuT5A_____wtc_O7zuUMY

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Collect static files
heroku run python manage.py collectstatic --noinput