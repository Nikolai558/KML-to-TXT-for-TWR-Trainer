import sys

xmlFilePath = ""
outFilePath = ""
roundCoords = False

if __name__ == '__main__':
    if len(sys.argv) == 2:
        xmlFilePath = sys.argv[1]
        outFilePath = f"{sys.argv[1].split('.')[0]}.txt"

    else:
        print("Your arguments are invalid. Try again.")
        print("Correct format is:\n"
              "\tKML_Coord_Extractor\t{Diagram_Name}\t{Diagram_File_Path}\n")

    thisDict = {}

    with open(xmlFilePath, "r") as inFile:
        print(f"Reading File:\n\t{xmlFilePath}")

        lines = inFile.readlines()

        grabCoords = False
        inPlaceMark = False

        title = ""
        coords = []
        for line in lines:
            if "<Placemark>" in line:
                inPlaceMark = True
            elif "</Placemark>" in line:
                inPlaceMark = False

            if inPlaceMark:
                if "<name>" in line:
                    title = line.replace("<name>", "")
                    title = title.replace("</name>", "")
                    title = title.replace("\t", "")
                    title = title.replace("\n", "")

                if grabCoords:
                    line = line.replace("\t", "")
                    line = line.replace("\n", "")
                    coords = line.split(",0 ")

                if "<coordinates>" in line:
                    grabCoords = True
                    continue
                else:
                    grabCoords = False
            else:
                continue

            if title != "" and len(coords) >= 1:
                try:
                    thisDict[title] = coords
                except KeyError:
                    print(f"There is already a Key with data in this Dictionary! Please fix name!\n{title}")

    with open(outFilePath, "w") as outFile:
        print(f"Starting to write Output File:\n\t{outFilePath}")
        for title, coordinate in thisDict.items():
            outFile.write(f"\n[{title}]\n")

            for indvCoord in coordinate:
                if "," in indvCoord:
                    lon = indvCoord.split(",")[0]
                    lat = indvCoord.split(",")[1]

                    if roundCoords:
                        lon = str(round(float(lon), 5))
                        lat = str(round(float(lat), 5))

                    outFile.write(f"{lat} {lon}\n")

    print("Complete")
