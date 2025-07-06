from django.contrib import admin

from wallets.models import Transaction, Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("id", "label", "balance", "transaction_count")
    readonly_fields = ("balance",)
    search_fields = ("label",)
    list_filter = ()
    ordering = ("id",)

    def transaction_count(self, obj):
        return obj.transactions.count()

    transaction_count.short_description = "Transactions"

    class TransactionInline(admin.TabularInline):
        model = Transaction
        extra = 0
        readonly_fields = ("txid", "amount", "created_at")
        can_delete = False
        show_change_link = True

    inlines = [TransactionInline]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "txid", "wallet", "amount", "created_at")
    search_fields = ("txid",)
    list_filter = ("wallet",)
    ordering = ("-created_at",)

    readonly_fields = ("created_at",)
    fieldsets = (
        (None, {"fields": ("wallet", "txid", "amount")}),
        (
            "Meta",
            {
                "fields": ("created_at",),
                "classes": ("collapse",),
            },
        ),
    )
