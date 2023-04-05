import logging
from functools import partial
from multiprocessing.dummy import Pool as ThreadPool
from timeit import default_timer as timer

from typedb.client import *


def data_count(uri, database):
    with TypeDB.core_client(uri) as client:
        with client.session(database, SessionType.DATA) as session:
            with session.transaction(TransactionType.READ) as tx:
                return tx.query().match_aggregate("match $x isa thing; count;").get().as_int()


class TypeDBInserter:

    def __init__(self, uri, database, batch_size=50, num_threads=16):
        self.database = database
        self.batch_size = batch_size
        self.num_threads = num_threads
        self.client = TypeDB.core_client(uri)

    def insert(self, queries):
        start = timer()
        batch = []
        batches = []
        print(f"Inserting {len(queries)} queries...")
        for q in queries:
            batch.append(q)
            if len(batch) == self.batch_size:
                batches.append(batch)
                batch = []
        batches.append(batch)

        with self.client.session(self.database, SessionType.DATA) as session:
            pool = ThreadPool(self.num_threads)
            pool.map(partial(self._insert_query_batch, session), batches)
            pool.close()
            pool.join()
        end = timer()
        logging.debug(f"Inserted {len(queries)} in {end - start} seconds")

    def _insert_query_batch(self, session, batch):
        with session.transaction(TransactionType.WRITE) as tx:
            for query in batch:
                tx.query().insert(query)
            tx.commit()

    def close(self):
        self.client.close()