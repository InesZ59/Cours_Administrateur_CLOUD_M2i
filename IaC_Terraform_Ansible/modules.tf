module "web" {
  source = "./modules/web"

  for_each = {
    for item in var.web_instances : "${item.name_prefix}${item.name_suffix}" => item
  }

  name_prefix   = each.value.name_prefix
  name_suffix   = each.value.name_suffix
  external_port = each.value.external_port
  image         = each.value.image
}
module "mysql" {
  source = "./modules/mysql"

  for_each = {
    for item in var.db_instances : "${item.name_prefix}${item.name_suffix}" => item
  }

  name_prefix = each.value.name_prefix
  name_suffix = each.value.name_suffix

  external_port = each.value.external_port
  image         = each.value.image

  mysql_root_password = each.value.mysql_root_password
  mysql_password      = each.value.mysql_password
  mysql_user          = each.value.mysql_user
  mysql_database      = each.value.mysql_database
}