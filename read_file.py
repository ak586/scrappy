def read_file(file_name):
    file_path='./scrapped_data/'+file_name
    text=''
    with open(file_path, 'r') as f:
        text=f.read()
    return text

        