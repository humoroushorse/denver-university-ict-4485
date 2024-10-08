from ict_4485_week_10.models import core_models


class SessionEntity(core_models.BaseModelWithId):
    user_id: str
    jwt: str

class SessionReadModel(SessionEntity):
    pass