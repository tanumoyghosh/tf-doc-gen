<!-- BEGIN_TF_DOCS -->

## Example Usage

```hcl
module "storage" {
  source              = "./modules/storage"

  resource_group_name = "<resource_group_name>"
  location            = "eastus"
  tags                = {
    <key> = "<value>"
  }
}
```

## Requirements

| Name | Version |
|------|---------|
| Terraform | `>= 1.6.0` |

## Providers

| Name | Source | Version |
|------|--------|---------|
| azurerm | `hashicorp/azurerm` | `~> 4.0` |
| random | `hashicorp/random` | `~> 3.7` |

## Resources

| Type | Name |
|------|------|
| `random_string` | `suffix` |
| `random_integer` | `priority` |

## Inputs

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `resource_group_name` | `string` | - | Resource Group Name |
| `location` | `string` | `eastus` | Azure Region |
| `tags` | `map(string)` | `{}` | Resource tags |

## Outputs

| Name | Description |
|------|-------------|
| `storage_account_id` | ID of the storage account |
| `storage_account_name` | Name of the storage account |

<!-- END_TF_DOCS -->
