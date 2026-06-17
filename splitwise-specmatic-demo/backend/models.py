from pydantic import BaseModel, Field
from typing import List

class CreateGroupRequest(BaseModel):
    name: str =Field(min_length=1)

class GroupResponse(BaseModel):
    groupId: int
    name: str

class AddExpenseRequest(BaseModel):
    groupId: int = Field(gt=0)
    amount: float = Field(gt=0)
    paidBy: int = Field(gt=0)

class ExpenseResponse(BaseModel):
    expenseId: int
    status: str

class Expense(BaseModel):
    expenseId: int
    groupId: int
    amount: float
    paidBy: int

class BalanceResponse(BaseModel):
    userId: int
    totalOwed: float
    totalReceivable: float

class SettlementRequest(BaseModel):
    fromUser: int = Field(gt=0)
    toUser: int = Field(gt=0)
    amount: float = Field(gt=0)

from typing import Literal

class SettlementResponse(BaseModel):
    settlementId: int
    status: Literal["SUCCESS"]

class ErrorResponse(BaseModel):
    detail: str


#commands
'''
MSYS_NO_PATHCONV=1 docker run --rm -v /c/splitwise-specmatic-demo:/work -w /work --add-host=host.docker.internal:host-gateway specmatic/specmatic test --testBaseURL=http://host.docker.internal:8000 openapi/expense-sharing-api.yaml

cd /c/splitwise-specmatic-demo/backend
uvicorn main:app --reload

'''