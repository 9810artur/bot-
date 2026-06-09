"""FSM states for influencer profile creation."""

from aiogram.fsm.state import State, StatesGroup


class InfluencerProfileStates(StatesGroup):
    """States for influencer profile creation FSM."""

    waiting_for_niche = State()
    waiting_for_followers = State()
    waiting_for_instagram = State()
    waiting_for_tiktok = State()
    waiting_for_telegram = State()
    waiting_for_price = State()
    profile_complete = State()
