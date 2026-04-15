#!/bin/bash
ORG="your-org"
TOKEN="ghp_xxx"
API="https://api.github.com"

repos=$(curl -s -H "Authorization: token $TOKEN" \
"$API/orgs/$ORG/repos?per_page=100")

echo "$repos" | jq -c '.[] | select(.name | test("ABC"; "i"))' | while read repo; do
  repo_name=$(echo "$repo" | jq -r '.name')

  hooks=$(curl -s -H "Authorization: token $TOKEN" \
  "$API/repos/$ORG/$repo_name/hooks")

  echo "$hooks" | jq -c '.[]' | while read hook; do
    id=$(echo "$hook" | jq -r '.id')

    deliveries=$(curl -s -H "Authorization: token $TOKEN" \
    "$API/repos/$ORG/$repo_name/hooks/$id/deliveries")

    count=$(echo "$deliveries" | jq 'length')

    if [ "$count" -eq 0 ]; then
      echo "DISABLING $repo_name -> $id"
      curl -s -X PATCH -H "Authorization: token $TOKEN" \
      "$API/repos/$ORG/$repo_name/hooks/$id" \
      -d '{"active":false}'
    fi
  done
done
