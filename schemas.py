from pydantic import BaseModel, Field
from typing import Dict

class TrafficLightPhasesRequest(BaseModel):
    phases: Dict[int, float] = Field(
        example={
            0: 35,
            2: 20
        },
        description="Ключ — индекс фазы, значение — новая длительность (сек)"
    )
