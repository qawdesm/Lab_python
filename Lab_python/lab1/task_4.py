sum =int(input("введите сумму денег которую нужно разменять:"))

k_100 = sum // 100
ostatok = sum % 100

k_50 = ostatok // 50
ostatok = ostatok % 50

k_10 = ostatok // 10
ostatok = ostatok % 10

k_5 = ostatok // 5
ostatok = ostatok % 5

m_2 = ostatok // 2
m_1 = ostatok % 2

print(f"\nДля суммы {sum} рублей потребуется:")
print(f"Купюр по 100 рублей: {k_100}")
print(f"Купюр по 50 рублей: {k_50}")
print(f"Купюр по 10 рублей: {k_10}")
print(f"Купюр по 5 рублей: {k_5}")
print(f"Монет по 2 рубля: {m_2}")
print(f"Монет по 1 рублю: {m_1}")
