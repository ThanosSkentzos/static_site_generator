import os,shutil
from markdown import BlockTypes, block_to_block_type, extract_md_title, markdown_to_blocks, markdown_to_html_node

static = 'static'
public = 'public'
project_dir = os.getcwd()

def clean_dir(dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)

def copy_static_to_public():

    source = os.path.join(project_dir,static)
    dest = os.path.join(project_dir,public)
    clean_dir(dest)
    copy_src_dest(source,dest)



def copy_src_dest(src,dest):
    for dir in os.listdir(src):
        src_path = os.path.join(src,dir)
        dest_path = os.path.join(dest,dir)
        if os.path.isfile(src_path):
            shutil.copy(src_path,dest_path)
            # print(f"copy {src_path} to {dest_path}")
        else:
            os.mkdir(dest_path)
            # print(f"mkdir {dest_path}")
            copy_src_dest(src_path,dest_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path,'r') as f:
        markdown = f.read()
    with open(template_path,'r') as f:
        template = f.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_md_title(markdown)
    site = template.replace("{{ Title }}",title).replace("{{ Content }}",html)
    with open(dest_path,'w') as f:
        f.write(site)


def main():
    copy_static_to_public()
    markdown_path = os.path.join(project_dir,"content","index.md")
    template_path = os.path.join(project_dir,"template.html")
    html_path = os.path.join(project_dir,"public","index.html")
    generate_page(markdown_path,template_path,html_path)
if __name__=="__main__":
    main()
