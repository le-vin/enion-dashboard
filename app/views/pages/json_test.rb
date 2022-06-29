py_file = Dir["app/assets/images/*.py"][0]
hello = `python #{py_file}`

require 'csv'
require 'json'

file = File.read(hello)
data_hash = JSON.parse(file)

puts(data_hash)