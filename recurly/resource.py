from pydoc import locate
import datetime
from datetime import timezone
import recurly
import json
import platform
from .response import Response

# TODO - more resilient parsing

DT_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
major, minor, patch = platform.python_version_tuple()
# For versions 3.6 and prior, timezone queries will return "None"
# instead of "UTC"
if major <= "3" and minor <= "6":
    DT_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class Resource:
    """Class representing a server-side object in Recurly"""

    # Allows us to override resource location for testing
    locator = lambda class_name: locate("recurly.resources.%s" % class_name)

    @classmethod
    def cast_file(cls, response):
        klass = cls.locator("BinaryFile")
        resource = klass()
        setattr(resource, "data", response.body)
        return resource

    @classmethod
    def cast_error(cls, response):
        if response.content_type == "application/json":
            json_body = json.loads(response.body.decode("utf-8"))

            error_json = json_body["error"]
            error_json["object"] = "error"
            error = cls.cast_json(error_json, response=response)
            error_type = error.type
            name_parts = error_type.split("_")
            class_name = "".join(x.title() for x in name_parts)
            msg = error.message + ". Recurly Request Id: " + response.request_id
        else:
            class_name = recurly.RecurlyError.error_from_status(response.status)
            error = None
            msg = "Unexpected %i Error. Recurly Request Id: %s" % (
                response.status,
                response.request_id,
            )
        if not class_name.endswith("Error"):
            class_name += "Error"
        klass = locate("recurly.errors.%s" % class_name)
        # Use a specific error class if we can find one, else
        # fall back to a generic ApiError
        if klass:
            return klass(msg, error)
        else:
            return recurly.ApiError(msg, error)

    @classmethod
    def cast_json(cls, properties, class_name=None, response=None):
        """Casts a dict of properties into a Recurly Resource"""

        if class_name is None and "object" in properties:
            # If it's a Page, let's return that now
            if (
                properties["object"] == "list"
                and "data" in properties
                and "has_more" in properties
            ):
                properties["data"] = [Resource.cast_json(i) for i in properties["data"]]
                return Page(properties)

            # If it's not a Page, we need to derive the class name
            # from the "object" property. The class_name passed in should
            # take precedence.
            name_parts = properties["object"].split("_")
            class_name = "".join(x.title() for x in name_parts)

        klass = cls.locator(class_name)

        # Special case for Empty class
        if class_name == Empty:
            klass = Empty

        # If we can't find a resource class, we should return
        # the untyped properties dict. If in strict-mode, explode.
        if klass is None:
            if recurly.STRICT_MODE:
                raise ValueError("Class could not be found for json: %s" % properties)
            else:
                return properties

        resource = klass()
        for k, v in properties.items():
            attr = None
            attr_type = klass.schema.get(k)
            if attr_type:
                # if the value is None, let's set to none
                # and skip the casting
                if v is None:
                    attr = None

                # if it's a plain type, use the type to cast it
                elif type(attr_type) == type:
                    attr = attr_type(v)

                # if it's a datetime, parse it
                elif attr_type == datetime:
                    attr = datetime.datetime.strptime(v, DT_FORMAT)

                # If the schema type a string, it's a reference
                # to another resource
                elif isinstance(attr_type, str) and isinstance(v, dict):
                    attr = Resource.cast_json(v, class_name=attr_type)

                # If the schema type is a list of strings, it's a reference
                # to a list of resources
                elif (
                    isinstance(attr_type, list)
                    and isinstance(attr_type[0], str)
                    and isinstance(v, list)
                ):
                    attr = [Resource.cast_json(r, class_name=attr_type[0]) for r in v]

            # We want to explode in strict mode because
            # the schema doesn't know about this attribute. In production
            # we will just set the attr to it's value or None
            if recurly.STRICT_MODE and attr_type is None:
                raise ValueError(
                    "%s could not find property %s in schema %s given value %s"
                    % (klass.__name__, k, klass.schema, v)
                )
            else:
                setattr(resource, k, attr)

        if response:
            # Maintain JSON parsed body for version < 4
            response.body = properties
            # TODO: Remove this (^^) for version 4
            resource.__response = response

        return resource

    def __repr__(self):
        return str(vars(self))

    def get_response(self):
        """
        Returns
        -------
        Response
            The metadata about the response from the recurly server
        """
        return self.__response


class Empty(Resource):
    """A special resource that represents an empty response"""

    pass


class Page(Resource):
    """A special resource that represents a single page of data

    Attributes
    ----------

    has_more : bool
        True if there is another page of data available
    next : str
        The relative path to the next page of data
    data : :obj:`list` of :obj:`Resource`
        The list of data for this page. The data will be the requested type of Resource.
    """

    def __init__(self, properties):
        vars(self).update(properties)
