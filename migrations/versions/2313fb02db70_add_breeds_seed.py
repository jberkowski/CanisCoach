"""Add breeds seed

Revision ID: 2313fb02db70
Revises: 00339a73c7b9
Create Date: 2026-08-09 11:10:37.175081

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2313fb02db70'
down_revision = '00339a73c7b9'
branch_labels = None
depends_on = None

BREED_NAMES = [
                "Australian Kelpie",
                "Australian Shepherd (Aussie)",
                "Beagle",
                "Border Collie",
                "Cocker Spaniel",
                "Doberman",
                "Golden Retriever",
                "Jack Russell Terrier",
                "Labrador Retriever",
                "Nova Scotia Duck Tolling Retriever (Toller)",
                "Belgian Malinois",
                "Poodle",
                "Siberian Husky",
                "Welsh Corgi",
                "Whippet"
             ]


def upgrade():
    # Seed breeds table 
    breeds = sa.table(
        "breeds",
        sa.column('breed_name', sa.String)
    )

    op.bulk_insert(
        breeds,
        [
            {"breed_name": "Australian Kelpie"},
            {"breed_name": "Australian Shepherd (Aussie)"},
            {"breed_name": "Beagle"},
            {"breed_name": "Border Collie"},
            {"breed_name": "Cocker Spaniel"},
            {"breed_name": "Doberman"},
            {"breed_name": "Golden Retriever"},
            {"breed_name": "Jack Russell Terrier"},
            {"breed_name": "Labrador Retriever"},
            {"breed_name": "Nova Scotia Duck Tolling Retriever (Toller)"},
            {"breed_name": "Belgian Malinois"},
            {"breed_name": "Poodle"},
            {"breed_name": "Siberian Husky"},
            {"breed_name": "Welsh Corgi"},
            {"breed_name": "Whippet"}
        ]
    )


def downgrade():
    breeds = sa.table("breeds", sa.column('breed_name', sa.String))
    op.execute(
        breeds.delete().where(breeds.c.breed_name.in_(BREED_NAMES))
    )
