import sys

if __name__ == '__main__':
    if len(sys.argv)<2:
        print('Usage: python sterile.py <filename>')
    else:
        try:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                content = f.read()
            content = content.replace('\t', '  ')
            ascii_content = content.encode('ascii', 'ignore').decode('ascii')
            output_path = sys.argv[2] or f'sterile_{sys.argv[1]}'
            with open(output_path, 'w', encoding='ascii') as f:
                f.write(ascii_content)
            print(f'Success: {output_path}')
        except Exception as e:
            print(f'Error: {e}')