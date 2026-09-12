from metadata import get_tables, get_columns

print("TABLES")

for table in get_tables():
    print(table)

print("\nCOLUMNS")

for column in get_columns():
    print(column)