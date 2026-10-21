
output "web_containers" {
  description = "Liste des conteneurs web créés"
  value = {
    for key, container in module.web : key => {
      name = container.container_name
      port = container.container_port
    }
  }
}

output "mysql_containers" {
  description = "Liste des conteneurs MySQL créés"
  value = {
    for key, container in module.mysql : key => {
      name = container.container_name
      port = container.container_port
    }
  }
}