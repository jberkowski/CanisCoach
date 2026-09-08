"""Add disciplines seed

Revision ID: b006bc0abe74
Revises: 2313fb02db70
Create Date: 2026-08-09 11:33:12.012659

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b006bc0abe74'
down_revision = '2313fb02db70'
branch_labels = None
depends_on = None

DISC_NAMES = [
    "Agility",
    "Bikejoring",
    "Canicross",
    "Dog Frisbee",
    "Flyball",
    "Nosework",
    "Rally-Obedience"
]


def upgrade():
    # Seed disciplines table 
    disciplines = sa.table(
        "disciplines",
        sa.Column('disc_name', sa.String),
        sa.Column('disc_type', sa.Integer),
        sa.Column('disc_usr_id', sa.Integer),
        sa.Column('disc_active', sa.Integer)
    )

    op.bulk_insert(
        disciplines,
        [
            {"disc_name": "Agility", "disc_type": 0, "disc_usr_id": None, "disc_active": 1},
            {"disc_name": "Bikejoring", "disc_type": 0, "disc_usr_id": None, "disc_active": 1},
            {"disc_name": "Canicross", "disc_type": 0, "disc_usr_id": None, "disc_active": 1},
            {"disc_name": "Dog Frisbee", "disc_type": 0, "disc_usr_id": None, "disc_active": 1},
            {"disc_name": "Flyball", "disc_type": 0, "disc_usr_id": None, "disc_active": 1},
            {"disc_name": "Nosework", "disc_type": 0, "disc_usr_id": None, "disc_active": 1},
            {"disc_name": "Rally-Obedience", "disc_type": 0, "disc_usr_id": None, "disc_active": 1}

        ]
    )


def downgrade():
    disciplines = sa.table("disciplines", sa.Column('disc_name', sa.String))
    op.execute(
            disciplines.delete().where(disciplines.c.disc_name.in_(DISC_NAMES))
        )
