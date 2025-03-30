from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


class Transaction(BaseModel):
    """
    Pydantic model for representing a single transaction.  This provides
    strong data typing and validation.
    """
    payment_id: Optional[str] = Field(None, description="Unique identifier for the payment")
    transaction_particulars: Optional[str] = Field(None, description="Details of the transaction (payee, payer, method, etc.)")
    payment_date: Optional[datetime] = Field(None, description="Date of the payment")
    transaction_context: Optional[str] = Field(None, description="Context of the transaction (e.g., category, purpose)")
    deposit_amount: Optional[float] = Field(None, description="Amount deposited")
    withdrawal_amount: Optional[float] = Field(None, description="Amount withdrawn")
    current_balance: Optional[float] = Field(None, description="Current account balance")
    original_text: Optional[str] = Field(None, description="Original text from which transaction was extracted")

    def __str__(self):
        """Improved string representation for better logging/debugging."""
        return f"Transaction(payment_id={self.payment_id}, payment_date={self.payment_date}, deposit={self.deposit_amount}, withdrawal={self.withdrawal_amount}, balance={self.current_balance}, particulars={self.transaction_particulars})"