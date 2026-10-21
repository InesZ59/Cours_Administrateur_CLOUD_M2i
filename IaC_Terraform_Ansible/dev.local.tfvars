web_instances = [
  {
    name_prefix   = "dev-web-"
    name_suffix   = "01"
    external_port = 8081
    image         = "nginx:latest"
  },
  {
    name_prefix   = "dev-web-"
    name_suffix   = "02"
    external_port = 8082
    image         = "nginx:latest"
  },
  {
    name_prefix   = "dev-web-"
    name_suffix   = "03"
    external_port = 8083
    image         = "nginx:latest"
  }
]

db_instances = [
  {
    name_prefix         = "dev-db-"
    name_suffix         = "01"
    external_port       = 3307
    image               = "mysql:8.0"
    mysql_root_password = "RootPass123!"
    mysql_password      = "AppPass123!"
    mysql_user          = "appuser"
    mysql_database      = "appdb"
  },
  {
    name_prefix         = "dev-db-"
    name_suffix         = "02"
    external_port       = 3308
    image               = "mysql:8.0"
    mysql_root_password = "RootPass456!"
    mysql_password      = "AppPass456!"
    mysql_user          = "appuser2"
    mysql_database      = "appdb2"
  }
]
