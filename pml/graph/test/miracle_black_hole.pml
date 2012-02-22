process miracle_black_hole {
  action blue_fill_rect {
    provides { black_text }
    script { "This action is a `miracl': an action that providesa
resource, but does not require any resource.  It should be rendered as a 
blue-filled square-corner rectangle with black text." }
  }
  action grey_fill_rect {
    script { "This action is a `black hole': an action that requires a 
resource, but does not provide a resource.  It should be rendered as a 
grey-filled square-corner rectangle with black text." }
    requires { black_text }
  }
}
