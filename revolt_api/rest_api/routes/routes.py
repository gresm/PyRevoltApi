class Platform:
    class Core:
        pass

    class OnBoarding:
        pass


class Auth:
    class Account:
        pass

    class Session:
        pass


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
