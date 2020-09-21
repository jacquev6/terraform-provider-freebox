variable "freebox_token" {
  type = string
}

provider freebox {
    token = var.freebox_token
}

data freebox_connection_status connection_status {}

output wan_ip_address {
    value = data.freebox_connection_status.connection_status.ipv4
}
