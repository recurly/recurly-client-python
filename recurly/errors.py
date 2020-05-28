#
# This file is automatically created by Recurly's OpenAPI generation process
# and thus any edits you make by hand will be lost. If you wish to make a
# change to this file, please create a Github issue explaining the changes you
# need and we will usher them to the appropriate places.
import recurly

ERROR_MAP = {
    500: "InternalServerError",
    502: "BadGatewayError",
    503: "ServiceUnavailableError",
    304: "NotModifiedError",
    400: "BadRequestError",
    401: "UnauthorizedError",
    402: "PaymentRequiredError",
    403: "ForbiddenError",
    404: "NotFoundError",
    406: "NotAcceptableError",
    412: "PreconditionFailedError",
    422: "UnprocessableEntityError",
    429: "TooManyRequestsError",
}


class ResponseError(recurly.ApiError):
    pass


class ServerError(ResponseError):
    pass


class InternalServerError(ServerError):
    pass


class BadGatewayError(ServerError):
    pass


class ServiceUnavailableError(ServerError):
    pass


class RedirectionError(ResponseError):
    pass


class NotModifiedError(ResponseError):
    pass


class ClientError(recurly.ApiError):
    pass


class BadRequestError(ClientError):
    pass


class InvalidContentTypeError(BadRequestError):
    pass


class UnauthorizedError(ClientError):
    pass


class PaymentRequiredError(ClientError):
    pass


class ForbiddenError(ClientError):
    pass


class InvalidApiKeyError(ForbiddenError):
    pass


class InvalidPermissionsError(ForbiddenError):
    pass


class NotFoundError(ClientError):
    pass


class NotAcceptableError(ClientError):
    pass


class UnknownApiVersionError(NotAcceptableError):
    pass


class UnavailableInApiVersionError(NotAcceptableError):
    pass


class InvalidApiVersionError(NotAcceptableError):
    pass


class PreconditionFailedError(ClientError):
    pass


class UnprocessableEntityError(ClientError):
    pass


class ValidationError(UnprocessableEntityError):
    pass


class MissingFeatureError(UnprocessableEntityError):
    pass


class TransactionError(UnprocessableEntityError):
    pass


class SimultaneousRequestError(UnprocessableEntityError):
    pass


class ImmutableSubscriptionError(UnprocessableEntityError):
    pass


class InvalidTokenError(UnprocessableEntityError):
    pass


class TooManyRequestsError(ClientError):
    pass


class RateLimitedError(TooManyRequestsError):
    pass
