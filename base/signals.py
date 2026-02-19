"""
=============================================================================
Django Signals — Auto-create Profile when a User is created
=============================================================================

WHAT ARE SIGNALS?
-----------------
Signals are like "event listeners" in Django. They let you say:
"Hey Django, whenever THIS event happens, automatically do THAT."

Django has built-in signals like:
    - post_save   → fires AFTER a model instance is saved to the database
    - pre_save    → fires BEFORE a model instance is saved
    - post_delete → fires AFTER a model instance is deleted
    - pre_delete  → fires BEFORE a model instance is deleted

WHY DO WE NEED SIGNALS HERE?
-----------------------------
We have two separate models:
    - User (Django's built-in) → handles login, username, password
    - Profile (our custom)     → handles bio, avatar

When a new user registers, we want a Profile to be created AUTOMATICALLY.

Without signals, we'd have to manually write:
    Profile.objects.create(user=user)
...in EVERY place a user can be created:
    - Register view
    - Admin panel
    - Django shell
    - Management commands
    - etc.

If we forget even ONE place, that user won't have a profile → app crashes!

Signals solve this by hooking into Django's model lifecycle:
    "Every time a User is saved → check if we need to create a Profile"

HOW IT WORKS (step by step):
----------------------------
1. A new user registers on the site
2. Django saves the User to the database (User.save())
3. Django sends a `post_save` signal automatically
4. Our `create_profile` function listens for that signal
5. It checks: was this a NEW user? (created=True)
6. If yes → creates a Profile linked to that user
7. Now the user has a profile, even though we never manually created one!

REAL-WORLD ANALOGY:
-------------------
Think of a hotel:
    Without signals → Receptionist manually calls housekeeping, room service,
                      and billing for every new guest. Forget one = problems.
    With signals   → Automatic system: guest checks in → housekeeping, room
                      service, billing are ALL notified automatically.

HOW TO REGISTER SIGNALS:
------------------------
Signals only work if Python imports this file. That's why in apps.py we have:

    class BaseConfig(AppConfig):
        def ready(self):
            import base.signals   # ← This line loads our signals on startup

Without this, Django never knows these listeners exist!

KEY TERMS:
----------
    @receiver    → Decorator that says "this function listens for a signal"
    post_save    → The signal/event type (fires after .save() is called)
    sender=User  → Only listen when a USER is saved (not Room, Message, etc.)
    instance     → The actual User object that was just saved
    created      → Boolean: True if brand new, False if just updated
    **kwargs     → Extra keyword arguments (required by Django's signal API)
=============================================================================
"""

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Runs every time a User is saved.
    If the user was JUST CREATED (not updated), create a Profile for them.

    Example flow:
        1. User.objects.create(username='john', password='...')
        2. Django saves → sends post_save signal
        3. This function catches it → created=True
        4. Creates Profile(user=john) automatically
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Runs on EVERY User save (create AND update).
    Ensures the profile stays in sync with the user.

    Also acts as a SAFETY NET: if somehow a user exists without a profile
    (e.g., created before we added signals), it creates one on the fly
    instead of crashing.
    """
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)
