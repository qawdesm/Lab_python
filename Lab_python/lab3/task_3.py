import json
from datetime import datetime

class Client:
    def __init__(self, client_id, name, phone, email):
        self.client_id = client_id
        self.name = name
        self.phone = phone
        self.email = email
        self.accounts = {}

    def add_account(self, account):
        if account.currency in self.accounts:
            raise ValueError(f"Счет в валюте {account.currency} уже существует")
        self.accounts[account.currency] = account

    def remove_account(self, currency):
        if currency in self.accounts:
            del self.accounts[currency]

    def get_account(self, currency):
        return self.accounts.get(currency)

    def get_total_balance(self):
        return sum(account.balance for account in self.accounts.values())

    def to_dict(self):
        return {
            'client_id': self.client_id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'accounts': {currency: account.to_dict() for currency, account in self.accounts.items()}
        }


class BankAccount:
    def __init__(self, account_number, currency, client_id, initial_balance=0):
        self.account_number = account_number
        self.currency = currency
        self.client_id = client_id
        self.balance = initial_balance
        self.created_date = datetime.now()
        self.transactions = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")
        self.balance += amount
        self.transactions.append({
            'type': 'deposit',
            'amount': amount,
            'date': datetime.now(),
            'balance_after': self.balance
        })

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")
        if amount > self.balance:
            raise ValueError("Недостаточно средств на счете")
        self.balance -= amount
        self.transactions.append({
            'type': 'withdraw',
            'amount': amount,
            'date': datetime.now(),
            'balance_after': self.balance
        })

    def transfer(self, amount, target_account):
        if amount <= 0:
            raise ValueError("Сумма перевода должна быть положительной")
        if amount > self.balance:
            raise ValueError("Недостаточно средств для перевода")
        
        self.withdraw(amount)
        target_account.deposit(amount)
        
        self.transactions.append({
            'type': 'transfer_out',
            'amount': amount,
            'target_account': target_account.account_number,
            'date': datetime.now(),
            'balance_after': self.balance
        })
        target_account.transactions.append({
            'type': 'transfer_in',
            'amount': amount,
            'source_account': self.account_number,
            'date': datetime.now(),
            'balance_after': target_account.balance
        })

    def to_dict(self):
        return {
            'account_number': self.account_number,
            'currency': self.currency,
            'client_id': self.client_id,
            'balance': self.balance,
            'created_date': self.created_date.isoformat()
        }


class Bank:
    def __init__(self, name):
        self.name = name
        self.clients = {}  
        self.accounts = {}
        self.next_account_number = 1

    def generate_account_number(self):
        account_number = f"ACC{self.next_account_number:06d}"
        self.next_account_number += 1
        return account_number

    def add_client(self, client):
        if client.client_id in self.clients:
            raise ValueError("Клиент с таким ID уже существует")
        self.clients[client.client_id] = client

    def open_account(self, client_id, currency, initial_balance=0):
        if client_id not in self.clients:
            raise ValueError("Клиент не найден")
        
        client = self.clients[client_id]
        if currency in client.accounts:
            raise ValueError(f"У клиента уже есть счет в валюте {currency}")
        
        account_number = self.generate_account_number()
        account = BankAccount(account_number, currency, client_id, initial_balance)
        
        client.add_account(account)
        self.accounts[account_number] = account
        
        return account

    def close_account(self, client_id, currency):
        if client_id not in self.clients:
            raise ValueError("Клиент не найден")
        
        client = self.clients[client_id]
        account = client.get_account(currency)
        
        if not account:
            raise ValueError(f"Счет в валюте {currency} не найден")
        
        if account.balance > 0:
            raise ValueError("Нельзя закрыть счет с положительным балансом")
        
        del self.accounts[account.account_number]
        client.remove_account(currency)

    def get_client_accounts(self, client_id):
        if client_id not in self.clients:
            raise ValueError("Клиент не найден")
        return self.clients[client_id].accounts

    def get_account(self, account_number):
        return self.accounts.get(account_number)

    def validate_client_access(self, client_id, account_number):
        account = self.get_account(account_number)
        if not account:
            raise ValueError("Счет не найден")
        if account.client_id != client_id:
            raise ValueError("Доступ к счету запрещен")
        return account


class BankSystem:
    def __init__(self):
        self.bank = Bank("MyBank")
        self.current_client = None
        self.setup_sample_data()

    def setup_sample_data(self):
        clients_data = [
            ("001", "Иван Козлов", "+375296547892", "ivan@mail.ru"),
            ("002", "Мария Григоренко", "+375291963348", "maria@mail.ru"),
            ("003", "Алексей Сидоров", "+375445652323", "alex@mail.ru")
        ]
        
        for client_id, name, phone, email in clients_data:
            client = Client(client_id, name, phone, email)
            self.bank.add_client(client)
            
            self.bank.open_account(client_id, "RUB", 1000)
            self.bank.open_account(client_id, "USD", 100)

    def show_menu(self):
        print("БАНКОВСКАЯ СИСТЕМА")
        if self.current_client:
            client = self.bank.clients[self.current_client]
            print(f"Клиент: {client.name} (ID: {client.client_id})")
        
        print("0. Выход из программы")
        print("1. Войти в систему")
        print("2. Открыть счет")
        print("3. Закрыть счет")
        print("4. Пополнить счет")
        print("5. Снять со счета")
        print("6. Перевести деньги")
        print("7. Показать мои счета")
        print("8. Выписка по счетам (сохранить в файл)")
        print("9. Выйти из системы")

    def login(self):
        client_id = input("Введите ваш ID клиента: ").strip()
        if client_id in self.bank.clients:
            self.current_client = client_id
            print(f"Успешный вход! Добро пожаловать, {self.bank.clients[client_id].name}!")
        else:
            print("Ошибка: Клиент с таким ID не найден")

    def logout(self):
        if self.current_client:
            print(f"До свидания, {self.bank.clients[self.current_client].name}!")
            self.current_client = None
        else:
            print("Вы не вошли в систему")

    def open_account(self):
        if not self.current_client:
            print("Ошибка: Сначала войдите в систему")
            return
        
        currency = input("Введите валюту счета (RUB, USD, EUR): ").strip().upper()
        initial_balance = float(input("Введите начальный баланс: "))
        
        try:
            account = self.bank.open_account(self.current_client, currency, initial_balance)
            print(f"Счет успешно открыт! Номер счета: {account.account_number}")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def close_account(self):
        if not self.current_client:
            print("Ошибка: Сначала войдите в систему")
            return
        
        currency = input("Введите валюту счета для закрытия: ").strip().upper()
        
        try:
            self.bank.close_account(self.current_client, currency)
            print(f"Счет в валюте {currency} успешно закрыт")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def deposit(self):
        if not self.current_client:
            print("Ошибка: Сначала войдите в систему")
            return
        
        currency = input("Введите валюту счета: ").strip().upper()
        amount = float(input("Введите сумму для пополнения: "))
        
        try:
            account = self.bank.validate_client_access(self.current_client, self.bank.clients[self.current_client].get_account(currency).account_number)
            account.deposit(amount)
            print(f"Счет успешно пополнен на {amount} {currency}")
            print(f"Текущий баланс: {account.balance} {currency}")
        except (ValueError, AttributeError) as e:
            print(f"Ошибка: {e}")

    def withdraw(self):
        if not self.current_client:
            print("Ошибка: Сначала войдите в систему")
            return
        
        currency = input("Введите валюту счета: ").strip().upper()
        amount = float(input("Введите сумму для снятия: "))
        
        try:
            account = self.bank.validate_client_access(self.current_client, self.bank.clients[self.current_client].get_account(currency).account_number)
            account.withdraw(amount)
            print(f"Со счета снято {amount} {currency}")
            print(f"Текущий баланс: {account.balance} {currency}")
        except (ValueError, AttributeError) as e:
            print(f"Ошибка: {e}")

    def transfer(self):
        if not self.current_client:
            print("Ошибка: Сначала войдите в систему")
            return
        
        from_currency = input("Введите валюту вашего счета: ").strip().upper()
        target_account_number = input("Введите номер счета получателя: ").strip()
        amount = float(input("Введите сумму для перевода: "))
        
        try:
            from_account = self.bank.validate_client_access(self.current_client, self.bank.clients[self.current_client].get_account(from_currency).account_number)
            target_account = self.bank.get_account(target_account_number)
            
            if not target_account:
                raise ValueError("Счет получателя не найден")
            
            from_account.transfer(amount, target_account)
            print(f"Успешно переведено {amount} {from_currency} на счет {target_account_number}")
            print(f"Текущий баланс: {from_account.balance} {from_currency}")
            
        except (ValueError, AttributeError) as e:
            print(f"Ошибка: {e}")

    def show_accounts(self):
        if not self.current_client:
            print("Ошибка: Сначала войдите в систему")
            return
        
        client = self.bank.clients[self.current_client]
        accounts = client.accounts
        
        print("ВАШИ СЧЕТА")
        
        if not accounts:
            print("У вас нет открытых счетов")
            return
        
        for currency, account in accounts.items():
            print(f"Валюта: {currency}")
            print(f"  Номер счета: {account.account_number}")
            print(f"  Баланс: {account.balance} {currency}")
            print(f"  Дата открытия: {account.created_date.strftime('%d.%m.%Y %H:%M')}")
        
        total_balance = client.get_total_balance()
        print(f"ОБЩИЙ БАЛАНС: {total_balance} RUB ")

    def generate_statement(self):
        if not self.current_client:
            print("Ошибка: Сначала войдите в систему")
            return
        
        client = self.bank.clients[self.current_client]
        filename = f"bank{client.client_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write("              ВЫПИСКА ПО СЧЕТАМ\n")
                file.write(f"Клиент: {client.name}\n")
                file.write(f"ID клиента: {client.client_id}\n")
                file.write(f"Дата формирования: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
                
                if not client.accounts:
                    file.write("Нет открытых счетов\n")
                else:
                    for currency, account in client.accounts.items():
                        file.write(f"Счет в валюте: {currency}\n")
                        file.write(f"  Номер счета: {account.account_number}\n")
                        file.write(f"  Баланс: {account.balance:.2f} {currency}\n")
                        file.write(f"  Дата открытия: {account.created_date.strftime('%d.%m.%Y')}\n")
                    
                    total_balance = client.get_total_balance()
                    file.write(f"\nОБЩИЙ БАЛАНС: {total_balance:.2f} RUB\n")
                
                file.write("Конец выписки\n")
            
            print(f"Выписка сохранена в файл: {filename}")
            
        except Exception as e:
            print(f"Ошибка при сохранении выписки: {e}")

    def run(self):
        print("Добро пожаловать в банковскую систему!")
        
        while True:
            self.show_menu()
            choice = input("Выберите действие: ").strip()
            
            try:
                if choice == "1":
                    self.login()
                elif choice == "2":
                    self.open_account()
                elif choice == "3":
                    self.close_account()
                elif choice == "4":
                    self.deposit()
                elif choice == "5":
                    self.withdraw()
                elif choice == "6":
                    self.transfer()
                elif choice == "7":
                    self.show_accounts()
                elif choice == "8":
                    self.generate_statement()
                elif choice == "9":
                    self.logout()
                elif choice == "0":
                    print("Спасибо за использование банковской системы! До свидания!")
                    break
                else:
                    print("Неверный выбор. Попробуйте снова.")
            
            except Exception as e:
                print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    system = BankSystem()
    system.run()