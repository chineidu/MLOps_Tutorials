# ==========================================================
# Output Variable Block(s)
# These are the outputs of the modeule.
# ==========================================================
output "public_ip" {
  value = aws_instance.web.public_ip
}

output "public_dns" {
  value = aws_instance.web.public_dns
}
