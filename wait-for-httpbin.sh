#!/bin/sh

# httpbin sometimes times out, but comes back shortly after this
# happens. Apply a basic backoff scheme to give a chance to the tests
# to run later instead of failing.
for i in 1 2 3
do
    if curl http://httpbin.org >/dev/null
    then
        break
    fi
    duration=$(($RANDOM % 100 + 100 * i))
    echo "Sleeping for $duration seconds"
    sleep $duration
done
