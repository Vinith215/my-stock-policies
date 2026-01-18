package portfolio.authz

default allow = false

# Allow access if the user is an 'admin'
allow {
    input.user.role == "admin"
}

# Allow 'viewers' to see stocks not marked as 'restricted'
allow {
    input.user.role == "viewer"
    input.stock.restricted == false
}
