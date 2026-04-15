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
