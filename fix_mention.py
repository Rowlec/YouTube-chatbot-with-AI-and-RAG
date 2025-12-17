import re

# Read file
with open('app/commands.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace @{author.name} with {author.name}
content = content.replace('f"@{author.name}', 'f"{author.name}')
content = content.replace("f'@{author.name}", "f'{author.name}")

# Write back
with open('app/commands.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Replaced all @{author.name} with {author.name}")
