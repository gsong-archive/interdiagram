# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from .node import Action, Part  # noqa: F401


NodeAttr = TypeVar('NodeAttr', 'Action', 'Part')
