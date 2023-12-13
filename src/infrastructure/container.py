from dependency_injector import containers, providers
from logging.config import fileConfig
from src.infrastructure import PostgresContext, HttpClient
from src.domain.service import BookService
from src.domain.repository import BookRepository, BookExternalRepository

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
    http_client = providers.Singleton(
        HttpClient
    )
    repository_book = providers.Singleton(
        BookRepository,
        context=postgres_context
    )
    repository_book_external = providers.Singleton(
        BookExternalRepository,
        http_client=http_client,
        configuration=config
    )
    service_book = providers.Singleton(
        BookService,
        book_repository=repository_book,
        book_external_repository=repository_book_external
    )
