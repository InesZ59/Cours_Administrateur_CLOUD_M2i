web_instances = [
  {
    name_prefix   = "prod-web-"
    name_suffix   = "01"
    external_port = 8081
    image         = "nginx:1.27-alpine"
  },
  {
    name_prefix   = "prod-web-"
    name_suffix   = "02"
    external_port = 8082
    image         = "nginx:1.27-alpine"
  },
  {
    name_prefix   = "prod-web-"
    name_suffix   = "03"
    external_port = 8083
    image         = "nginx:1.27-alpine"
  }
]

db_instances = [
  {
    name_prefix         = "prod-db-"
    name_suffix         = "01"
    external_port       = 3307
    image               = "mysql:8.4"
    mysql_root_password = "ProdRootPass123!"
    mysql_password      = "ProdAppPass123!"
    mysql_user          = "produser"
    mysql_database      = "proddb"
  },
  {
    name_prefix         = "prod-db-"
    name_suffix         = "02"
    external_port       = 3308
    image               = "mysql:8.4"
    mysql_root_password = "ProdRootPass456!"
    mysql_password      = "ProdAppPass456!"
    mysql_user          = "produser2"
    mysql_database      = "proddb2"
  }
]
