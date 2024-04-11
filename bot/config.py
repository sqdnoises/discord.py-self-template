BOT_NAME = "template bot"
DEFAULT_PREFIX = "."
ADMINS = [1077982815070728223]

MISSING_ARGUMENT_MESSAGE = True
MISSING_ARGUMENT_MESSAGE = ("Missing argument `{argument}` of type `{type}`.\n"
                            "For more information refer to `{prefix}help {command.qualified_name}`.")
NO_PERMISSIONS_MESSAGE = "You don't have permissions to use this command."
BOT_NO_PERMISSIONS_MESSAGE = ("I'm missing permissions to run this command.\n"
                              "Permissions required: {joined_permissions_code}")

HELP_PAGE_ITEMS = 5

TIME_FORMAT = "%d %b %Y - %H:%M"
LOGGER_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

COGS_EXCLUDE = ["template"]