#!/usr/bin/env python3
import re
import shutil
from datetime import datetime
from html import unescape
from pathlib import Path

from bs4 import BeautifulSoup, Comment
from markdownify import markdownify as md

ROOT = Path('/workspaces/ruby')
SOURCE_REPO = ROOT / 'davamix.github.io'
SOURCE_POSTS = SOURCE_REPO / 'posts'
SOURCE_IMAGES = SOURCE_REPO / 'images'
TARGET_BLOG = ROOT / 'blog'
TARGET_POSTS = TARGET_BLOG / '_posts'
TARGET_IMAGES = TARGET_BLOG / 'assets' / 'images'

METADATA_BY_SOURCE = {
    'asp-net-core-2-with-https.html': {
        'categories': ['dotnet', 'web'],
        'tags': ['asp-net-core', 'https', 'ssl'],
    },
    'install-net-3-5-on-Windows-10.html': {
        'categories': ['dotnet', 'sysadmin'],
        'tags': ['dotnet-framework', 'windows'],
    },
    'create-local-nuget-server.html': {
        'categories': ['dotnet', 'backend'],
        'tags': ['nuget', 'package-management'],
    },
    'save-video-frames-as-images-with-opencv.html': {
        'categories': ['python', 'computer-vision'],
        'tags': ['opencv', 'image-processing', 'video'],
    },
    'detecting-my-cats-with-Detectron2.html': {
        'categories': ['python', 'ml'],
        'tags': ['detectron2', 'object-detection', 'ml'],
    },
    'github-actions-build-xamarin-forms-poject-and-create-the-apk.html': {
        'categories': ['devops', 'mobile'],
        'tags': ['github-actions', 'xamarin', 'ci-cd'],
    },
}


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r'[^a-z0-9]+', '-', value)
    return re.sub(r'-+', '-', value).strip('-')


def normalize_ws(text: str) -> str:
    text = text.replace('\u00a0', ' ')
    text = re.sub(r'[ \t]+\n', '\n', text)
    return text


def rewrite_image_links(markdown: str) -> str:
    markdown = re.sub(
        r'\((?:\.\./images/|/images/|images/)([^)]+)\)',
        lambda m: f'(/assets/images/{m.group(1)})',
        markdown,
    )
    return markdown


def clean_code_block(code_div) -> str:
    html = code_div.decode_contents()
    html = re.sub(r'(?is)</?code[^>]*>', '', html)
    html = re.sub(r'(?i)<br\s*/?>', '\n', html)
    html = html.replace('&nbsp;', ' ')
    html = unescape(html)
    text = BeautifulSoup(html, 'html.parser').get_text('')
    lines = text.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    lines = [line.rstrip() for line in lines]
    while lines and lines[0] == '':
        lines.pop(0)
    while lines and lines[-1] == '':
        lines.pop()
    body = '\n'.join(lines)
    return f"```plaintext\n{body}\n```" if body else '```plaintext\n```'


def note_to_markdown(note_div) -> str:
    inner = ''.join(str(c) for c in note_div.contents)
    content = md(inner, heading_style='ATX').strip()
    content = rewrite_image_links(content)
    lines = content.split('\n') if content else ['']
    return '\n'.join('> ' + line if line.strip() else '>' for line in lines)


def generic_to_markdown(tag) -> str:
    converted = md(str(tag), heading_style='ATX').strip()
    converted = rewrite_image_links(converted)
    return converted


def extract_title_date(post_div):
    title_div = post_div.find('div', class_='title')
    if not title_div:
        raise ValueError('Missing title div')

    h1 = title_div.find('h1')
    date_span = title_div.find('span', class_=lambda c: c and 'date' in c)
    if not h1 or not date_span:
        raise ValueError('Missing title or date')

    title = h1.get_text(strip=True)
    raw_date = date_span.get_text(strip=True)
    parsed_date = datetime.strptime(raw_date, '%d-%m-%Y').strftime('%Y-%m-%d 00:00:00 +0000')
    file_date = datetime.strptime(raw_date, '%d-%m-%Y').strftime('%Y-%m-%d')
    return title, parsed_date, file_date


def first_paragraph_description(blocks):
    for block in blocks:
        candidate = re.sub(r'```[\s\S]*?```', '', block).strip()
        candidate = re.sub(r'^>\s?', '', candidate, flags=re.MULTILINE).strip()
        if not candidate:
            continue

        first_line = candidate.split('\n')[0].strip()
        first_line = re.sub(r'[#*_`\[\]]', '', first_line).strip()
        if not first_line:
            continue

        if '.' in first_line:
            sentence = first_line.split('.', 1)[0].strip() + '.'
        else:
            sentence = first_line[:155].strip()
            if len(first_line) > 155:
                sentence += '...'
        return sentence.replace('"', "'")
    return 'Migrated post from the old blog.'


def insert_excerpt_separator(markdown_body: str) -> str:
    parts = [p for p in markdown_body.split('\n\n') if p.strip()]
    if not parts:
        return markdown_body
    if len(parts) == 1:
        return parts[0] + '\n\n<!--more-->'
    return parts[0] + '\n\n<!--more-->\n\n' + '\n\n'.join(parts[1:])


def convert_post(source_file: Path):
    html = source_file.read_text(encoding='utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    # Ignore commented HTML blocks so commented-out images don't become markdown content.
    for comment in soup.find_all(string=lambda s: isinstance(s, Comment)):
        comment.extract()

    post_div = soup.find('div', class_='post')
    if not post_div:
        raise ValueError(f'Missing post container: {source_file.name}')

    title, jekyll_date, file_date = extract_title_date(post_div)

    blocks = []
    for child in post_div.children:
        if isinstance(child, str):
            if child.strip():
                blocks.append(child.strip())
            continue

        classes = child.get('class') or []
        if child.name == 'div' and 'title' in classes:
            continue

        if child.name == 'div' and 'code' in classes:
            blocks.append(clean_code_block(child))
            continue

        if child.name == 'div' and 'note' in classes:
            blocks.append(note_to_markdown(child))
            continue

        if child.name == 'div' and 'post-references-section' in classes:
            for sub in child.children:
                if isinstance(sub, str):
                    if sub.strip():
                        blocks.append(sub.strip())
                    continue
                out = generic_to_markdown(sub)
                if out:
                    blocks.append(out)
            continue

        out = generic_to_markdown(child)
        if out:
            blocks.append(out)

    blocks = [normalize_ws(b).strip() for b in blocks if b and b.strip()]
    markdown_body = '\n\n'.join(blocks)
    markdown_body = re.sub(r'\n{3,}', '\n\n', markdown_body).strip()
    markdown_body = insert_excerpt_separator(markdown_body)

    description = first_paragraph_description(blocks)

    metadata = METADATA_BY_SOURCE.get(source_file.name)
    if not metadata:
        raise ValueError(f'Missing category/tag mapping for {source_file.name}')

    categories = ', '.join(metadata['categories'])
    tags = ', '.join(metadata['tags'])

    front_matter = (
        '---\n'
        'layout: post\n'
        f'title: "{title.replace("\"", "'")}"\n'
        f'date: {jekyll_date}\n'
        f'categories: [{categories}]\n'
        f'tags: [{tags}]\n'
        f'description: "{description}"\n'
        'excerpt_separator: <!--more-->\n'
        '---\n\n'
    )

    filename = f"{file_date}-{slugify(title)}.md"
    output_path = TARGET_POSTS / filename
    output_path.write_text(front_matter + markdown_body + '\n', encoding='utf-8')
    return output_path


def copy_images():
    TARGET_IMAGES.parent.mkdir(parents=True, exist_ok=True)
    if TARGET_IMAGES.exists():
        shutil.rmtree(TARGET_IMAGES)
    shutil.copytree(SOURCE_IMAGES, TARGET_IMAGES)


def main():
    if not SOURCE_POSTS.exists():
        raise SystemExit(f'Source posts directory not found: {SOURCE_POSTS}')

    TARGET_POSTS.mkdir(parents=True, exist_ok=True)
    copy_images()

    outputs = []
    for post_file in sorted(SOURCE_POSTS.glob('*.html')):
        outputs.append(convert_post(post_file))

    print('Migrated posts:')
    for path in outputs:
        print(f'- {path}')
    print(f'Copied images into: {TARGET_IMAGES}')


if __name__ == '__main__':
    main()
