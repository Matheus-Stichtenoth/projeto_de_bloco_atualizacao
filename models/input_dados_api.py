from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Literal

# Lista de estados e DDDs válidos
ESTADOS_VALIDOS = [
    "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS",
    "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC",
    "SE", "SP", "TO"
]

DDD_VALIDOS = [
    "11", "12", "13", "14", "15", "16", "17", "18", "19", "21", "22", "24",
    "27", "28", "31", "32", "33", "34", "35", "37", "38", "41", "42", "43",
    "44", "45", "46", "47", "48", "49", "51", "53", "54", "55", "61", "62",
    "63", "64", "65", "66", "67", "68", "69", "71", "73", "74", "75", "77",
    "79", "81", "82", "83", "84", "85", "86", "87", "88", "89", "91", "92",
    "93", "94", "95", "96", "97", "98", "99"
]

class InputDadosAPI(BaseModel):
    DATA_BASE: str = Field(..., description="Data de referência (formato: AAAAMM, ex.: 202409).")
    CLIENTE: Literal["PF", "PJ"] = Field(..., description="Tipo de cliente: PF (Pessoa Física) ou PJ (Pessoa Jurídica).")
    ESTADO: str = Field(..., description="Estado no formato UF (ex.: RS).")
    SUB_REGIAO: str = Field(..., description="Sub-região no formato DDD (ex.: 54).")
    MODALIDADE: str = Field(..., description="Modalidade de crédito (ex.: Habitacional).")
    CARTEIRA: float = Field(..., description="Montante total da carteira no formato americano (ex.: 123456.78).")
    VENCIDO_ACIMA_DE_15_DIAS: float = Field(..., description="Montante vencido acima de 15 dias no formato americano.")

    @field_validator("DATA_BASE")
    def validar_data_base(cls, value):
        if not value.isdigit():
            raise ValueError("DATA_BASE deve conter apenas números.")
        if len(value) != 6:
            raise ValueError("DATA_BASE deve ter exatamente 6 dígitos (formato: AAAAMM).")
        return value

    @field_validator("ESTADO")
    def validar_estado(cls, value):
        if value not in ESTADOS_VALIDOS:
            raise ValueError(f"ESTADO deve ser um UF válido ({', '.join(ESTADOS_VALIDOS)}).")
        return value

    @field_validator("SUB_REGIAO")
    def validar_sub_regiao(cls, value):
        if value not in DDD_VALIDOS:
            raise ValueError(f"SUB_REGIAO deve ser um DDD válido ({', '.join(DDD_VALIDOS)}).")
        return value