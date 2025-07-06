from rest_framework_json_api import filters, views
from rest_framework_json_api.django_filters import DjangoFilterBackend

from wallets.filters import TransactionFilter
from wallets.models import Transaction, Wallet
from wallets.serializers import TransactionSerializer, WalletSerializer


class WalletViewSet(views.ModelViewSet):
    """
    API endpoint for wallets
    Balance is read-only and calculated automatically
    """

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    http_method_names = [
        "get",
        "post",
        "patch",
        "head",
        "options",
        "delete",
    ]  # IDK what methods are needed (like can we delete wallet? Depends on requirements)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["id", "label"]
    ordering = ["id", "label"]


class TransactionViewSet(views.ModelViewSet):
    """
    API endpoint for transactions
    Creates, updates, and deletes transactions, modifying the wallet balance
    """

    queryset = Transaction.objects.select_related("wallet").all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = TransactionFilter
    ordering_fields = ["amount", "created_at", "txid"]
    ordering = ["-created_at"]
