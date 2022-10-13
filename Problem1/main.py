# Rajesh Sharma, 1004, CEO
# Jordan Leon, 1012, Project Manager
# Mark Antony, 1006, CTO
# Divya Rajesh, 1013, software Engg
# Anvar Mohamed, 1017, Project Manager
# Rajesh Nair, 1103, Software Engg
# Najeem Ali, 1105, PRO
# Sony Rajesh, 1015, Project Manager
input_file = 'PS11Q1.txt'
prompt_file = 'promptsPS11Q1.txt'
output_file = 'outputPS11Q1.txt'


class Node:
    def __init__(self, x: list):
        self.data = x
        self.left = None
        self.right = None


def build_tree(node, data: list):
    # input_id is at 2nd position
    input_id = data[1]
    if node is None:
        return Node(data)

    if input_id < node.data[1]:
        node.left = build_tree(node.left, data)
    else:
        node.right = build_tree(node.right, data)

    return node


def process_inputs(input_str):
    current_input = []
    x = None
    if ',' in input_str:
        x = input_str.split(',')
        if len(x) == 3:
            current_input.append(x[0].strip())
            current_input.append(x[1].strip())
            current_input.append(x[2].strip())
        else:
            print('Invalid input string.')
    return current_input


def process_prompts(input_str):
    # Search ID: 1004
    current_prompt = []
    x = None
    if ':' in input_str:
        input_str = input_str.replace('Search', '')
        input_str = input_str.strip()
        x = input_str.split(':')
        if len(x) == 2:
            current_prompt.append(x[0].strip())
            current_prompt.append(x[1].strip())
        else:
            print('Invalid prompt string.')
    return current_prompt


def read_inputs(is_input=True, is_prompt=False):
    all_inputs = []
    f = None
    if is_input:
        f = open(input_file, "r")
    elif is_prompt:
        f = open(prompt_file, "r")
    for line in f.readlines():
        if is_input:
            temp = process_inputs(line)
        elif is_prompt:
            temp = process_prompts(line)
        if len(temp) > 0:
            all_inputs.append(temp)
    return all_inputs


traversed = dict()
counter = 0


# Inorder traversal
# If recording is set, we will record the traversal so that it can be used searching
def inorder(root, record=False):
    if root is not None:
        global traversed
        global counter

        if record:
            inorder(root.left, record)
            traversed[counter] = root.data
            counter = counter + 1
            # Traverse right
            inorder(root.right, record)
        else:
            # Traverse left
            inorder(root.left, record)
            # Traverse
            print_to_file(as_string(root.data))
            inorder(root.right, record)


def delete_from_tree():
    pass


# List as string. Mostly for printing purpose
def as_string(input_list):
    return ' , '.join(input_list)


def process_search_inputs(inp, search_type):
    out = None
    if len(inp) > 0:
        if search_type == 'Name':
            out = inp[0]
        elif search_type == 'ID':
            out = inp[1]
        elif search_type == 'Designation':
            out = inp[2]
        else:
            print('Invalid search type [{}]'.format(search_type))
    return out


# 9 Binary Tree Created with the employee details (from file
# abc_emp_dataPS11.txt”)
# ------------- Search by ID ---------------
# 1004 Rajesh Sharma
# 1005 not found
# 1006 Mark Antony
# 1009 Arun Kumar
# 1105 Najeem Ali
# -----------------------------------------------
# ------------- Search by Name: Rajesh -----------
# Rajesh Sharma
# Divya Rajesh
# Sony Rajesh
# Rajesh Nair
# -----------------------------------------------
# -----------List Employees by Designation: Project Manager -------------
# Jordan Leon, 1012
# Sony Rajesh, 1015
# Anvar Mohamed, 1017
# -----------------------------------------------

def search(node, search_type, search_str):
    out = []
    if not len(traversed) > 0:
        inorder(node, record=True)
    print('Search by [{}] for [{}]'.format(search_type, search_str))
    if len(traversed) > 0:
        for key in traversed.keys():
            current_inputs = traversed.get(key)
            current = process_search_inputs(current_inputs, search_type)
            if search_str.lower() in current.lower():
                out.append(current_inputs)
                # print('Name [{}]'.format(current_inputs[0]))

    if not len(out) > 0:
        out.append(['not found', 'not found', 'not found'])
    return out


def show_tree():
    pass


def entry():
    clear_output_file()
    inputs = read_inputs()
    prompts = read_inputs(is_input=False, is_prompt=True)
    node = None
    for data in inputs:
        node = build_tree(node, data)
    print_to_file('Listing the tree based on seniority')
    print_to_file('#####################')
    inorder(node)
    print_to_file('#####################')

    for prompt in prompts:
        # Format for prompt is list with 0 as type and 1 as value to search
        search_type = prompt[0]
        search_value = prompt[1]
        result = search(node, search_type=search_type, search_str=search_value)
        process_results(search_type, search_value, result)


def clear_output_file():
    import os
    try:
        os.remove(output_file)
    except IOError as e:
        print('Could not delete the output file')


def print_to_file(std_str):
    f = None
    try:
        # print('Writing {}'.format(std_str))
        f = open(output_file, 'a')
        print(std_str, file=f)

    except IOError as e:
        print('Could not write to output file')
    finally:
        if f is not None:
            f.close()


def process_results(search_type, search_value, results):
    print_to_file('Search by field {} for {}'.format(search_type, search_value))
    print_to_file("###########################")
    for result in results:
        if search_type == 'ID':
            print_to_file('{} {}'.format(result[1], result[0]))
        elif search_type == 'Name':
            print_to_file('{}'.format(result[0]))
        elif search_type == 'Designation':
            print_to_file('{}, {}'.format(result[0], result[1]))
    print_to_file("###########################")


# print(read_inputs(is_input=False, is_prompt=True))
entry()
