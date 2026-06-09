"""Initial schema creation.

Revision ID: 001
Revises:
Create Date: 2026-06-09 23:15:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create initial database schema."""
    # Create enum types
    user_role_enum = postgresql.ENUM(
        "advertiser", "influencer", "admin", name="userrole"
    )
    user_role_enum.create(op.get_bind(), checkfirst=True)

    campaign_status_enum = postgresql.ENUM(
        "draft", "active", "paused", "completed", "cancelled", name="campaignstatus"
    )
    campaign_status_enum.create(op.get_bind(), checkfirst=True)

    application_status_enum = postgresql.ENUM(
        "pending", "accepted", "rejected", "completed", "cancelled",
        name="applicationstatus"
    )
    application_status_enum.create(op.get_bind(), checkfirst=True)

    # Create users table
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("telegram_id", sa.Integer(), nullable=False),
        sa.Column("role", user_role_enum, nullable=False, server_default="influencer"),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("username", sa.String(255), nullable=True),
        sa.Column("city", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("telegram_id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index("ix_users_id", "users", ["id"])
    op.create_index("ix_users_telegram_id", "users", ["telegram_id"])
    op.create_index("ix_users_username", "users", ["username"])

    # Create influencer_profiles table
    op.create_table(
        "influencer_profiles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("niche", sa.String(255), nullable=True),
        sa.Column("followers_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("instagram_link", sa.String(500), nullable=True),
        sa.Column("tiktok_link", sa.String(500), nullable=True),
        sa.Column("telegram_link", sa.String(500), nullable=True),
        sa.Column("advertising_price", sa.Float(), nullable=False, server_default="0"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index("ix_influencer_profiles_id", "influencer_profiles", ["id"])

    # Create campaigns table
    op.create_table(
        "campaigns",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("advertiser_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("city", sa.String(255), nullable=False),
        sa.Column("budget", sa.Float(), nullable=False),
        sa.Column("required_influencers", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("campaign_date", sa.DateTime(), nullable=False),
        sa.Column("status", campaign_status_enum, nullable=False, server_default="draft"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["advertiser_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_campaigns_id", "campaigns", ["id"])

    # Create applications table
    op.create_table(
        "applications",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("campaign_id", sa.Integer(), nullable=False),
        sa.Column("influencer_id", sa.Integer(), nullable=False),
        sa.Column("status", application_status_enum, nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["campaign_id"], ["campaigns.id"]),
        sa.ForeignKeyConstraint(["influencer_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_applications_id", "applications", ["id"])


def downgrade() -> None:
    """Drop all tables and enums."""
    op.drop_index("ix_applications_id", "applications")
    op.drop_table("applications")
    op.drop_index("ix_campaigns_id", "campaigns")
    op.drop_table("campaigns")
    op.drop_index("ix_influencer_profiles_id", "influencer_profiles")
    op.drop_table("influencer_profiles")
    op.drop_index("ix_users_username", "users")
    op.drop_index("ix_users_telegram_id", "users")
    op.drop_index("ix_users_id", "users")
    op.drop_table("users")

    # Drop enum types
    sa.Enum(name="applicationstatus").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="campaignstatus").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="userrole").drop(op.get_bind(), checkfirst=True)
