from db import execute_query
from metadata import build_schema_document

result = execute_query("SELECT version();")

print(result)
print(build_schema_document())
