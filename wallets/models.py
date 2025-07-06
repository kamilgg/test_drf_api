from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    """
    Base model with created_at and updated_at
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Wallet(BaseModel):
    """
    Wallet model
    Balance is always equal to the sum of all related transactions and cannot be negative
    """

    label = models.CharField(max_length=255)
    balance = models.DecimalField(
        max_digits=30,
        decimal_places=18,
        default=Decimal("0.0"),
    )

    class Meta:
        indexes = [
            models.Index(fields=["label"]),
        ]
        verbose_name = _("Wallet")
        verbose_name_plural = _("Wallets")

        # To be sure that balance is not negative
        constraints = [
            models.CheckConstraint(
                condition=models.Q(balance__gte=Decimal("0.0")),
                name="wallet_balance_non_negative",
            )
        ]

    def __str__(self) -> str:
        return f"Wallet({self.label})"


class Transaction(BaseModel):
    """
    Wallet transaction model
    """

    wallet = models.ForeignKey(
        Wallet,
        related_name="transactions",
        on_delete=models.CASCADE,
    )
    txid = models.CharField(
        max_length=255,
        unique=True,
        help_text="Unique transaction identifier",
    )
    amount = models.DecimalField(
        max_digits=30,
        decimal_places=18,
        help_text="Can be negative. Up to 18 digits precision.",
    )

    class Meta:
        indexes = [
            models.Index(fields=["wallet"]),
            models.Index(fields=["txid"]),
        ]
        ordering = ["-created_at"]
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")

    def __str__(self) -> str:
        return f"Transaction({self.txid}): {self.amount}"

    def clean(self) -> None:
        """
        Validate that applying this transaction will not cause negative balance
        """
        if not self.wallet_id:
            return

        current_balance = self.wallet.balance
        delta = self.amount

        if self.pk:
            old = Transaction.objects.get(pk=self.pk)
            delta -= old.amount

        projected = current_balance + delta
        if projected < Decimal("0.0"):
            raise ValidationError(_("Wallet balance cannot become negative."))

    def save(self, *args, **kwargs) -> None:
        """
        Save transaction and update wallet balance atomically
        """
        with transaction.atomic():
            self.clean()
            is_update = self.pk is not None
            old_amount = None

            if is_update:
                old_amount = Transaction.objects.get(pk=self.pk).amount

            super().save(*args, **kwargs)

            if is_update:
                delta = self.amount - old_amount
            else:
                delta = self.amount

            self.wallet.balance = self.wallet.balance + delta
            if self.wallet.balance < Decimal("0.0"):
                raise ValidationError(_("Wallet balance cannot be negative."))

            self.wallet.save()

    def delete(self, *args, **kwargs) -> None:
        """
        Deleting a transaction rolls back its effect on the wallet balance
        """
        with transaction.atomic():
            self.wallet.balance = self.wallet.balance - self.amount
            if self.wallet.balance < Decimal("0.0"):
                raise ValidationError(
                    _("Cannot delete: wallet balance would become negative.")
                )
            self.wallet.save()
            super().delete(*args, **kwargs)
