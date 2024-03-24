# ==========================================================
# Output Block(s)
# ==========================================================
output "public_ip" {
  value = aws_instance.ubuntu_server.public_ip
}

output "public_dns" {
  value = aws_instance.ubuntu_server.public_dns
}

output "public_ip_server_subnet_1" {
  value = aws_instance.web_server.public_ip
}

output "public_dns_server_subnet_1" {
  value = aws_instance.web_server.public_dns
}
