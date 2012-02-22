process example {
  action a {
    requires { R }
    provides { S }
  }
  action b {
    requires { S }
    provides { T }
  }
}
