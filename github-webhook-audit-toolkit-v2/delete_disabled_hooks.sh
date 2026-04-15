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
    active=$(echo "$hook" | jq -r '.active')

    if [ "$active" = "false" ]; then
      echo "DELETING $repo_name -> $id"
      curl -s -X DELETE -H "Authorization: token $TOKEN" \
      "$API/repos/$ORG/$repo_name/hooks/$id"
    fi
  done
done
