def parse_line(line_input: str, dic: dict):
    line_cleared = line_input.replace(' ', '')
    if line_cleared[0] != '#':
        line_cleared, typ = line_cleared.split('@')
        key, value = line_cleared.split(':')
        if typ == 'INT':
            value = int(value)
        elif typ == 'FLOAT':
            value = float(value)
        elif typ == 'INTERVAL':
            value = [float(i) for i in value.split(',')]
        dic[key] = value



