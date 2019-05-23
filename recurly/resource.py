from pydoc import locate


class Resource:
    """Class representing a server-side object in Recurly"""

    # Allows us to override resource location
    locator = lambda class_name: locate("recurly.resources.%s" % class_name)

    @classmethod
    def cast(cls, properties):
        """Casts a dict of properties into a Recurly Resource"""

        if "object" not in properties:
            return properties

        if (
            properties["object"] == "list"
            and "data" in properties
            and "has_more" in properties
        ):
            properties["data"] = [Resource.cast(i) for i in properties["data"]]
            return Page(properties)

        name_parts = properties["object"].split("_")
        class_name = "".join(x.title() for x in name_parts)

        klass = cls.locator(class_name)

        if klass is None:
            return properties

        del properties["object"]
        for k, v in properties.items():
            if isinstance(v, dict):
                properties[k] = Resource.cast(v)
            elif isinstance(v, list):
                for i in range(len(v)):
                    if isinstance(v[i], dict):
                        v[i] = Resource.cast(v[i])

        return klass(properties)

    def __init__(self, properties):
        vars(self).update(properties)


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

    pass
