from jinja2 import Environment,FileSystemLoader
from sys import argv
import os
import yaml

template_dir, template_file = os.path.split(argv[1])
vars_file = argv[2]
env = Environment(
        loader=FileSystemLoader(template_dir),
        trim_blocks=False,
        lstrip_blocks=False
        )
template = env.get_template(template_file)
with open(vars_file) as f:
    vars_dict = yaml.safe_load(f)
print(template.render(vars_dict))

