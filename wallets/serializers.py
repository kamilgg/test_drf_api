from decimal import Decimal

from rest_framework_json_api import serializers
from rest_framework_json_api.relations import ResourceRelatedField

from wallets.models import Transaction, Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ("id", "label", "balance")
        read_only_fields = ("balance",)


class TransactionSerializer(serializers.ModelSerializer):
    wallet = ResourceRelatedField(queryset=Wallet.objects.all())

    class Meta:
        model = Transaction
        fields = ("id", "wallet", "txid", "amount", "created_at")
        read_only_fields = ("created_at",)

    def validate(self, data):
        """
        Ensure that wallet balance will not become negative.
        """
        wallet = data.get("wallet")
        amount = data.get("amount")

        if self.instance:
            wallet = wallet or self.instance.wallet
            amount = amount if amount is not None else self.instance.amount

        if wallet is None or amount is None:
            raise serializers.ValidationError("Wallet and amount must be provided.")

        if self.instance:
            delta = amount - self.instance.amount
        else:
            delta = amount

        projected_balance = wallet.balance + delta

        if projected_balance < Decimal("0.0"):
            raise serializers.ValidationError("Wallet balance cannot become negative.")

        return data
