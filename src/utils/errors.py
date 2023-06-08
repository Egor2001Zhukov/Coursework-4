class FewParamError(Exception):
    def __init__(self, *args, **kwargs):
        self.message = args[0] if args else "Слишком мало значений"

    def __str__(self):
        return self.message


class ValueInputError(Exception):
    def __init__(self, *args, **kwargs):
        self.message = args[0] if args else "Не то значение"

    def __str__(self):
        return self.message


def is_any_pos_number_to(args: str, from_: int = 0, to: int = 0):
    if args.isdigit():
        args = int(args)
        if to:
            if from_ < args < to:
                return args
            else:
                raise ValueInputError
        elif args > from_:
            return args
        else:
            raise ValueInputError
    else:
        raise ValueInputError


def is_0_or_1(args: str):
    if args.isdigit():
        args = int(args)
        if args in [0, 1]:
            return args
        else:
            raise ValueInputError
    else:
        raise ValueInputError


def is_list_indexes(args: str, len_of_massive: int):
    list_return = []
    list_ = args.split(", ")
    for x in list_:
        if not x.isdigit():
            raise ValueInputError
        elif 0 >= int(x) > len_of_massive:
            raise ValueInputError
        else:
            list_return.append(x)
    return list_return


