from dependency_injector import providers, containers

from src.application.services.accounts.account_management import AccountManagementService
from src.application.services.accounts.account_profile import AccountProfileService
from src.application.services.additions.addition_profile import AdditionProfileService
from src.application.services.auth.auth import AuthService
from src.application.services.auth.login import LoginService
from src.application.services.auth.password import PasswordService
from src.application.services.auth.payload import PayloadExtractorService
from src.application.services.auth.token import TokenService
from src.application.services.auth.user import AuthUserService
from src.application.services.banks.bank_management import BankManagementService
from src.application.services.banks.bank_public import BankPublicService
from src.application.services.logs.log import LogService
from src.application.services.profile.profile import ProfileService
from src.application.services.registration.registration import UserRegistrationService
from src.application.services.users.user_management import UserManagementService


class Services(containers.DeclarativeContainer):
    config = providers.Configuration()

    repositories = providers.DependenciesContainer()
    core = providers.DependenciesContainer()
    uow = providers.DependenciesContainer()

    log_service = providers.Factory(
        LogService,
        logger=core.logger
    )

    token_service = providers.Factory(
        TokenService,
        token_handler=core.token_handler,
    )

    payload_extractor_service = providers.Factory(
        PayloadExtractorService,
        token_handler=core.token_handler,
    )

    password_service = providers.Factory(
        PasswordService,
        password_handler=core.password_handler,
    )

    auth_service = providers.Factory(
        AuthService,
        token_service=token_service,
        payload_extractor_service=payload_extractor_service,
    )

    user_registration_service = providers.Factory(
        UserRegistrationService,
        repository=repositories.user_repository,
        uow=uow.uow,
        password_handler=core.password_handler
    )

    auth_user_service = providers.Factory(
        AuthUserService,
        repository=repositories.user_repository,
    )

    login_service = providers.Factory(
        LoginService,
        auth_user_service=auth_user_service,
        password_service=password_service,
        token_service=token_service,
    )

    bank_info_service = providers.Factory(
        BankPublicService,
        repository=repositories.bank_repository
    )

    profile_service = providers.Factory(
        ProfileService,
        uow=uow.uow,
        repository=repositories.user_repository
    )

    account_profile_service = providers.Factory(
        AccountProfileService,
        repository=repositories.account_repository,
    )

    addition_profile_service = providers.Factory(
        AdditionProfileService,
        repository=repositories.addition_repository,
        account_repository=repositories.account_repository,
    )

    bank_management_service = providers.Factory(
        BankManagementService,
        repository=repositories.bank_repository,
    )

    user_management_service = providers.Factory(
        UserManagementService,
        repository=repositories.user_repository,
    )

    account_management_service = providers.Factory(
        AccountManagementService,
        repository=repositories.account_repository,
    )
