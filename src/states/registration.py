"""FSM states for registration."""

from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    """States for user registration FSM."""

    waiting_for_full_name = State()
    waiting_for_username = State()
    waiting_for_city = State()
    waiting_for_role = State()
    registration_complete = State()
