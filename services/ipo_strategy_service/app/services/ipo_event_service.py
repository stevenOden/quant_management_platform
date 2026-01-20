import datetime

from fastapi import HTTPException
from pydantic.v1.typing import is_union
from sqlmodel import select, Session
from app.models.ipo_event import IPOEvent

def get_symbol(symbol: str, session: Session) -> IPOEvent:
    normalized = symbol.strip().upper()
    result = session.exec(select(IPOEvent).where(IPOEvent.symbol == normalized)).one_or_none()

    if not result:
        raise HTTPException(status_code=404, detail=f"{symbol} not found in IPOEvent Table")

    return result

def get_all_symbols(session: Session) -> list[IPOEvent]:
    return session.exec(select(IPOEvent)).all()

def modify_symbol(symbol: str, fieldname: str, fieldvalue: str, fieldtype: str, session: Session) -> IPOEvent:
    import types
    import typing
    from datetime import datetime, timezone
    normalized = symbol.strip().upper()
    row = session.exec(select(IPOEvent).where(IPOEvent.symbol == normalized)).one_or_none()

    if not row:
        raise HTTPException(status_code=404, detail=f"{symbol} not found in IPOEvent Table")

    if not hasattr(row,fieldname):
        raise HTTPException(status_code=404, detail=f"{fieldname} not found in IPOEvent Fields")

    truefieldtype = row.__fields__[fieldname].annotation
    if isinstance(truefieldtype,types.UnionType):
        truefieldtype = typing.get_args(truefieldtype)[0].__name__
    else:
        truefieldtype = truefieldtype.__name__
    if fieldtype != truefieldtype:
        raise HTTPException(status_code=404, detail=f"Input type: {fieldtype} != {truefieldtype} for {fieldname}")

    if truefieldtype == "float":
        fieldvalue = float(fieldvalue)
    elif truefieldtype == "datetime":
        fieldvalue = datetime.strptime(fieldvalue,"%Y-%m-%d")
        fieldvalue = fieldvalue.replace(tzinfo=timezone.utc)

    row.__setattr__(fieldname,fieldvalue)
    session.add(row)
    session.commit()
    session.refresh(row)

    return row