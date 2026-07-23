from pydantic import BaseMode, Field

class Solution(BaseModel):
    steps: list[str] = Field(min_length=1)
    answer: str
    
import re, json

match = re.search(r'\{.*\}', text, re.DOTALL)
data = json.loads(match.group(0))

