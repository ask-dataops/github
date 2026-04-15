In GitHub webhooks, the “secret” is not centrally stored in GitHub in a retrievable way, and it’s also not owned by GitHub long-term in a usable form.
So the real answer is:
The system that created/configured the webhook owns the secret and must manage rotation.

if webhook is deleted in github
Immediate effect
1. GitHub stops sending events instantly
No more webhook POST requests
No retries
No background queue

👉 From GitHub’s perspective, the integration is gone.

🔐 What happens to the Jira-held secret
Jira still keeps its stored secret/config
It becomes orphaned configuration
 

# GitHub Webhook Cleanup Toolkit

This toolkit helps you safely audit, disable, and delete unused GitHub webhooks.

## Files

### 1. list_never_fired.sh
Lists all webhooks that have never received any deliveries.

### 2. disable_inactive_hooks.sh
Soft-disables webhooks that are never fired or inactive by clearing events.

### 3. delete_disabled_hooks.sh
Deletes webhooks that are already disabled or have no events.

---

## Requirements

- curl
- jq
- bash
- GitHub Personal Access Token with:
  - repo
  - admin:repo_hook

---

## Usage

```bash
chmod +x *.sh

# Step 1: list
./list_never_fired.sh

# Step 2: disable
./disable_inactive_hooks.sh

# Step 3: delete
./delete_disabled_hooks.sh
```

---

## Safety Flow

1. Discover unused hooks
2. Disable first (safe mode)
3. Wait and observe
4. Delete only confirmed unused hooks

---

## Warning

Be careful with integrations like Jira, Jenkins, Harness.
They may recreate webhooks automatically.
