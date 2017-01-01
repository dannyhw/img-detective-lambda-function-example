# img-detective-lambda-function-example

Testing out hash generation for duplicate image detection using lambda functions.

This is an example lambda function based on the imagehash library. The
repository is quite large due to the fact that external libraries need to be
provided explicitly.

you can update the existing function like so:

```shell
rm -f img-detective.zip
zip img-detective.zip ./* -r
aws s3 cp img-detective.zip s3://BUCKET_NAME
aws lambda update-function-code --function-name FUNCTION_NAME \
    --s3-bucket BUCKET_NAME --s3-key img-detective.zip
```

The file lambda.py contains the lambda function handler.
The hash generating code is in the imgdetective folder.

line length is kept to 80 characters when possible and doc string where
appropriate. Currently using flake8 as a linter