from fastapi import APIRouter, BackgroundTasks, Request, Depends
from modules.EMAIL import EMAIL
from modules.TOOLS import payload_
router = APIRouter()


@router.post("/{receiver}", tags=['EMAIL'], summary="EMAIL測試")
async def send_email(receiver: str, background_tasks: BackgroundTasks,
                     payload: dict = Depends(payload_)):
    background_tasks.add_task(EMAIL.send, receiver, subject=payload['subject'], detail=payload['detail'])
    return '1|OK'

