from datetime import date, timedelta
import datetime
print(type(date(2025, 5, 5)))
print(datetime.date.today())

today = datetime.datetime.now()
print(today)
# Calculate yesterday's date
yesterday = today - timedelta(days=1)
print(type(date.today() - timedelta(days=1)))
# Print yesterday's date
print(yesterday.date())

# Optionally, format the date as a string
yesterday_str = yesterday.strftime("%Y-%m-%d")
print(yesterday_str)


print(len("10626900-f7cd-4a18-b293-1ddebbe1fb6c"))
