# MongoDB Import/Export Utility

This guide provides a comprehensive overview of how to effectively import and export VDF formatted to and from MongoDB collections.

## Prerequisites

Ensure you have reviewed the root [README](../README.md) of this repository before proceeding.

## Command-Line Usage

### Shared Arguments

- `<connection_string>`: Your MongoDB Atlas connection string.
- `<database_name>`: The name of your MongoDB database.
- `<collection_name>`: The name of your MongoDB collection.
- `<vector_dimension>`: The dimension of the vector columns to be imported/exported. If not specified, the script will auto-detect the dimension.

### 1. Exporting Data from MongoDB

To export data from a MongoDB collection to a VDF (Vector Data Format) dataset:

```bash
export_vdf mongodb --connection_string <connection_string> --database <database_name> --collection <collection_name> --vector_dim <vector_dimension>
```

### 2. Importing Data to MongoDB

To import data from a VDF dataset into a MongoDB collection:

```bash
import_vdf -d <vdf_directory> mongodb --connection_string <connection_string> --database <database_name> --collection <collection_name> --vector_dim <vector_dimension>
```

**Additional Argument** for Import:

- `<vdf_directory>`: Path to the VDF dataset directory on your system.

### Example Usage

#### Export Example

To export data from a MongoDB collection called `my_collection` in the database `my_database`, where vectors are of dimension 128:

```bash
export_vdf mongodb --connection_string "mongodb+srv://<username>:<password>@<cluster_name>.mongodb.net/<database_name>?retryWrites=true&w=majority" --database "my_database" --collection "my_collection" --vector_dim 128
```

#### Import Example

To import data from a VDF dataset located in `/path/to/vdf/dataset` into the MongoDB collection `sample_collection`:

```bash
import_vdf -d /path/to/vdf/dataset mongodb --connection_string "mongodb+srv://<username>:<password>@<cluster_name>.mongodb.net/<database_name>?retryWrites=true&w=majority" --database "sample_database" --collection "sample_collection" --vector_dim 128
```

## Key Features

- **Batch Processing**: Both import and export operations support batching for improved efficiency.
- **Data Type Conversion**: Automatically converts data types to corresponding MongoDB-compatible formats.
- **Auto-detection**: If the `vector_dim` parameter is not specified, the utility will automatically detect the dimension of the vectors.
- **Interactive Mode**: The utility will prompt for any missing arguments if they are not provided via the command line.

## Additional Notes

- Always verify that your `<connection_string>` contains the correct username, password, cluster name, and database details.
- Ensure the VDF dataset is properly formatted to match MongoDB's expected data types and structure.

## Troubleshooting

- Ensure that your IP address is configured in the **Network Access** section of your MongoDB Atlas dashboard to allow connections to your MongoDB instance. If you encounter difficulties with the connection string format, consult [MongoDB's official documentation](https://www.mongodb.com/docs/atlas/connect-to-cluster/) for detailed guidance.

- For any issues related to vector dimension mismatches, verify that the vector dimension in the VDF dataset matches the `vector_dim` parameter you provide during import or export operations.
