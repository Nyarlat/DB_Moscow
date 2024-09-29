def flatten_hierarchy(hierarchy, parent_key=''):
    result = []

    for key, value in hierarchy.items():
        # склейка текущего уровня
        new_key = f"{parent_key}: {key}" if parent_key else key

        if isinstance(value, dict) and value:  # если это словарь, идем дальше
            result.extend(flatten_hierarchy(value, new_key))
        elif isinstance(value, list) and value:  # если это список, добавляем все элементы списка
            for item in value:
                result.append(f"{new_key}:{item}")
        else:  # если это конец пути (пустой словарь или список)
            result.append(new_key)

    return result