from   fastapi import Depends
from app.dependencies.di_utilities import di_get_ai_message_validation, di_get_api_validation, get_user_validation_utility
from app.services.conv.ai_message_service import AIMessageService
from app.services.prompt_service import PromptService
from app.services.user_service import UserService
from app.dependencies.di_dal_repositories import di_get_prompt_repository,di_get_ai_message_repo, get_user_repository


def get_user_service(user_repository = Depends(get_user_repository),
                     user_validation_utility = Depends(get_user_validation_utility)):
    return UserService(user_repository, user_validation_utility)


def di_get_ai_message_service(repo=Depends(di_get_ai_message_repo),
                     validation_utility = Depends(di_get_ai_message_validation)):
    return AIMessageService(repo, validation_utility)



def di_get_prompt_service(repo=Depends(di_get_prompt_repository),
                          ai_msg_service = Depends(di_get_ai_message_service),
                     validation_utility = Depends(di_get_api_validation)):
    return PromptService(repo, ai_msg_service, validation_utility)
 