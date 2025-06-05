import os
import pathlib
import shutil
import markdown2
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.lexers import get_lexer_for_filename, guess_lexer
from pygments.formatters import HtmlFormatter

TARGET_DIRECTORIES = ['design-patterns', 'oop', 'problems', 'solutions']
BASE_OUTPUT_DIR = "docs"
ROOT_IMAGES_DIR = 'images'

image_path_map = {} # Global map: original_absolute_path -> new_path_relative_to_docs_root

def get_html_file_depth(html_output_path_obj, root_output_dir_path_obj):
    try:
        relative_to_docs = html_output_path_obj.relative_to(root_output_dir_path_obj)
        return len(relative_to_docs.parent.parts)
    except ValueError:
        return 0

def get_relative_css_path(html_file_depth):
    if html_file_depth == 0: return "css/style.css"
    return ("../" * html_file_depth) + "css/style.css"

def get_file_type(filepath_str):
    _, ext = os.path.splitext(filepath_str)
    ext = ext.lower()
    if ext == '.md': return 'markdown'
    if ext in ['.py', '.java', '.js', '.cpp', '.h', '.cs', '.go']: return 'code'
    if ext in ['.png', '.jpg', '.jpeg', '.gif']: return 'image'
    return 'unknown'

# --- Pass 2: Image Processing ---
def process_image_file(image_filepath_abs_str, base_processing_dir_abs_str):
    global image_path_map
    try:
        image_filepath_abs = pathlib.Path(image_filepath_abs_str)
        base_processing_dir_abs = pathlib.Path(base_processing_dir_abs_str)

        image_rel_to_scan_scope = image_filepath_abs.relative_to(base_processing_dir_abs)

        dest_image_path_in_docs_abs = (pathlib.Path(BASE_OUTPUT_DIR).resolve() / 'images' / image_rel_to_scan_scope)

        dest_image_dir_abs = dest_image_path_in_docs_abs.parent
        dest_image_dir_abs.mkdir(parents=True, exist_ok=True)

        shutil.copy2(image_filepath_abs_str, dest_image_path_in_docs_abs)

        new_path_relative_to_docs_root = dest_image_path_in_docs_abs.relative_to(pathlib.Path(BASE_OUTPUT_DIR).resolve())
        image_path_map[str(image_filepath_abs)] = str(new_path_relative_to_docs_root)

        print(f"Copied image: {image_filepath_abs_str} -> {dest_image_path_in_docs_abs}")
    except Exception as e:
        print(f"Error copying image {image_filepath_abs_str}: {e}")


# --- Pass 3: Markdown Processing ---
def convert_markdown_to_html(md_filepath_str, html_output_path_obj):
    global image_path_map
    try:
        md_filename = html_output_path_obj.stem
        title = md_filename if md_filename != "index" else html_output_path_obj.parent.name

        with open(md_filepath_str, 'r', encoding='utf-8') as f: md_content = f.read()

        converted_html_content = markdown2.markdown(md_content, extras=["fenced-code-blocks", "tables", "markdown-in-html"]) # Added extras

        soup = BeautifulSoup(converted_html_content, 'lxml')
        img_tags = soup.find_all('img')
        for img_tag in img_tags:
            src = img_tag.get('src')
            if not src or src.startswith('http://') or src.startswith('https://'):
                continue

            original_image_abs_path_str = str(pathlib.Path(md_filepath_str).parent.joinpath(src).resolve())

            if original_image_abs_path_str in image_path_map:
                new_image_path_in_docs = image_path_map[original_image_abs_path_str] # Relative to docs root

                # Calculate path from current HTML file to the new image path in docs
                html_file_dir_abs_path = html_output_path_obj.parent.resolve()
                target_image_abs_path_in_docs = pathlib.Path(BASE_OUTPUT_DIR).resolve() / new_image_path_in_docs

                new_relative_src = os.path.relpath(str(target_image_abs_path_in_docs), str(html_file_dir_abs_path))
                img_tag['src'] = new_relative_src
                print(f"Rewrote IMG SRC in {md_filepath_str}: '{src}' -> '{new_relative_src}'")
            else:
                print(f"Warning: Image source '{src}' in '{md_filepath_str}' (resolved to '{original_image_abs_path_str}') not found in image_path_map.")

        converted_html_content = str(soup)

        depth = get_html_file_depth(html_output_path_obj, pathlib.Path(BASE_OUTPUT_DIR).resolve())
        relative_css_path = get_relative_css_path(depth)

        full_html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{title}</title><link rel="stylesheet" href="{relative_css_path}"></head><body><div class="container">{converted_html_content}</div></body></html>"""
        html_output_path_obj.parent.mkdir(parents=True, exist_ok=True)
        with open(html_output_path_obj, 'w', encoding='utf-8') as f: f.write(full_html)
        print(f"Converted MD: {md_filepath_str} -> {html_output_path_obj}")
        return html_output_path_obj.name
    except Exception as e:
        print(f"Error converting MD {md_filepath_str}: {e}")
        return None

# --- Pass 4: Code Processing ---
def process_code_file(code_filepath_str, html_output_path_obj):
    try:
        title = pathlib.Path(html_output_path_obj.stem).stem
        with open(code_filepath_str, 'r', encoding='utf-8') as f: code_content = f.read()
        try:
            lexer = get_lexer_for_filename(code_filepath_str, ignore=True)
        except Exception:
            lexer = guess_lexer(code_content)
            print(f"Note: Guessed lexer for {code_filepath_str}")

        formatter = HtmlFormatter(full=False, linenos=True, cssclass='syntax', wrapcode=True)
        highlighted_code_content = highlight(code_content, lexer, formatter)

        depth = get_html_file_depth(html_output_path_obj, pathlib.Path(BASE_OUTPUT_DIR).resolve())
        relative_css_path = get_relative_css_path(depth)

        full_html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{title}</title><link rel="stylesheet" href="{relative_css_path}"></head><body><div class="container">{highlighted_code_content}</div></body></html>"""
        html_output_path_obj.parent.mkdir(parents=True, exist_ok=True)
        with open(html_output_path_obj, 'w', encoding='utf-8') as f: f.write(full_html)
        print(f"Processed Code: {code_filepath_str} -> {html_output_path_obj}")
        return html_output_path_obj.name
    except Exception as e:
        print(f"Error processing code file {code_filepath_str}: {e}")
        return None

# --- Pass 5: Index Generation ---
def generate_index_html(current_dir_output_relative_path_str, subdirectories, html_files, root_output_dir_str):
    # (Content largely same as before, ensure paths are correct)
    root_output_dir_path = pathlib.Path(root_output_dir_str).resolve()
    title_path = current_dir_output_relative_path_str if current_dir_output_relative_path_str else "Root Index"

    if not current_dir_output_relative_path_str:
        index_full_path = root_output_dir_path / "index.html"
    else:
        index_full_path = root_output_dir_path / current_dir_output_relative_path_str / "index.html"

    depth = get_html_file_depth(index_full_path, root_output_dir_path)
    relative_css_path = get_relative_css_path(depth)
    index_full_path.parent.mkdir(parents=True, exist_ok=True)

    content = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Index of {title_path}</title><link rel="stylesheet" href="{relative_css_path}"></head><body><div class="container"><h1>Index of {title_path}</h1>"""
    if current_dir_output_relative_path_str: content += '<p><a href="../index.html">Parent Directory</a></p>'
    content += "<h2>Subdirectories:</h2><ul>"
    for subdir in sorted(list(subdirectories)): content += f'<li><a href="{subdir}/index.html">{subdir}/</a></li>'
    content += "</ul><h2>Files:</h2><ul>"
    for f_name in sorted(list(html_files)): content += f'<li><a href="{f_name}">{f_name}</a></li>'
    content += "</ul></div></body></html>"
    with open(index_full_path, 'w', encoding='utf-8') as f: f.write(content)
    print(f"Generated Index: {index_full_path}")


if __name__ == "__main__":
    base_output_path_obj = pathlib.Path(BASE_OUTPUT_DIR).resolve()
    base_output_path_obj.mkdir(parents=True, exist_ok=True)

    # --- Pass 1: Data Collection ---
    dir_index_data = {} # For index.html generation
    image_processing_queue = [] # List of (abs_image_path_str, abs_base_processing_dir_str)
    markdown_processing_queue = [] # List of (abs_md_path_str, html_output_path_obj)
    code_processing_queue = [] # List of (abs_code_path_str, html_output_path_obj)

    # 1a. Collect from ROOT_IMAGES_DIR
    root_images_dir_abs_str = str(pathlib.Path(ROOT_IMAGES_DIR).resolve())
    if pathlib.Path(ROOT_IMAGES_DIR).exists():
        for root, _, filenames in os.walk(ROOT_IMAGES_DIR):
            for filename in filenames:
                filepath_str = os.path.join(root, filename)
                if get_file_type(filepath_str) == 'image':
                    image_processing_queue.append((str(pathlib.Path(filepath_str).resolve()), root_images_dir_abs_str))

    # 1b. Collect from TARGET_DIRECTORIES
    for target_dir_input_str in TARGET_DIRECTORIES:
        target_dir_abs_str = str(pathlib.Path(target_dir_input_str).resolve())
        # Populate dir_index_data for hierarchy
        current_p = pathlib.Path(target_dir_input_str) # Relative to repo root for dir_index_data keys
        while True:
            dir_index_data.setdefault(str(current_p), {'subdirs': set(), 'html_files': set()})
            if str(current_p.parent) == '.': break
            parent_str = str(current_p.parent)
            dir_index_data.setdefault(parent_str, {'subdirs': set(), 'html_files': set()})
            dir_index_data[parent_str]['subdirs'].add(current_p.name)
            current_p = current_p.parent
        if pathlib.Path(target_dir_input_str).parts: # Ensure top level of target_dir is added
             dir_index_data.setdefault(pathlib.Path(target_dir_input_str).parts[0], {'subdirs': set(), 'html_files': set()})


        for root, dirnames, filenames in os.walk(target_dir_input_str):
            current_dir_rel_repo = pathlib.Path(root)
            dir_index_data.setdefault(str(current_dir_rel_repo), {'subdirs': set(), 'html_files': set()})
            for dn in dirnames: dir_index_data[str(current_dir_rel_repo)]['subdirs'].add(dn)

            for filename in filenames:
                filepath_str = os.path.join(root, filename)
                filepath_abs_str = str(pathlib.Path(filepath_str).resolve())
                file_type = get_file_type(filepath_str)

                # Output path for HTML file, relative to BASE_OUTPUT_DIR, then resolved
                output_html_path_obj = base_output_path_obj / current_dir_rel_repo / filename

                if file_type == 'markdown':
                    markdown_processing_queue.append((filepath_abs_str, output_html_path_obj.with_suffix(".html")))
                elif file_type == 'code':
                    code_processing_queue.append((filepath_abs_str, output_html_path_obj.with_name(f"{filename}.html")))
                elif file_type == 'image':
                    image_processing_queue.append((filepath_abs_str, target_dir_abs_str))

    # --- Pass 2: Process Images ---
    print("\n--- Processing Images ---")
    for img_abs_path, base_dir_abs in image_processing_queue:
        process_image_file(img_abs_path, base_dir_abs)

    # --- Pass 3: Process Markdown ---
    print("\n--- Processing Markdown ---")
    for md_abs_path, html_out_path in markdown_processing_queue:
        html_filename = convert_markdown_to_html(md_abs_path, html_out_path)
        if html_filename: # Add to dir_index_data for the containing directory
            # Key for dir_index_data is relative to repo root
            html_container_dir_rel_repo = str(pathlib.Path(md_abs_path).parent)
            if html_container_dir_rel_repo in dir_index_data:
                 dir_index_data[html_container_dir_rel_repo]['html_files'].add(html_filename)


    # --- Pass 4: Process Code ---
    print("\n--- Processing Code ---")
    for code_abs_path, html_out_path in code_processing_queue:
        html_filename = process_code_file(code_abs_path, html_out_path)
        if html_filename:
            html_container_dir_rel_repo = str(pathlib.Path(code_abs_path).parent)
            if html_container_dir_rel_repo in dir_index_data:
                dir_index_data[html_container_dir_rel_repo]['html_files'].add(html_filename)

    # --- Pass 5: Generate Indexes ---
    print("\n--- Generating Indexes ---")
    for dir_path_str, data in dir_index_data.items():
        # dir_path_str is relative to repo root
        generate_index_html(dir_path_str, data['subdirs'], data['html_files'], BASE_OUTPUT_DIR)

    root_level_subdirs = set()
    for path_str in dir_index_data.keys():
        p = pathlib.Path(path_str)
        if str(p.parent) == '.' and p.name in [pathlib.Path(td).parts[0] for td in TARGET_DIRECTORIES if pathlib.Path(td).parts]:
            if path_str in dir_index_data:
                root_level_subdirs.add(p.name)

    generate_index_html("", sorted(list(root_level_subdirs)), [], BASE_OUTPUT_DIR)

    print("\nScript execution finished.")
