def progress_bar(current, total, length=8, fill="█", show_percent=True):
    percent = int(100 * (current / float(total)))
    filled_length = int(length * current // total)
    bar = fill * filled_length + "-" * (length - filled_length)

    if show_percent:
        return f"|{bar}| {percent}%"
    else:
        return f"|{bar}| {current}"

    if current == total:
        print()
