import graphene
from weblog.schema import WeblogQuery
from weblog.schema import WeblogCreate

class Query(
    WeblogQuery,
    ):
    pass

class Mutations(graphene.ObjectType):
    weblog_create = WeblogCreate.Field()

schema = graphene.Schema(
    query=Query,
    mutation=Mutations)
