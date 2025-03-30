from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any, Type
from datetime import datetime
import json

class StructuredLLMWrapper:
    """
    A wrapper that calls the underlying LLM and parses its output into a Pydantic model.
    
    Parameters:
        llm: The underlying language model. Expected to have an `invoke` method.
        schema: A Pydantic model class that defines the structured output.
        include_raw: If True, returns both the raw output and parsed object.
    """
    def __init__(self, llm: Any, schema: Type[BaseModel], include_raw: bool = False):
        self.llm = llm
        self.schema = schema
        self.include_raw = include_raw

    def invoke(self, input_data: Any) -> Any:
        # Call the underlying LLM's invoke method
        raw_output = self.llm.invoke(input_data)
        
        # Attempt to parse the output as JSON
        try:
            parsed_json = json.loads(raw_output)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Failed to decode LLM output as JSON: {e}. Raw output: {raw_output}"
            )
        
        # Validate and parse into the structured schema
        try:
            structured_output = self.schema.parse_obj(parsed_json)
        except Exception as e:
            raise ValueError(
                f"Failed to parse structured output: {e}. Parsed JSON: {parsed_json}"
            )
        
        if self.include_raw:
            return {"raw": raw_output, "parsed": structured_output}
        else:
            return structured_output

    def __call__(self, input_data: Any) -> Any:
        return self.invoke(input_data)

def with_structured_output(llm: Any, schema: Type[BaseModel], include_raw: bool = False) -> StructuredLLMWrapper:
    """
    Utility to wrap any LLM with structured output capability.
    """
    return StructuredLLMWrapper(llm, schema, include_raw)


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