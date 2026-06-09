"""FSM states for campaign creation."""

from aiogram.fsm.state import State, StatesGroup


class CampaignCreationStates(StatesGroup):
    """States for campaign creation FSM."""

    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_city = State()
    waiting_for_budget = State()
    waiting_for_required_influencers = State()
    waiting_for_campaign_date = State()
    campaign_complete = State()
