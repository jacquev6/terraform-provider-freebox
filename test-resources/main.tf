variable "freebox_app_token" {
  type = string
}

provider freebox {
    app_id = "terraform-provider-freebox-tests"
    app_token = var.freebox_app_token
}

data freebox_connection_status connection_status {}

output connection_ipv4 {
    value = data.freebox_connection_status.connection_status.ipv4
}

output connection_ipv4_port_range {
    value = data.freebox_connection_status.connection_status.ipv4_port_range
}
