from django_filters.rest_framework import CharFilter, FilterSet, NumberFilter

from wallets.models import Transaction


class TransactionFilter(FilterSet):
    amount_min = NumberFilter(field_name="amount", lookup_expr="gte")
    amount_max = NumberFilter(field_name="amount", lookup_expr="lte")
    wallet = NumberFilter(field_name="wallet")
    txid = CharFilter(field_name="txid", lookup_expr="icontains")

    class Meta:
        model = Transaction
        fields = ["wallet", "txid", "amount_min", "amount_max"]
