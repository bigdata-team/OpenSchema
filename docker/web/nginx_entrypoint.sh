#!/bin/sh

function join_by { local IFS="$1"; shift; echo "$*"; }

############################################################################
# Find env vars
vars=$(env | grep VITE_ | awk -F = '{print "$"$1}')
vars=$(join_by ',' $vars)
echo "Found variables: $vars" >&2

# Replace env vars in JavaScript files
echo "Replacing env vars in JS" >&2
for file in  $(find /usr/share/nginx/html -name "*.js");
do
  echo "Processing $file ..."; >&2

  # Use the existing JS file as template
  if [ ! -f $file.tmpl ]; then
    cp $file $file.tmpl
  fi

  envsubst "$vars" < $file.tmpl > $file
done

echo "Starting Nginx" >&2
nginx -g 'daemon off;'
