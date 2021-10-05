from jinja2 import Environment,FileSystemLoader
from sys import argv
import os
import yaml
template_dir,template_file = os.path.split(argv[1])
env = Environment(loader = FileSystemLoader(template_dir),trim_blocks=True,lstrip_blocks=True)
template = env.get_template(template_file)
data_file = argv[2]
gen_file = argv[3]
with open (data_file) as f:
    data_dict = yaml.safe_load(f)
with open (gen_file,'w') as f:
    f.write(template.render(data_dict))


