base_price = 24.99
base_minutes = 60
base_sms = 30
base_internet = 1024

price_minute = 0.89
price_sms = 0.59
price_mb = 0.79
tax_rate = 0.02 

minutes = int(input("Сколько минут использовали: "))
sms = int(input("Сколько SMS отправили: "))
internet = int(input("Сколько интернета использовали (МБ): "))


dop_minutes = minutes - base_minutes
if dop_minutes < 0:
    dop_minutes = 0

dop_sms = sms - base_sms
if dop_sms < 0:
    dop_sms = 0

dop_internet = internet - base_internet
if dop_internet < 0:
    dop_internet = 0

cost_dop_minutes = dop_minutes * price_minute
cost_dop_sms = dop_sms * price_sms
cost_dop_internet = dop_internet * price_mb


total_before_tax = base_price + cost_dop_minutes + cost_dop_sms + cost_dop_internet
tax_amount = total_before_tax * tax_rate

final_total = total_before_tax + tax_amount

print(f"Базовая цена: {base_price:.2f} rub.")

if dop_minutes > 0:
    print(f"Доп. минуты: {cost_dop_minutes:.2f} rub.")

if dop_sms > 0:
    print(f"Доп SMS: {cost_dop_sms:.2f} rub.")

if dop_internet > 0:
    print(f"Доп минуты: {cost_dop_internet:.2f} rub.")

print(f"Сумма до налога: {total_before_tax:.2f} rub.")
print(f"Налог(2%): {tax_amount:.2f} rub.")
print(f"Итоговая сумма: {final_total:.2f} rub.")