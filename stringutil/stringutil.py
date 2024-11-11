# Bản đồ ký tự tiếng Việt có dấu sang không dấu
vietnamese_tones = {
    'á': 'a', 'à': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a', 'ă': 'a', 'ắ': 'a', 'ằ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
    'â': 'a', 'ấ': 'a', 'ầ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
    'é': 'e', 'è': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e', 'ê': 'e', 'ế': 'e', 'ề': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
    'í': 'i', 'ì': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
    'ó': 'o', 'ò': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o', 'ô': 'o', 'ố': 'o', 'ồ': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
    'ơ': 'o', 'ớ': 'o', 'ờ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
    'ú': 'u', 'ù': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u', 'ư': 'u', 'ứ': 'u', 'ừ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
    'ý': 'y', 'ỳ': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y',
    'Á': 'A', 'À': 'A', 'Ả': 'A', 'Ã': 'A', 'Ạ': 'A', 'Ă': 'A', 'Ắ': 'A', 'Ằ': 'A', 'Ẳ': 'A', 'Ẵ': 'A', 'Ặ': 'A',
    'Â': 'A', 'Ấ': 'A', 'Ầ': 'A', 'Ẩ': 'A', 'Ẫ': 'A', 'Ậ': 'A',
    'É': 'E', 'È': 'E', 'Ẻ': 'E', 'Ẽ': 'E', 'Ẹ': 'E', 'Ê': 'E', 'Ế': 'E', 'Ề': 'E', 'Ể': 'E', 'Ễ': 'E', 'Ệ': 'E',
    'Í': 'I', 'Ì': 'I', 'Ỉ': 'I', 'Ĩ': 'I', 'Ị': 'I',
    'Ó': 'O', 'Ò': 'O', 'Ỏ': 'O', 'Õ': 'O', 'Ọ': 'O', 'Ô': 'O', 'Ố': 'O', 'Ồ': 'O', 'Ổ': 'O', 'Ỗ': 'O', 'Ộ': 'O',
    'Ơ': 'O', 'Ớ': 'O', 'Ờ': 'O', 'Ở': 'O', 'Ỡ': 'O', 'Ợ': 'O',
    'Ú': 'U', 'Ù': 'U', 'Ủ': 'U', 'Ũ': 'U', 'Ụ': 'U', 'Ư': 'U', 'Ứ': 'U', 'Ừ': 'U', 'Ử': 'U', 'Ữ': 'U', 'Ự': 'U',
    'Ý': 'Y', 'Ỳ': 'Y', 'Ỷ': 'Y', 'Ỹ': 'Y', 'Ỵ': 'Y', 'đ': 'd', 'Đ': 'D'
}
delimiters = [',', '.', '-', '_', '+']

# Bản đồ chuẩn hóa và alias cho các số phường
number_ward_normalize_map = {
    "01": "1", "02": "2", "03": "3", "04": "4", "05": "5", "07": "7", "08": "8", "09": "9"
}

number_ward_alias_map = {
    "01": "1", "02": "2", "03": "3", "04": "4", "05": "5", "07": "7", "08": "8", "09": "9",
    "1": "01", "2": "02", "3": "03", "4": "04", "5": "05", "6": "06", "7": "07", "8": "08", "9": "09"
}

# Hàm loại bỏ dấu tiếng Việt
def remove_vietnamese_accents(input_text):
    output = ''.join(vietnamese_tones.get(char, char) for char in input_text)
    return output

# Hàm loại bỏ ký tự đặc biệt
def remove_delimiters(name):
    for delimiter in delimiters:
        name = name.replace(delimiter, "")
    return name

# Hàm loại bỏ tiền tố của phường
def remove_ward_prefix(name):
    prefixes = ["Phường ", "Xã ", "Thị trấn "]
    for prefix in prefixes:
        if name.startswith(prefix):
            return name[len(prefix):]
    return name

# Hàm loại bỏ tiền tố của quận/huyện
def remove_district_prefix(name):
    prefixes = ["Quận ", "Huyện ", "Thị xã ", "Thành phố "]
    for prefix in prefixes:
        if name.startswith(prefix):
            return name[len(prefix):]
    return name

# Hàm loại bỏ tiền tố của tỉnh/thành phố
def remove_province_prefix(name):
    prefixes = ["Tỉnh ", "Thành phố "]
    for prefix in prefixes:
        if name.startswith(prefix):
            return name[len(prefix):]
    return name

# Chuẩn hóa địa chỉ bằng cách loại bỏ dấu và chuyển về chữ thường
def standardize_location(address):
    address = remove_vietnamese_accents(address)
    address = address.lower()
    return address

# Kiểm tra chuỗi có phải là số nguyên không
def is_integer(string):
    return string.isdigit()

# Hàm đảo ngược chuỗi
def reverse_string(s):
    return s[::-1]