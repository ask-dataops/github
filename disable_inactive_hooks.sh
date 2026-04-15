#!/bin/bash
OWNER="your-org"
REPO="your-repo"
TOKEN="ghp_xxx"
API="https://api.github.com"

echo "Disabling inactive webhooks..."

hooks=$(curl -s -H "Authorization: token $TOKEN" \
  "$API/repos/$OWNER/$REPO/hooks")

echo "$hooks" | jq -c '.[]' | while read hook; do
  id=$(echo "$hook" | jq -r '.id')

  deliveries=$(curl -s -H "Authorization: token $TOKEN" \
    "$API/repos/$OWNER/$REPO/hooks/$id/deliveries")

  count=$(echo "$deliveries" | jq 'length')

  if [ "$count" -eq 0 ]; then
    echo "Disabling hook $id"
    curl -s -X PATCH -H "Authorization: token $TOKEN" \
      "$API/repos/$OWNER/$REPO/hooks/$id" \
      -d '{"active":false}'
  fi
done
