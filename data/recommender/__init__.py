"""Person A recommender package.

Exports the real engine as `recommend`. Stub and debug helpers available.
"""

from .engine import recommend, recommend_with_debug
from .stub import stub_recommend

__all__ = ["recommend", "recommend_with_debug", "stub_recommend"]
