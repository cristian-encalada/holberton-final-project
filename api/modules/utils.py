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
        

def tex_none(text):
    """
    Separates multiple names to form a list. If the input text is None, it returns None.
    """
    if text is None:
        return None
    separated_names = [element for element in text.split(',') if element != ""]
    return separated_names


def chek_int(text):
    """
    Extracts a list of string numbers (",") and validates whether they are indeed integers.
    If a value is not a valid integer, it is replaced with None in the resulting list.
    """
    numbers_list = tex_none(text)
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
    column_order_pairs = tex_none(text)
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


def conversion():
    """
    Retrieves the currency conversion rate between two currencies.
    In this case, the function fetches the conversion rate between USD and UYU.
    If the API call fails, it returns a default value of 40 as a sample conversion rate.
    """
    access_key = '108becf3bf3c99a76d9548282aa88dba51012e8b'
    base_currency = 'USD'
    target_currency = 'UYU'

    url = f'https://api.getgeoapi.com/v2/currency/convert?api_key={access_key}&from={base_currency}&to={target_currency}&amount=1&format=json'
    response = requests.get(url)

    if response.status_code == 200:
        conversion_data = response.json()
        if conversion_data['status'] == 'success':
            converted_value = float(conversion_data['rates']['UYU']['rate'])
            return converted_value
    print("No more API queries for conversion. Sample value: 40")
    return 40
    # return None
