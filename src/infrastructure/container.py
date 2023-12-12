from dependency_injector import containers, providers
from logging.config import fileConfig
from src.infrastructure import PostgresContext

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["src.application.graphql"])
    config = providers.Configuration(yaml_files=["setting.yml"])
    logging = providers.Resource(
        fileConfig,
        fname="logging.ini"
    )
    postgres_context = providers.Singleton(
        PostgresContext,
        configuration=config
    )
    