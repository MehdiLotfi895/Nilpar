import json
import re

with open("data.json", "r", encoding="utf-8") as f:
    data = f.read()

# سال‌های خراب مثل 784- را تبدیل می‌کند
data = re.sub(
    r'"(\d{3})-(\d{2})-(\d{2})"',
    lambda m: '"1404-'+m.group(2)+'-'+m.group(3)+'"',
    data
)

with open("data_fixed.json", "w", encoding="utf-8") as f:
    f.write(data)

print("done")