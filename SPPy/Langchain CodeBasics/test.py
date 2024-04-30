from langchain.chains.openai_functions.base import convert_to_openai_function
from pydantic.v1 import BaseModel as BaseModelV1, Field as FieldV1
from pydantic import BaseModel as BaseModelV2, Field as FieldV2
import json

class FuncV1(BaseModelV1):
  "Pydantic v1 model."
  output: str = FieldV1(description="A output text")


class FuncV2(BaseModelV2):
  "Pydantic v2 model."
  output: str = FieldV2(description="A output text")

print(convert_to_openai_function(FuncV1))

print(convert_to_openai_function(FuncV2))
