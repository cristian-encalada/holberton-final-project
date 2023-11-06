import json
import requests

def is_int(text):
    """
    Converts a string representation of a number into a positive integer. 
    If the input is not a valid positive integer, it returns None.
    """
    try:
        converted_number = int(text)
        if converted_number < 0:
            converted_number = 0
    except (ValueError, TypeError):
        converted_number = None
    return converted_number
        

def tex_none(text, split):
    """
    Separates multiple names to form a list. If the input text is None, it returns None.
    """
    if text is None:
        return None
    separated_names = text.split(split)
    return separated_names


def chek_int(text):
    """
    Extracts a list of string numbers (",") and validates whether they are indeed integers.
    If a value is not a valid integer, it is replaced with None in the resulting list.
    """
    numbers_list = tex_none(text, ',')
    if numbers_list:
        validated_numbers = []
        for number in numbers_list:
            validated_number = is_int(number)
            validated_numbers.append(validated_number)
        numbers_list = validated_numbers
    return numbers_list


def sorting(text):
    """
    Preprocesses sorting criteria for a list of columns and their corresponding orders (ascending 1 or descending -1).
    Returns a dictionary with the column names as keys and the corresponding order as values.
    If the input values are not valid, the sorting criteria for those values are not included in the dictionary.
    """
    column_order_pairs = tex_none(text, ',')
    sorting_criteria_dict = {}
    if column_order_pairs:
        for pair in column_order_pairs:
            pair_elements = pair.split(':')
            if len(pair_elements) >= 2:
                order = is_int(pair_elements[1])
                if order is not None:
                    if order > 1:
                        order = 1 # acendente (de menor a mayor)
                    if order == 0:
                        order = -1 # desendente (de mayor a menor)
                    sorting_criteria_dict[pair_elements[0]] = order
    return sorting_criteria_dict

def cambio_call():
    """
    Retrieves the value of the currency conversion rate from a remote JSON file.
    
    This function makes an HTTP request to the given URL, which contains the conversion rate between two currencies,
    and retrieves the value of the currency conversion rate. If the request is successful and the JSON data is parsed,
    the function returns the value of the currency conversion rate. If there are any errors during the request or JSON
    parsing, the function will raise an appropriate error.

    Returns:
    float: The value of the currency conversion rate from the remote JSON file.
    """
    url = "https://raw.githubusercontent.com/cristian-encalada/Alquivago/main/data/cambio.json"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        data = response.json()  # Parse the JSON response
        return data["rate"]
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error while making the HTTP request: {str(e)}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Error while parsing JSON data: {str(e)}")
