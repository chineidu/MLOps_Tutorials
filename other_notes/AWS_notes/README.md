# AWS CLI Tutorial


## Table of Content

- [AWS CLI Tutorial](#aws-cli-tutorial)
  - [Table of Content](#table-of-content)
  - [Common Operations](#common-operations)
    - [Copy Files](#copy-files)
    - [List Objects In A Bucket](#list-objects-in-a-bucket)

## Common Operations

### Copy Files

```sh
aws s3 cp <s3://bucket> <destination/file/path> --recursive

# e.g.
aws s3 cp s3://my-special-bucket/huge_data.parquet/ ./data --recursive
```

### List Objects In A Bucket

```sh
aws s3 ls <s3://bucket>

# e.g.
aws s3 ls s3://my-special-bucket/raw_trans_data/
```
