#!/bin/bash
OWNER="your-org"
REPO="your-repo"
TOKEN="ghp_xxx"
API="https://api.github.com"

echo "Deleting DISABLED webhooks..."

hooks=$(curl -s -H "Authorization: token $TOKEN" \
  "$API/repos/$OWNER/$REPO/hooks")

echo "$hooks" | jq -c '.[]' | while read hook; do
  id=$(echo "$hook" | jq -r '.id')
  active=$(echo "$hook" | jq -r '.active')

  if [ "$active" = "false" ]; then
    echo "Deleting hook $id"
    curl -s -X DELETE -H "Authorization: token $TOKEN" \
      "$API/repos/$OWNER/$REPO/hooks/$id"
  fi
done
