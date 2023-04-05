from typedb.client import *

def initialise_database(uri, database, force=False):
    client = TypeDB.core_client(uri)
    if client.databases().contains(database):
        if force:
            client.databases().get(database).delete()
        else:
            raise ValueError(f"Database '{database}' already exists")
    client.databases().create(database)
    session = client.session(database, SessionType.SCHEMA)
    with open("schema/cti-schema.tql", "r") as schema_file:
        schema = schema_file.read()
    with open("schema/cti-rules.tql", "r") as rules_file:
        rules = rules_file.read()
    print('.....')
    print('Inserting schema and rules...')
    print('.....')
    with session.transaction(TransactionType.WRITE) as write_transaction:
        write_transaction.query().define(schema)
        write_transaction.commit()
    with session.transaction(TransactionType.WRITE) as write_transaction:
        write_transaction.query().define(rules)
        write_transaction.commit()
    print('.....')
    print('Successfully committed schema!')
    print('.....')
    session.close()
    client.close()