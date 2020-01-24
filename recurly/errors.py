#
# This file is automatically created by Recurly's OpenAPI generation process
# and thus any edits you make by hand will be lost. If you wish to make a
# change to this file, please create a Github issue explaining the changes you
# need and we will usher them to the appropriate places.
import recurly


class BadRequestError(recurly.ApiError):
    pass


class InternalServerError(recurly.ApiError):
    pass


class ImmutableSubscriptionError(recurly.ApiError):
    pass


class InvalidApiKeyError(recurly.ApiError):
    pass


class InvalidApiVersionError(recurly.ApiError):
    pass


class InvalidContentTypeError(recurly.ApiError):
    pass


class InvalidPermissionsError(recurly.ApiError):
    pass


class InvalidTokenError(recurly.ApiError):
    pass


class NotFoundError(recurly.ApiError):
    pass


class SimultaneousRequestError(recurly.ApiError):
    pass


class TransactionError(recurly.ApiError):
    pass


class UnauthorizedError(recurly.ApiError):
    pass


class UnavailableInApiVersionError(recurly.ApiError):
    pass


class UnknownApiVersionError(recurly.ApiError):
    pass


class ValidationError(recurly.ApiError):
    pass


class MissingFeatureError(recurly.ApiError):
    pass


class RateLimitedError(recurly.ApiError):
    pass
