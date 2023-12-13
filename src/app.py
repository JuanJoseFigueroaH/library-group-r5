import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.container import Container
from src.application.graphql.query import Query
from src.application.graphql.mutation import Mutation

app = FastAPI()
container = Container()
container.init_resources()
app.container = container

@app.get('/')
def home():
    return "Welcome application!"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")