#класс программист фамилия стаж работы язык прлграммирования
# метод делать таски получать зарплату тратить зарплату
# при попытке потратить больше программа не должна прерываться добавить программиста поменять зарплату вывожу

class ErrorProgramist(Exception):
    pass

class ErrorExperience(ErrorProgramist):
    pass

class ErrorSalary(ErrorProgramist): 
    pass  

class Programist:
    def __init__(self, firstname: str, experience: int, salary: int, language: str):
        if experience < 0:
            raise ErrorExperience("стаж не может быть отрицательным")
        if salary < 0:
            raise ErrorSalary("зарплата не может быть отрицательной")
         
        self.firstname = firstname 
        self.experience = experience
        self.salary = salary
        self.language = language

    def __str__(self):
        return f"Фамилия - {self.firstname}, стаж работы - {self.experience}, зарплата - {self.salary}, язык программирования - {self.language}"

    def do_tasks(self, task_count: int = 1):
        earnings = task_count * 9999
        self.salary += earnings
        print(f"Программист {self.firstname} пишет на {self.language} языке программирования")
        print(f"Программист получает за выполнение задания {earnings}")
        print(f"Общая зарплата: {self.salary}")

    def get_salary(self):
        if self.salary == 0:
            print("зарплата пока равна 0")
        elif self.salary > 0:
            print(f"зарплата = {self.salary}")
        else:
            raise ErrorSalary("Некорректная зарплата")
        
    def spend_salary(self, amount: int):
        try:
            if amount < 0:
                print("сумма трат не может быть отрицательной")
                return False
            elif amount > self.salary:
                print(f"Недостаточно средств! Текущая зарплата: {self.salary}, попытка потратить: {amount}")
                return False
            else:
                self.salary -= amount
                print(f"Программист {self.firstname} потратил {amount}")
                print(f"Остаток зарплата: {self.salary}")
                return True
        except Exception as e:
            print(f"Ошибка при трате зарплаты: {e}")
            return False

    def work(self, months: int = 1, count: int = 1):
        for month in range(1, months + 1):
            print(f"Месяц {month}")
            self.do_tasks(count)

def add_programmer(programmers):
    try:
        firstname = input("Введите фамилию: ")
        experience = int(input("Введите стаж работы: "))
        salary = int(input("Введите зарплату: "))
        language = input("Введите язык программирования: ")
        
        new_programmer = Programist(firstname, experience, salary, language)
        programmers.append(new_programmer)
        print(f"Программист {firstname} успешно добавлен!")
        return True
    except ValueError:
        print("Ошибка: введите корректные числовые значения")
        return False
    except ErrorProgramist as e:
        print(f"Ошибка: {e}")
        return False

def change_salary(programmers):
    if not programmers:
        print("Список программистов пуст!")
        return False
        
    firstname = input("Введите фамилию программиста: ")
    
    for programmer in programmers:
        if programmer.firstname == firstname:
            try:
                new_salary = int(input("Введите новую зарплату: "))
                if new_salary < 0:
                    print("Зарплата не может быть отрицательной!")
                    return False
                programmer.salary = new_salary
                print(f"Зарплата программиста {firstname} изменена на {new_salary}")
                return True
            except ValueError:
                print("Ошибка: введите корректное число")
                return False
    
    print(f"Программист c фамилией {firstname} не найден")

    return False

def show_all_programmers(programmers):
    if not programmers:
        print("Список программистов пуст!")
        return
        
    for i, programmer in enumerate(programmers, 1):
        print(f"{i}. {programmer}")

def select_programmer(programmers):
    if not programmers:
        print("Список программистов пуст!")
        return None
        
    show_all_programmers(programmers)
    
    try:
        choice = int(input("Выберите номер программиста: ")) - 1
        if 0 <= choice < len(programmers):
            return programmers[choice]
        else:
            print("Неверный номер!")
            return None
    except ValueError:
        print("Ошибка: введите число!")
        return None

def main():
    try:
        programmer1 = Programist("Иванов", 3, 59999, "Python")
        programmer2 = Programist("Григоренко", 1, 3852, "Java")
        programmer3 = Programist("Сидоров", 5, 7866446, "C++")
        programmers = [programmer1, programmer2, programmer3]
    except ErrorProgramist as e:
        print(f"Ошибка создания программиста: {e}")
        programmers = []

    current_programmer = None

    while True:
        print("МЕНЮ УПРАВЛЕНИЯ ПРОГРАММИСТАМИ")
        print("1. Выбрать программиста")
        print("2. Выполнить задания")
        print("3. Показать зарплату")
        print("4. Потратить зарплату")
        print("5. Работать несколько месяцев")
        print("6. Добавить программиста")
        print("7. Изменить зарплату")
        print("8. Показать всех программистов")
        print("9. Выход")
        
        if current_programmer:
            print(f"Текущий программист: {current_programmer.firstname}")
        else:
            print("Текущий программист: не выбран")

        choice = input("Сделайте выбор (1-9): ")

        try:
            if choice == "1":
                selected = select_programmer(programmers)
                if selected:
                    current_programmer = selected
                    print(f"Выбран программист: {current_programmer.firstname}")

            elif choice == "2":
                if not current_programmer:
                    print("Сначала выберите программиста!")
                    continue
                    
                try:
                    count = int(input("Введите количество заданий: "))
                    current_programmer.do_tasks(count)
                except ValueError:
                    print("Ошибка: введите число!")

            elif choice == "3":
                if not current_programmer:
                    print("Сначала выберите программиста!")
                    continue
                current_programmer.get_salary()

            elif choice == "4":
                if not current_programmer:
                    print("Сначала выберите программиста!")
                    continue
                    
                try:
                    cost = int(input("Введите сумму для траты: "))
                    current_programmer.spend_salary(cost)
                except ValueError:
                    print("Ошибка: введите число!")

            elif choice == "5":
                if not current_programmer:
                    print("Сначала выберите программиста!")
                    continue
                    
                try:
                    months = int(input("Введите количество месяцев: "))
                    count = int(input("Введите количество заданий в месяц: "))
                    current_programmer.work(months, count)
                except ValueError:
                    print("Ошибка: введите числа!")

            elif choice == "6":
                if add_programmer(programmers):
                    print("Программист успешно добавлен!")

            elif choice == "7":
                change_salary(programmers)

            elif choice == "8":
                show_all_programmers(programmers)

            elif choice == "9":
                break

            else:
                print("Неверный выбор! Введите число от 1 до 9")

        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()