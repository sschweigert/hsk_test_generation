from jinja2 import Environment, FileSystemLoader
import subprocess


def generate_pdf(test_def, name):
    suffix = '.tex'
    if not name.endswith(suffix):
        name = name + suffix

    generate_tex(test_def, name)
    generate_pdf_from_tex(name)
    

def generate_tex(test_def, filename):
    env = Environment(loader=FileSystemLoader('templates/'), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('chinese_test.jinja')
    content = template.render(
        words_chinese=test_def['words_chinese'],
        sentences_chinese=test_def['sentences_chinese'],
        words_english=test_def['words_english'],
        sentences_english=test_def['sentences_english'],
        title=test_def['title']
    )

    with open(filename, mode='w') as message:
        message.write(content)
    
def generate_pdf_from_tex(tex_filename):
    subprocess.run(['xelatex', tex_filename])
