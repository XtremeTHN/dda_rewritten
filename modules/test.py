content = open('test_info','r').read().splitlines()
for x in content:
    split_symbol = x.find(":")
    if split_symbol == -1:
        raise SyntaxError(f"Error while parsing file: {x}, expected :")
    splited = [x[:split_symbol], x[split_symbol +1:]]
    if splited[0] == "Name":
        print(f"Name passed: {splited[1]}")
    if splited[0] == "Description":
        print(f"Description passed: {splited[1]}")
    if splited[0] == "Dependencies":
        print(f"Dependencies passed: {splited[1]}")
    if splited[0] == "Version":
        print(f"Version passed: {splited[1]}")