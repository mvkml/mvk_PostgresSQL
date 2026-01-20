from fastapi import Depends
from app.common.modules.users.user_validation_utility import UserValidationUtility
from app.common.validation.ai_message_validation import AIMessageValidation
from app.common.validation.api_validation import APIValidation, IAPIValidation

def get_user_validation_utility():
    return UserValidationUtility()

def di_get_ai_message_validation():
    return AIMessageValidation()

def di_get_api_validation()->IAPIValidation:
    return APIValidation()
