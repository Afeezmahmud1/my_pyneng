import yaml
from jinja2 import Environment,FileSystemLoader
from pprint import pprint

def generate_config(templates,data_dict):
    template_dir,template_file = templates.split('/')
    env = Environment(loader = FileSystemLoader(template_dir),trim_blocks=True,lstrip_blocks=True)
    template = env.get_template(template_file)
    return template.render(data_dict)

if __name__ == "__main__":
    data_file = "data_files/cisco_ospf.yml"
    template_file = "templates/cisco_ospf.txt"
    with open(data_file) as f:
        data = yaml.safe_load(f)
    print(generate_config(template_file, data))

