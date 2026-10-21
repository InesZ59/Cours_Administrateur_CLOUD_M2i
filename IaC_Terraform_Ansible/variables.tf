variable "web_instances" {
  description = "Liste des conteneurs web à créer"
  type = list(object({
    name_prefix   = string
    name_suffix   = string
    external_port = number
    image         = string
  }))
  default = []
}

variable "db_instances" {
  description = "Liste des conteneurs MySQL à créer"
  type = list(object({
    name_prefix         = string
    name_suffix         = string
    external_port       = number
    image               = string
    mysql_root_password = string
    mysql_password      = string
    mysql_user          = string
    mysql_database      = string
  }))
  default = []
}
