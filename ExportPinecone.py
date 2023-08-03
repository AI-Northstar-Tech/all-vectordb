import pinecone
import sqlite3
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

class ExportQdrant:
    def __init__(self, index):
        """
        Initialize the index
        """
        self.index = index

    def get_data(self, index_name, vector_dim):
        """
        Get data from Qdrant
        """
        info = self.index.describe_index_stats()
        namespaces = info['namespaces']
        zero_array = [0] * vector_dim
        data = []
        for key, value in namespaces.items():
            response = self.index.query(namespace=key, top_k=value['vector_count'], include_metadata=True, include_values=True, vector=zero_array)
            data.append(response)
        con = sqlite3.connect(f'{index_name}_pinecone.db')
        cur = con.cursor()
        for response in data:
            namespace = response['namespace']
            property_names = list(response['matches'][0]['metadata'].keys())
            cur.execute(f"CREATE TABLE IF NOT EXISTS {namespace}_{index_name} (id, {','.join(property_names)})")
            insert_query = f"INSERT INTO {namespace}_{index_name} (id, {','.join(property_names)}) VALUES ({','.join(['?']*(len(property_names) + 1))})"
            self.insert_data(f"{index_name}_pinecone.parquet", response['matches'], property_names, insert_query, cur)

    def insert_data(file_path, objects, property_names, insert_query, cur):
        """
        Insert data into sqlite database and parquet file
        """
        data_to_insert = []
        vectors = []
        for object in objects:
            vectors.append({"Vectors" : object.values})
            data_dict = {}
            data_dict['id'] = object.id
            for property_name in property_names:
                if property_name in object.metadata:
                    data_dict[property_name] = object.metadata[property_name]
                else:
                    data_dict[property_name] = ''
            data_tuple = ()
            for property in data_dict.values():
                data_tuple += (property,)
            data_to_insert.append(data_tuple)
        vectors = pd.DataFrame(vectors)
        schema = pa.Table.from_pandas(vectors).schema
        with pq.ParquetWriter(file_path, schema) as writer:
            table = pa.Table.from_pandas(vectors, schema=schema)
            writer.write_table(table)
        cur.executemany(insert_query, data_to_insert)