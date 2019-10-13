def element_to_detection(label, detection):
    with open("label.py", "a") as file:
        row = str(label) + "," + str(detection) + ";\n"
        file.write(str(row))
