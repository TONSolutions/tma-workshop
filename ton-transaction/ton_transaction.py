from typing import Tuple
from pytoniq_core.tlb.transaction import MessageAny
from pytoniq_core import Cell
from pytoniq_core.boc.cell import CellError
from tonsdk.utils import b64str_to_bytes


def get_body_hash_from_boc(boc: str) -> MessageAny:
    """
    Get body hash from boc

    Args:
        boc: base64 string

    Returns:
        str: body hash
    """
    try:
        cell = Cell.one_from_boc(b64str_to_bytes(boc))
        parsed_message = MessageAny.deserialize(
            cell.begin_parse().refs[0].begin_parse()
        )
    except (CellError, IndexError) as e:
        raise ValueError("boc is invalid") from e

    return parsed_message


def find_transaction_by_meessage(
    address: str, message: MessageAny
) -> Tuple[str, str, str, int]:
    """
    Find transaction by body hash

    Args:
        address: address
        message: message

    Returns:
        Transaction: transaction
    """
    # Getting account lite by address and getting last block
    # Getting transactions by address and last block
    transactions = []
    # Iterating over transactions
    for transaction in transactions:
        in_message_raw_body = "te6ccgEBB..."  # fetch from transaction
        transaction_body = Cell.one_from_boc(b64str_to_bytes(in_message_raw_body))

        if transaction_body.hash != message.body.hash:
            continue

        address = transaction.get("address")
        tx_hash = transaction.get("hash")

        value = int(message.info.value.grams)
        dest = message.info.dest
        bounced = message.info.bounced
        if bounced:
            continue

        return (
            tx_hash,
            address,
            dest,
            value,
        )
