from fastapi import APIRouter, BackgroundTasks, Request, Depends
from modules.SMS import SMS
from modules.TOOLS import payload_
router = APIRouter()


@router.post("/{receiver}", tags=['SMS'], summary='SMS測試')
async def send_email(receiver: str, background_tasks: BackgroundTasks, payload: dict = Depends(payload_)):
    background_tasks.add_task(SMS.send, receiver, detail=payload['detail'])
    return '1|OK'

