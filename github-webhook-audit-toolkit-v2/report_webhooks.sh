#!/bin/bash
ORG="your-org"
TOKEN="ghp_xxx"
API="https://api.github.com"

CSV="webhook_report.csv"
JSON="webhook_report.json"

echo "[]" > "$JSON"
echo "repo,hook_id,url,active,delivery_count,last_delivery" > "$CSV"

repos=$(curl -s -H "Authorization: token $TOKEN" \
"$API/orgs/$ORG/repos?per_page=100")

echo "$repos" | jq -c '.[] | select(.name | test("ABC"; "i"))' | while read repo; do
  repo_name=$(echo "$repo" | jq -r '.name')

  hooks=$(curl -s -H "Authorization: token $TOKEN" \
  "$API/repos/$ORG/$repo_name/hooks")

  echo "$hooks" | jq -c '.[]' | while read hook; do
    id=$(echo "$hook" | jq -r '.id')
    url=$(echo "$hook" | jq -r '.config.url')
    active=$(echo "$hook" | jq -r '.active')

    deliveries=$(curl -s -H "Authorization: token $TOKEN" \
    "$API/repos/$ORG/$repo_name/hooks/$id/deliveries")

    count=$(echo "$deliveries" | jq 'length')
    last=$(echo "$deliveries" | jq -r '.[0].delivered_at // "never"')

    echo "$repo_name,$id,$url,$active,$count,$last" >> "$CSV"

    jq --arg r "$repo_name" --arg i "$id" --arg u "$url" --arg a "$active" --arg c "$count" --arg l "$last"     '. += [{repo:$r,hook_id:$i,url:$u,active:$a,delivery_count:($c|tonumber),last_delivery:$l}]' "$JSON" > tmp.json && mv tmp.json "$JSON"
  done
done

echo "DONE"
