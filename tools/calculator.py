from langchain_core.tools import tool


@tool
def calculator(
    first_num: float,
    second_num: float,
    operation: str
):
    """
    Perform basic arithmetic.
    operation:add,sub,mul,div

    """

    if operation == "add":
        return first_num + second_num

    elif operation == "sub":
        return first_num - second_num

    elif operation == "mul":
        return first_num * second_num

    elif operation == "div":

        if second_num == 0:
            return "Division by zero."

        return first_num / second_num

    return "Invalid operation."