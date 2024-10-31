def read_config(file_path):
    """Читает конфигурационный файл и возвращает его содержимое строками."""
    with open(file_path, 'r') as file:
        return file.readlines()


def write_config(file_path, lines):
    """Записывает измененные строки обратно в файл конфигурации."""
    with open(file_path, 'w') as file:
        file.writelines(lines)


def read_zones_to_remove(file_path):
    """Читает файл с зонами, которые нужно удалить, и возвращает список зон."""
    with open(file_path, 'r') as file:
        # Читаем и удаляем лишние пробелы и символы новой строки
        return [line.strip() for line in file.readlines() if line.strip()]


def find_zone_blocks(config_lines):
    """Находит все блоки зон в конфигурации."""
    blocks = []
    current_block = []
    inside_block = False

    for line in config_lines:
        if line.strip().startswith('zone'):
            inside_block = True
            current_block = [line]  # Начало нового блока
        elif inside_block:
            current_block.append(line)
            if '};' in line:  # Конец блока зоны
                blocks.append(current_block)
                inside_block = False

    return blocks


def remove_zones(config_lines, zones_to_remove):
    """Удаляет блоки с зонами, если они совпадают с зонами из списка zones_to_remove."""
    blocks = find_zone_blocks(config_lines)
    zones_to_remove_set = set(zones_to_remove)

    # Определяем блоки, которые нужно оставить
    filtered_lines = []
    for block in blocks:
        zone_name = block[0].split('"')[1]  # Извлекаем имя зоны
        if zone_name not in zones_to_remove_set:
            filtered_lines.extend(block)

    return filtered_lines


def main(config_file, zones_file):
    # 1. Чтение исходного файла конфигурации
    config_lines = read_config(config_file)

    # 2. Чтение файла с зонами для удаления
    zones_to_remove = read_zones_to_remove(zones_file)

    # 3. Удаление нужных блоков
    updated_config_lines = remove_zones(config_lines, zones_to_remove)

    # 4. Запись нового конфига в файл
    write_config(config_file, updated_config_lines)
    print(f"Зоны {zones_to_remove} были удалены из конфигурации.")

# Пример использования:
config_file_path = 'master.include'
zones_to_remove_list = 'del_zone_2.txt'

main(config_file_path, zones_to_remove_list)