"""Initial migration

Revision ID: b973c6ebaf4a
Revises: 
Create Date: 2025-05-25 17:44:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "b973c6ebaf4a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create ENUM type for user role
    userrole = postgresql.ENUM("admin", "user", name="userrole")
    userrole.create(op.get_bind())

    # Create ENUM type for order status
    orderstatus = postgresql.ENUM(
        "pending", "completed", "cancelled", name="orderstatus"
    )
    orderstatus.create(op.get_bind())

    # Create users table
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column(
            "role",
            postgresql.ENUM("admin", "user", name="userrole"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(
        op.f("ix_users_created_at"), "users", ["created_at"], unique=False
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(
        op.f("ix_users_username"), "users", ["username"], unique=True
    )

    # Create clients table
    op.create_table(
        "clients",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("cpf", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_clients_cpf"), "clients", ["cpf"], unique=True)
    op.create_index(
        op.f("ix_clients_created_at"), "clients", ["created_at"], unique=False
    )
    op.create_index(
        op.f("ix_clients_email"), "clients", ["email"], unique=True
    )
    op.create_index(op.f("ix_clients_id"), "clients", ["id"], unique=False)
    op.create_index(op.f("ix_clients_name"), "clients", ["name"], unique=False)

    # Create products table
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("stock", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_products_created_at"),
        "products",
        ["created_at"],
        unique=False,
    )
    op.create_index(op.f("ix_products_id"), "products", ["id"], unique=False)
    op.create_index(
        op.f("ix_products_name"), "products", ["name"], unique=False
    )

    # Create orders table
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            postgresql.ENUM(
                "pending", "completed", "cancelled", name="orderstatus"
            ),
            nullable=False,
        ),
        sa.Column("total", sa.Float(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["client_id"],
            ["clients.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_orders_client_id"), "orders", ["client_id"], unique=False
    )
    op.create_index(
        op.f("ix_orders_created_at"), "orders", ["created_at"], unique=False
    )
    op.create_index(op.f("ix_orders_id"), "orders", ["id"], unique=False)

    # Create order_items table
    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("unit_price", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(
            ["order_id"],
            ["orders.id"],
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_order_items_id"), "order_items", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_order_items_order_id"),
        "order_items",
        ["order_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_order_items_product_id"),
        "order_items",
        ["product_id"],
        unique=False,
    )

    # Create whatsapp_messages table
    op.create_table(
        "whatsapp_messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("message", sa.String(), nullable=False),
        sa.Column(
            "sent_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["client_id"],
            ["clients.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_whatsapp_messages_client_id"),
        "whatsapp_messages",
        ["client_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_whatsapp_messages_id"),
        "whatsapp_messages",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_whatsapp_messages_sent_at"),
        "whatsapp_messages",
        ["sent_at"],
        unique=False,
    )


def downgrade():
    # Drop tables in reverse order
    op.drop_index(
        op.f("ix_whatsapp_messages_sent_at"), table_name="whatsapp_messages"
    )
    op.drop_index(
        op.f("ix_whatsapp_messages_id"), table_name="whatsapp_messages"
    )
    op.drop_index(
        op.f("ix_whatsapp_messages_client_id"), table_name="whatsapp_messages"
    )
    op.drop_table("whatsapp_messages")

    op.drop_index(op.f("ix_order_items_product_id"), table_name="order_items")
    op.drop_index(op.f("ix_order_items_order_id"), table_name="order_items")
    op.drop_index(op.f("ix_order_items_id"), table_name="order_items")
    op.drop_table("order_items")

    op.drop_index(op.f("ix_orders_id"), table_name="orders")
    op.drop_index(op.f("ix_orders_created_at"), table_name="orders")
    op.drop_index(op.f("ix_orders_client_id"), table_name="orders")
    op.drop_table("orders")

    op.drop_index(op.f("ix_products_name"), table_name="products")
    op.drop_index(op.f("ix_products_id"), table_name="products")
    op.drop_index(op.f("ix_products_created_at"), table_name="products")
    op.drop_table("products")

    op.drop_index(op.f("ix_clients_name"), table_name="clients")
    op.drop_index(op.f("ix_clients_id"), table_name="clients")
    op.drop_index(op.f("ix_clients_email"), table_name="clients")
    op.drop_index(op.f("ix_clients_created_at"), table_name="clients")
    op.drop_index(op.f("ix_clients_cpf"), table_name="clients")
    op.drop_table("clients")

    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_index(op.f("ix_users_created_at"), table_name="users")
    op.drop_table("users")

    # Drop ENUM types
    op.execute("DROP TYPE orderstatus")
    op.execute("DROP TYPE userrole")
