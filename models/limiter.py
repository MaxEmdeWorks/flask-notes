"""
Rate limiter configuration for Flask Notes app.
"""
import os
import time

from flask import render_template, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Smart key function: bypass rate limit after 60s session time
def smart_key():
    key = f"rl_{get_remote_address()}"
    if key in session and time.time() - session[key] >= 60:
        session.pop(key, None)
        return f"cleared_{get_remote_address()}_{int(time.time())}"
    return get_remote_address()

# Create limiter instance
limiter = Limiter(
    enabled=os.getenv('FLASK_LIMITER_ENABLED', 'False'),
    storage_uri=os.getenv('FLASK_LIMITER_STORAGE_URI', 'memory://'),
    default_limits=[os.getenv('FLASK_LIMITER_DEFAULT_LIMIT', '50 per minute')],
    strategy="moving-window",
    key_func=smart_key
)

# Rate limit handler
def rate_limit_handler(e):
    key = f"rl_{get_remote_address()}"
    now = time.time()

    if key not in session:
        session[key] = now
        retry_after = 60
    else:
        retry_after = max(1, int(60 - (now - session[key])))

    reset_time = time.strftime('%H:%M:%S', time.localtime(now + retry_after))
    return render_template('errors/rate_limit.html', retry_after=retry_after, limit_description=getattr(e, 'description', 'Rate limit exceeded'), reset_time=reset_time), 429

