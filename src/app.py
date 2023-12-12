import strawberry
from fastapi import FastAPI
###from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from src.infrastructure.container import Container
from src.application.graphql.query import Query
from src.application.graphql.mutation import Mutation

app = FastAPI()

@app.get('/')
def home():
    return "Welcome application!"

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")