#!/bin/bash
OWNER="your-org"
REPO="your-repo"
TOKEN="ghp_xxx"
API="https://api.github.com"

echo "Listing NEVER FIRED webhooks..."

hooks=$(curl -s -H "Authorization: token $TOKEN" \
  "$API/repos/$OWNER/$REPO/hooks")

echo "$hooks" | jq -c '.[]' | while read hook; do
  id=$(echo "$hook" | jq -r '.id')
  url=$(echo "$hook" | jq -r '.config.url')

  deliveries=$(curl -s -H "Authorization: token $TOKEN" \
    "$API/repos/$OWNER/$REPO/hooks/$id/deliveries")

  count=$(echo "$deliveries" | jq 'length')

  if [ "$count" -eq 0 ]; then
    echo "NEVER FIRED -> ID:$id URL:$url"
  fi
done
