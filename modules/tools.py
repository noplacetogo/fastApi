import uuid


# dict ->dict
# {"apple":"3" => apple='3'}
def parse_params_to_sql(params: dict) -> str:
    return "&".join([f"{i}='{params[i]}'" for i in params])


# create uuid
def getUUID() -> str:
    temp = str(uuid.uuid4())
    return temp.replace('-', '')