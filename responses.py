class Responses():
    LOG_EXIST_USER = {"code":200,"success": True}
    LOG_USER_INVAL_CREDS = {"code":401, "message":"email or password are incorrect", "success": False}
    REG_UNIQUE_USER = {"code":200,"success": True}
    REG_DUPLICATE_USER = {"code":403, "message":"User already exists", "success": False}
    REG_USER_MISSING_FIELD = {"code":403, "message":"Email, password and name are required fields", "success": False}
    CRE_ORDR_INGR_AUTH = {"code":200,"success": True}
    CRE_ORDR_NONEINGR_AUTH = {"code":400,"message":"Ingredient ids must be provided","success": False}
    CRE_ORDR_UNAUTH = {"code":401, "message":"You should be authorised", "success": False}
    CRE_ORDR_WRONGINGR_AUTH = {"code":500}