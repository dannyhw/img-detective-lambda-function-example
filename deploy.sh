rm -f img-detective.zip
zip img-detective.zip ./* -r
aws s3 cp img-detective.zip s3://dannyhw-lambda-functions
aws lambda update-function-code --function-name image-hash-test --s3-bucket dannyhw-lambda-functions --s3-key img-detective.zip