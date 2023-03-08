from django.contrib import admin

from .models import Token, TokenOrder, TokenRound


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ["name", "total_amount", "total_amount_sold"]


@admin.register(TokenRound)
class TokenRoundAdmin(admin.ModelAdmin):
    list_display = [
        "unit_price",
        "total_cost",
        "percent_share",
        "is_active",
        "is_complete",
    ]


@admin.register(TokenOrder)
class TokenOrderAdmin(admin.ModelAdmin):
    list_display = ["buyer", "buyer_parent", "type", "amount", "reward", "price_sum"]
