def declension_token(amount: int) -> str:
    values = (
        'токен',
        'токена',
        'токенов',
    )
    if amount % 10 == 1 and amount % 100 != 11:
        return values[0]
    elif amount % 10 in (2, 3, 4) and amount % 100 not in (12, 13, 14):
        return values[1]
    else:
        return values[2]