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
        Login = Route(url="auth/session/login", method="POST", with_auth=False, can_be_bot=False)
        Logout = Route(url="auth/session/logout", method="POST", with_auth=False, can_be_bot=False)
        EditSession = Route(url="auth/session/:session", method="PATCH", with_auth=True, can_be_bot=False)
        DeleteSession = Route(url="auth/session/:session", method="DELETE", with_auth=True, can_be_bot=False)
        FetchSessions = Route(url="auth/session/all", method="GET", with_auth=True, can_be_bot=False)
        DeleteAllSessions = Route(url="auth/session/all", method="DELETE", with_auth=True, can_be_bot=False)


class User:
    class UserInformation:
        FetchUser = Route(url="users/:user", method="GET", with_auth=True, can_be_bot=True)
        EditUser = Route(url="users/@me", method="PATCH", with_auth=True, can_be_bot=True)
        ChangeUsername = Route(url="users/@me/username", method="PATCH", with_auth=True, can_be_bot=False)
        FetchUserProfile = Route(url="users/:user/profile", method="GET", with_auth=True, can_be_bot=True)
        FetchDefaultAvatar = Route(url="users/:user/default_avatar", method="GET", with_auth=False)
        FetchMutualFriends = Route(url="users/:user/mutual", method="GET", with_auth=True, can_be_bot=True)

    class DirectMessaging:
        FetchDirectMessageChannels = Route(url="users/dms", method="GET", with_auth=True, can_be_bot=True)
        OpenDirectMessage = Route(url="users/:user/dm", method="GET", with_auth=True, can_be_bot=True)

    class Relationships:
        FetchRelationships = Route(url="users/relationships", method="GET", with_auth=True, can_be_bot=False)
        FetchRelationship = Route(url="users/:user/relationship", method="GET", with_auth=True, can_be_bot=False)
        SendFriendRequestOrAcceptRequest = Route(
            url="users/:username/friend", method="PUT", with_auth=True, can_be_bot=False
        )
        DenyFriendRequestRemoveFriend = Route(
            url="users/:username/friend", method="DELETE", with_auth=True, can_be_bot=False
        )
        BlockUser = Route(url="users/:user/block", method="PUT", with_auth=True, can_be_bot=False)
        UnblockUser = Route(url="users/:user/block", method="DELETE", with_auth=True, can_be_bot=False)


class AccountBots:
    CreateBot = Route(url="bots/create", method="POST", with_auth=True, can_be_bot=False)
    FetchOwnedBots = Route(url="bots/@me", method="GET", with_auth=True, can_be_bot=False)
    FetchBot = Route(url="bots/:bot", method="GET", with_auth=True, can_be_bot=False)
    EditBot = Route(url="bots/:bot", method="PATCH", with_auth=True, can_be_bot=False)
    DeleteBot = Route(url="bots/:bot", method="DELETE", with_auth=True, can_be_bot=False)
    FetchPublicBot = Route(url="bots/:bot/invite", method="GET", with_auth=True, can_be_bot=False)
    InvitePublicBot = Route(url="bots/:bot/invite", method="POST", with_auth=True, can_be_bot=False)


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
    "AccountBots",
    "Channel",
    "Server",
    "Miscellaneous"
]
