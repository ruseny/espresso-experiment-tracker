from enum import Enum

class YesNo(str, Enum):
    yes = "yes"
    no = "no"

class UserTypes(str, Enum):
    home_barista = "home barista"
    professional_barista = "professional barista"
    developer = "developer"

class PidTypes(str, Enum):
    automatic = "automatic"
    programmable = "programmable"
    unknown = ""

class OperationTypes(str, Enum):
    manual = "manual"
    electric = "electric"

class BasketSizes(str, Enum):
    single = "single"
    double = "double"
    triple = "triple"
    quadruple = "quadruple"

class SpoutTypes(str, Enum):
    single = "single"
    double = "double"
    bottomless = "bottomless"

class OriginTypes(str, Enum):
    single_origin = "single origin"
    blend = "blend"

class EqpTypes(str, Enum):
    coffee_machine = "coffee machine"
    grinder = "grinder"
    portafilter = "portafilter"