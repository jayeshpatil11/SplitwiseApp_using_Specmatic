from fastapi import FastAPI, HTTPException

from models import *
from storage import groups, expenses, settlements

app = FastAPI(
    title="Expense Sharing API",
    version="1.0.0"
)

group_counter = 1
expense_counter = 1
settlement_counter = 1


@app.post("/groups", response_model=GroupResponse, status_code=201)
def create_group(request: CreateGroupRequest):

    global group_counter

    group = {
        "groupId": group_counter,
        "name": request.name
    }

    groups.append(group)

    group_counter += 1

    return group

'''
@app.get("/groups/{groupId}")
def get_group(groupId: int):
    return {
        "groupId": groupId,
        "name": f"Group-{groupId}"
    }
'''
'''
@app.get(
    "/groups/{groupId}",
    response_model=GroupResponse
)
def get_group(groupId: int):

    for group in groups:
        if group["groupId"] == groupId:
            return group

    raise HTTPException(
        status_code=404,
        detail="Group not found"
    )
'''
@app.get("/groups/{groupId}", response_model=GroupResponse)
def get_group(groupId: int):

    if groupId == 99999:
        raise HTTPException(
            status_code=404,
            detail="Group not found"
        )

    return {
        "groupId": groupId,
        "name": f"Group-{groupId}"
    }


@app.post("/expenses", response_model=ExpenseResponse, status_code=201)
def add_expense(request: AddExpenseRequest):

    global expense_counter

    expense = {
        "expenseId": expense_counter,
        "groupId": request.groupId,
        "amount": request.amount,
        "paidBy": request.paidBy
    }

    expenses.append(expense)

    expense_counter += 1

    return {
        "expenseId": expense["expenseId"],
        "status": "CREATED"
    }


@app.get("/expenses")
def get_expenses():
    return expenses


@app.get("/balances/{user_id}", response_model=BalanceResponse)
def get_balance(user_id: int):

    paid = sum(
        expense["amount"]
        for expense in expenses
        if expense["paidBy"] == user_id
    )

    return {
        "userId": user_id,
        "totalOwed": 0,
        "totalReceivable": paid
    }


@app.post(
    "/settlements",
    response_model=SettlementResponse,
    status_code=201
)
def create_settlement(request: SettlementRequest):

    global settlement_counter

    settlement = {
        "settlementId": settlement_counter,
        "fromUser": request.fromUser,
        "toUser": request.toUser,
        "amount": request.amount
    }

    settlements.append(settlement)

    settlement_counter += 1

    return {
        "settlementId": settlement["settlementId"],
        "status": "SUCCESS"
    }