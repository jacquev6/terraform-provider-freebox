provider freebox {
}

data freebox_connection_status connection_status {}

output wan_ip_address {
    value = data.freebox_connection_status.connection_status.ip
}
