process transform {
  action blue_text {
    script { 
      "This action is a transform.  Its name should appear in blue text, 
indicating that the required resource is `transformed' into a different 
provided resource.

The required resource is not provided by any other action, so it is 
possibly an input, and thus should be rendered in green text.

The provided resource is not required by any other action, so it is
possbily an output, and thus should be rendered in red text." }

    requires { green_text }
    provides { red_text }

  }
}
