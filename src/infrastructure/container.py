from dependency_injector import containers, providers
from logging.config import fileConfig
from src.infrastructure import PostgresContext
from src.domain.service import BookService
from src.domain.repository import BookRepository

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
    repository_book = providers.Singleton(
        BookRepository,
        context=postgres_context
    )
    service_book = providers.Singleton(
        BookService,
        book_repository=repository_book
    )