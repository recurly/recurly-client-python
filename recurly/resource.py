from pydoc import locate
import datetime
import recurly

# TODO - more resilient parsing
DT_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class Resource:
    """Class representing a server-side object in Recurly"""

    # Allows us to override resource location for testing
    locator = lambda class_name: locate("recurly.resources.%s" % class_name)

    @classmethod
    def cast(cls, properties, class_name=None):
        """Casts a dict of properties into a Recurly Resource"""

        if class_name is None and "object" in properties:
            # If it's a Page, let's return that now
            if (
                properties["object"] == "list"
                and "data" in properties
                and "has_more" in properties
            ):
                properties["data"] = [Resource.cast(i) for i in properties["data"]]
                return Page(properties)

            # If it's not a Page, we need to derive the class name
            # from the "object" property. The class_name passed in should
            # take precedence.
            name_parts = properties["object"].split("_")
            class_name = "".join(x.title() for x in name_parts)

        klass = cls.locator(class_name)

        # If we can't find a resource class, we should return
        # the untyped properties dict. If in strict-mode, explode.
        if klass is None:
            if recurly.STRICT_MODE:
                raise ValueError("Class could not be found for json: %s" % properties)
            else:
                return properties

        resource = klass()
        for k, v in properties.items():
            # Skip "object" attributes
            if k == "object":
                continue

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
                    attr = Resource.cast(v, class_name=attr_type)

                # If the schema type is a list of strings, it's a reference
                # to a list of resources
                elif (
                    isinstance(attr_type, list)
                    and isinstance(attr_type[0], str)
                    and isinstance(v, list)
                ):
                    attr = [Resource.cast(r, class_name=attr_type[0]) for r in v]

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

        return resource


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
