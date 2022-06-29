class ApplicationController < ActionController::Base
    def dashboard
        require 'json'
        python_file = Dir["app/assets/images/*.py"][1]
        @result = `python #{python_file}`
        py_file = Dir["app/assets/images/*.py"][0]
        hello = `python #{py_file}`
        @data_hash = JSON.parse(`python #{py_file}`)
    end
end
