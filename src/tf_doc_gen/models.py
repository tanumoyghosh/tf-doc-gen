from dataclasses import dataclass, field
from typing import Any


@dataclass
class Variable:
    name: str
    description: str
    type: str
    default: Any | None = None


@dataclass
class Output:
    name: str
    description: str
    value: Any


@dataclass
class Requirement:
    name: str
    version: str


@dataclass
class Provider:
    name: str
    source: str
    version: str


@dataclass
class Resource:
    type: str
    name: str


@dataclass
class ModuleDocumentation:
    name: str
    requirements: list[Requirement] = field(default_factory=list)
    providers: list[Provider] = field(default_factory=list)
    resources: list[Resource] = field(default_factory=list)
    variables: list[Variable] = field(default_factory=list)
    outputs: list[Output] = field(default_factory=list)
