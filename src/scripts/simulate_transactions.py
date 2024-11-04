import asyncio

from src.enums.transactions_types import TransactionsTypes
from src.schemas.bank_account import BankAccountRequest
from src.schemas.transaction import (
    TransactionDepositRequest,
    TransactionTransferRequest,
    TransactionWithdrawRequest,
)
from src.services.bank_account import BankAccountService
from src.services.transaction import TransactionService

transfer_queue = asyncio.Queue()


async def transfer_worker(transaction_service):
    while True:
        transfer_data = await transfer_queue.get()
        await transaction_service.create_bank_transfer(data=transfer_data)
        transfer_queue.task_done()


async def main():
    bank_account = BankAccountService()
    transaction = TransactionService()

    asyncio.create_task(transfer_worker(transaction))

    await bank_account.create(
        data=BankAccountRequest(account_number=1, balance=0)
    )
    await bank_account.create(
        data=BankAccountRequest(account_number=2, balance=0)
    )
    await bank_account.create(
        data=BankAccountRequest(account_number=3, balance=0)
    )

    # Transação 1: Depósito
    data = TransactionDepositRequest(account_number=1, balance=100)
    deposit = await transaction.create_bank_deposit(data=data)
    print("Depósito")
    print(f"Saldo da Conta {deposit.account_number}: {deposit.balance}")
    print("----------------$$----------------\n")

    # Transação 2: Saque
    data = TransactionWithdrawRequest(account_number=1, balance=50)
    withdraw = await transaction.create_bank_withdraw(data=data)
    print("Saque")
    print(f"Saldo da Conta {withdraw.account_number}: {withdraw.balance}")
    print("----------------$$----------------\n")

    # Transação 3: Transferência
    data = TransactionTransferRequest(
        type=TransactionsTypes.TRANSFER.value,
        from_account=TransactionDepositRequest(account_number=1, balance=30),
        to_account=2,
    )
    await transfer_queue.put(data)
    await transfer_queue.join()  # Wait for the transfer to complete
    account_1 = await transaction.bank_account_repository.get_by(
        account_number=1
    )
    account_2 = await transaction.bank_account_repository.get_by(
        account_number=2
    )
    print("Transferência")
    print(f"Saldo da Conta {account_1.account_number}: {account_1.balance}")
    print(f"Saldo da Conta {account_2.account_number}: {account_2.balance}")
    print("----------------$$----------------\n")

    # Concorrência 1
    await asyncio.gather(
        transaction.create_bank_deposit(
            data=TransactionDepositRequest(account_number=1, balance=50)
        ),
        transaction.create_bank_withdraw(
            data=TransactionWithdrawRequest(account_number=1, balance=30)
        ),
    )
    account_1 = await transaction.bank_account_repository.get_by(
        account_number=1
    )
    print("Concorrência 1")
    print(f"Saldo da Conta {account_1.account_number}: {account_1.balance}")
    print("----------------$$----------------\n")

    # Concorrência 2
    await asyncio.gather(
        transaction.create_bank_deposit(
            data=TransactionDepositRequest(account_number=1, balance=100)
        ),
        transfer_queue.put(
            TransactionTransferRequest(
                type=TransactionsTypes.TRANSFER.value,
                from_account=TransactionDepositRequest(
                    account_number=1, balance=50
                ),
                to_account=2,
            )
        ),
    )
    await transfer_queue.join()  # Wait for the transfer to complete
    account_1 = await transaction.bank_account_repository.get_by(
        account_number=1
    )
    account_2 = await transaction.bank_account_repository.get_by(
        account_number=2
    )
    print("Concorrência 2")
    print(f"Saldo da Conta {account_1.account_number}: {account_1.balance}")
    print(f"Saldo da Conta {account_2.account_number}: {account_2.balance}")
    print("----------------$$----------------\n")

    # Concorrência 3
    await asyncio.gather(
        transfer_queue.put(
            TransactionTransferRequest(
                type=TransactionsTypes.TRANSFER.value,
                from_account=TransactionDepositRequest(
                    account_number=1, balance=20
                ),
                to_account=2,
            )
        ),
        transfer_queue.put(
            TransactionTransferRequest(
                type=TransactionsTypes.TRANSFER.value,
                from_account=TransactionDepositRequest(
                    account_number=2, balance=10
                ),
                to_account=3,
            )
        ),
    )
    await transfer_queue.join()
    account_1 = await transaction.bank_account_repository.get_by(
        account_number=1
    )
    account_2 = await transaction.bank_account_repository.get_by(
        account_number=2
    )
    account_3 = await transaction.bank_account_repository.get_by(
        account_number=3
    )
    print("Concorrência 3")
    print(f"Saldo da Conta {account_1.account_number}: {account_1.balance}")
    print(f"Saldo da Conta {account_2.account_number}: {account_2.balance}")
    print(f"Saldo da Conta {account_3.account_number}: {account_3.balance}")
    print("----------------$$----------------")


if __name__ == "__main__":
    asyncio.run(main())
    """
    Ao me referir a concorrência, logo imagino filas de execução assíncronas, sendo elas executadas de forma paralela.
    Neste exemplo, utilizamos `asyncio.gather` para executar as transações, também utilizamos `asyncio.Queue` para criar uma fila
    de execução de transferências, onde cada transferência é executada de forma assíncrona.
    No Python, temos o Celery, que é uma ferramenta de fila de tarefas distribuída, que nos permite executar tarefas assíncronas em segundo plano.
    Mundo afora, temos o RabbitMQ, Apache Kafka, Amazon SQS, Google Cloud Pub/Sub, entre outros. Desses, o que já tive
    a oportunidade de trabalhar foi o Amazon SQS, Pub/Sub e tbm já realizei um exemplo prático de pagamentos utilizando Go + RabbitMQ.

    Agora vamos ao resultado da execução do script:
    -> Comparando este resultado com a tabela verdade do case, percebemos que a maneira que foi desenvolvido
    o script atende as necessidades, pois o saldo das contas está correto e respeitando cada execução. Por mais que
    tenhamos concorrência, as transações são executadas seguindo a ordem de cada requisição.

    Depósito
    Saldo da Conta 1: 100
    ----------------$$----------------

    Saque
    Saldo da Conta 1: 50
    ----------------$$----------------

    Transferência
    Saldo da Conta 1: 20
    Saldo da Conta 2: 30
    ----------------$$----------------

    Concorrência 1
    Saldo da Conta 1: 40
    ----------------$$----------------

    Concorrência 2
    Saldo da Conta 1: 90
    Saldo da Conta 2: 80
    ----------------$$----------------

    Concorrência 3
    Saldo da Conta 1: 70
    Saldo da Conta 2: 90
    Saldo da Conta 3: 10
    ----------------$$----------------
    """
