from typing import Any, Callable, Dict


class ServiceFactory:
    """
    A Factory that handles dynamic service discovery using a registry.
    """
    def __init__(self) -> None:
        self._services: Dict[str, Any] = {}

    def register_service(self, service_name: str, service_class: Any) -> None:
        """Registers a service class into the factory."""
        self._services[service_name] = service_class

    def get_service(self, service_name: str, *args, **kwargs) -> Any:
        """Discovers and instantiates a registered service by its name."""
        service_class = self._services.get(service_name)
        if not service_class:
            raise ValueError(f"Service '{service_name}' is not registered.")
        
        return service_class(*args, **kwargs)


# Global factory instance to be used across the microservice
service_factory = ServiceFactory()


def register(service_name: str) -> Callable:
    """
    A decorator to dynamically register services upon interpretation.
    """
    def wrapper(cls: Any) -> Any:
        service_factory.register_service(service_name, cls)
        return cls
    return wrapper