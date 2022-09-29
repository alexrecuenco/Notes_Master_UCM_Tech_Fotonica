#!/usr/bin/env Rscript

input <- commandArgs(trailingOnly = TRUE)
print(input)
if (length(input) != 1) {
  print("Function only allows one argument")
  quit(status=1, save="no")
}
file <- input[1]

if (xfun::file_ext(file) != "ipynb") {
  print("Function only allows .ipynb files")
  quit(status=1, save="no")
}
output <- xfun::with_ext(input, "Rmd")

if (file.exists(output)) {
  print("Function is confident we are overwriting file output if we proceed")
  quit(status=1, save="no")
}
rmarkdown::convert_ipynb(input = file, output = xfun::with_ext(input, "Rmd"))
