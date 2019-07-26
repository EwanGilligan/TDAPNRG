docker run --mount type=bind,source="$(pwd)/$1",target=/user/src/randology/output \
--mount type=bind,source="$(pwd)/$2",target=/user/src/randology/config.json \
randology
