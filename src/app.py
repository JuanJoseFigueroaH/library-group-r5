from fastapi import FastAPI
from starlette_graphene3 import GraphQLRouter
from fastapi.middleware.cors import CORSMiddleware
from .schemas import schema

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")