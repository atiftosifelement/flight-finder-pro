class FlightProvider:
    """Base class for all providers."""

    def search(self, *args, **kwargs):
        raise NotImplementedError("Provider must implement search()")
