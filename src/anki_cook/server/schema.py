from typing import Annotated, Optional

import pydantic
from annotated_types import Ge, Le, Len


class GenerateWordListSchema(pydantic.BaseModel, frozen=True):
    topic: Annotated[str, Len(3, 100)]
    native: Annotated[str, Len(3, 50)]
    target: Annotated[str, Len(3, 50)]
    extra: Optional[str]
    count: Annotated[int, Ge(5), Le(100)]


class GenerateDeckSchema(GenerateWordListSchema, frozen=True):
    target_tts: bool
    native_tts: bool
    boost_extra: bool
