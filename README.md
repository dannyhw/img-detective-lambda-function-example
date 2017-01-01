# img-detective-lambda-function-example

Testing out hash generation for duplicate image detection using lambda functions.

This is an example lambda function based on the imagehash library. The repository is quite large
due to the fact that external libraries need to be provided explicitly.

you can update the exisiting function like so:

```shell
rm -f img-detective.zip
zip img-detective.zip ./* -r
aws s3 cp img-detective.zip s3://dannyhw-lambda-functions
aws lambda update-function-code --function-name image-hash-test --s3-bucket dannyhw-lambda-functions --s3-key img-detective.zip
```
