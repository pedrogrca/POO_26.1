"""Utilitários de entrada e saída no terminal, compartilhados pelas telas."""
from datetime import date, datetime


class TelaBase:
    """Superclasse das telas: centraliza leitura e formatação da interface.

    Todas as telas do sistema herdam destes utilitários, garantindo uma
    apresentação uniforme e a validação básica das entradas do usuário.
    """

    LARGURA = 60

    # ------------------------------- saída ------------------------------ #
    @classmethod
    def titulo(cls, texto: str) -> None:
        print("\n" + "=" * cls.LARGURA)
        print(f" {texto}")
        print("=" * cls.LARGURA)

    @staticmethod
    def subtitulo(texto: str) -> None:
        print(f"\n--- {texto} ---")

    @staticmethod
    def mensagem(texto: str) -> None:
        print(f">> {texto}")

    @staticmethod
    def erro(texto: str) -> None:
        print(f"[!] {texto}")

    @staticmethod
    def pausar() -> None:
        input("\nPressione Enter para continuar...")

    # ------------------------------ entrada ----------------------------- #
    @staticmethod
    def ler(rotulo: str, obrigatorio: bool = False) -> str:
        while True:
            valor = input(f"{rotulo}: ").strip()
            if valor or not obrigatorio:
                return valor
            print("   Campo obrigatório, tente novamente.")

    @staticmethod
    def ler_int(rotulo: str, permitir_vazio: bool = False, padrao: int | None = None) -> int | None:
        while True:
            valor = input(f"{rotulo}: ").strip()
            if not valor and permitir_vazio:
                return padrao
            try:
                return int(valor)
            except ValueError:
                print("   Informe um número inteiro válido.")

    @staticmethod
    def ler_float(rotulo: str, permitir_vazio: bool = False, padrao: float | None = None) -> float | None:
        while True:
            valor = input(f"{rotulo}: ").strip().replace(",", ".")
            if not valor and permitir_vazio:
                return padrao
            try:
                return float(valor)
            except ValueError:
                print("   Informe um número válido (ex.: 80.00).")

    @staticmethod
    def ler_data_hora(rotulo: str, padrao: datetime | None = None) -> datetime | None:
        """Lê uma data/hora no formato dd/mm/aaaa hh:mm (Enter mantém o padrão)."""
        while True:
            valor = input(f"{rotulo} (dd/mm/aaaa hh:mm): ").strip()
            if not valor:
                return padrao
            try:
                return datetime.strptime(valor, "%d/%m/%Y %H:%M")
            except ValueError:
                print("   Data/hora inválida. Use o formato dd/mm/aaaa hh:mm.")

    @staticmethod
    def ler_data(rotulo: str, padrao: date | None = None) -> date | None:
        """Lê uma data no formato dd/mm/aaaa (Enter mantém o padrão)."""
        while True:
            valor = input(f"{rotulo} (dd/mm/aaaa, Enter p/ nenhuma): ").strip()
            if not valor:
                return padrao
            try:
                return datetime.strptime(valor, "%d/%m/%Y").date()
            except ValueError:
                print("   Data inválida. Use o formato dd/mm/aaaa.")

    @staticmethod
    def confirmar(rotulo: str) -> bool:
        return input(f"{rotulo} (s/N): ").strip().lower() == "s"
