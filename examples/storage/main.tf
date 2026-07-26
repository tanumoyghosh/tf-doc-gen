resource "random_string" "suffix" {
  length = 6
}

resource "random_integer" "priority" {
  min = 100
  max = 999
}
