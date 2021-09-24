from . import Route


class Platform:
    class Core:
        QueryNode = Route("", "GET", False)

    class OnBoarding:
        CheckOnBoardingStatus = Route("onboard/hello", "GET", True, False, False)
        CompleteOnBoarding = Route("onboard/complete", "POST", True, False)


class Auth:
    class Account:
        FetchAccount = Route(url="auth/account", method="GET", with_auth=True, can_be_bot=False, with_ulid=False)
        CreateAccount = Route(url="auth/account/create", method="POST", with_auth=False, can_be_bot=False)
        ResendVerification = Route(url="auth/account/reverify", method="POST", with_auth=False, can_be_bot=False)
        VerifyEmail = Route(url="auth/account/verify/:code", method="POST", with_auth=False, can_be_bot=False)
        SendPasswordReset = Route(url="auth/account/reset_password", method="POST", with_auth=False, can_be_bot=False)
        PasswordReset = Route(url="auth/account/reset_password", method="PATCH", with_auth=False, can_be_bot=False)
        ChangePassword = Route(url="auth/account/change/password", method="PATCH", with_auth=True, can_be_bot=False)
        ChangeEmail = Route(url="auth/account/change/email", method="PATCH", with_auth=True, can_be_bot=False)

    class Session:
        Login = Route(url="https://api.revolt.chat/auth/session/login", method="POST", with_auth=False, can_be_bot=False)


class User:
    class UserInformation:
        pass

    class DirectMessaging:
        pass

    class Relationships:
        pass


class Bot:
    pass


class Channel:
    class ChannelInformation:
        pass

    class ChannelInvites:
        pass

    class ChannelPermissions:
        pass

    class Messaging:
        pass

    class Groups:
        pass

    class Voice:
        pass


class Server:
    class ServerInformation:
        pass

    class ServerMembers:
        pass

    class ServerPermissions:
        pass


class Miscellaneous:
    class Invites:
        pass

    class Sync:
        pass

    class WebPush:
        pass


__all__ = [
    "Platform",
    "Auth",
    "User",
    "Bot",
    "Channel",
    "Server",
    "Miscellaneous"
]
