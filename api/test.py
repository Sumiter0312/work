import re
username = 'dsdsdsadasd'
pwd = '123add'
username_regex = r"[a-zA-Z]{10,}"
pwd_regex = r"(?=.*[a-z])(?=.*[A-Z])(?=.*[$@$!%*?&.])[A-Za-z\d]{1,6}"

user_match = re.findall(username_regex,username)
pwd_match = re.findall(pwd_regex,pwd)


print(user_match,pwd_match)