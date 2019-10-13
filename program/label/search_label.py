def element_in_label_PY():

    label = []
    number_label = []
    increment = ""
 
    with open("label/label.py", "r") as file:
        for i in file:
            for j in i:
                if j in (";"):
                    label.append(increment)
                    increment = ""

                if j not in (",", " ", "\n"):
                    try:
                        j = int(j)
                        if j == int(j):
                            number_label.append(j)
                    except:
                        increment += j

    return number_label, label
