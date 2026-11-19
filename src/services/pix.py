"""Generates the Pix "copy and paste" code (static BR Code) and its QR Code."""

import unicodedata

import segno


def _sem_acento(texto: str) -> str:
    return unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()


def _campo(id_: str, valor: str) -> str:
    return f"{id_}{len(valor):02d}{valor}"


def _crc16(payload: str) -> str:
    crc = 0xFFFF
    for byte in payload.encode("utf-8"):
        crc ^= byte << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return f"{crc:04X}"


def gerar_pix(chave: str, nome: str, cidade: str, valor: float, txid: str = "***") -> str:
    conta = _campo("00", "BR.GOV.BCB.PIX") + _campo("01", chave)
    payload = (
        _campo("00", "01")
        + _campo("26", conta)
        + _campo("52", "0000")
        + _campo("53", "986")
        + _campo("54", f"{valor:.2f}")
        + _campo("58", "BR")
        + _campo("59", _sem_acento(nome)[:25])
        + _campo("60", _sem_acento(cidade)[:15])
        + _campo("62", _campo("05", txid))
        + "6304"
    )
    return payload + _crc16(payload)


def qr_png(codigo: str) -> bytes:
    """Returns the QR Code as PNG bytes (for use in ft.Image)."""
    import io

    buf = io.BytesIO()
    segno.make(codigo, error="m").save(buf, kind="png", scale=6, border=1)
    return buf.getvalue()
