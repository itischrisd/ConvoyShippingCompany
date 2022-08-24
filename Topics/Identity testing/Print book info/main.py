def print_book_info(title, author=None, year=None):
    print(f'"{title}"', end='')
    if author is not None or year is not None:
        print(' was written ', end='')
    if author is not None:
        print(f'by {author}', end=' ')
    if year is not None:
        print(f'in {year}')
    pass