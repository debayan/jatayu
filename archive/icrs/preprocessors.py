import re

EMAIL = re.compile(r'[\S]+@[^@]+\.[\w]+')

def recursively_remove_email(s, emails=None):
    """
    returns (string_replaced_with_EMAIL, emails)
    """
    if not emails:
        emails = []
    m = EMAIL.search(s)
    if m:
        emails.append(m.group(0))
    else:
        return (s, emails)
    return recursively_remove_email(re.sub(EMAIL, "EMAIL", s, 1), emails)
