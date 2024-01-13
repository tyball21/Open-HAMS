from datetime import datetime, timedelta
from backend.app import db
from backend.models.animal import Animal

def reset_daily_counters():
    """Resets the daily checkout counters for all animals."""
    try:
        animals = Animal.query.all()
        for animal in animals:
            animal.daily_checkout_count = 0
            animal.daily_checkout_duration = timedelta(hours=0)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error resetting daily counters: {e}")

# This function can be called by an external scheduler like cron
