# utils/helpers.py
from datetime import datetime, timedelta
from typing import Dict, Optional

def format_date(date: datetime) -> str:
    return date.strftime("%Y-%m-%d")

def calculate_streak(last_completed: Optional[datetime]) -> int:
    if not last_completed:
        return 0
    
    days_since = (datetime.now() - last_completed).days
    return days_since if days_since <= 1 else 0