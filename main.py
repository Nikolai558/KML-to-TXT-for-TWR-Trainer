import sys

debug = True

inputFilePath = "C:\\PoconoDocuments\\Downloads\\KSLC-UPDATE-01.txt"
outputFilePath = "C:\\PoconoDocuments\\Downloads\\KSLC-UPDATE-01.kml"
roundCoords = True
kmlPlaceMarkers = {}
isTxtFile = None


def txtToKml():
    # --- CONFIG ---
    LINECOLOR = ""

    # --- Tower Trainer TXT Components ---
    AirportIcao = "TESTING"
    Parking = {}
    Runway = {}
    Taxiway = {}

    title = ""
    flag = ""

    with open(inputFilePath, "r") as inFile:
        print(f"Reading File:\n\t{inputFilePath}")
        inFileLines = inFile.readlines()

        for line in inFileLines:
            line = line.replace("\n", "")
            line = line.replace("\t", "")

            if "icao=" in line:
                AirportIcao = line.split("icao=")[1]
                continue

            if "[" in line:
                title = line.replace("[", "")
                title = title.replace("]", "")

                if "PARKING" in title:
                    Parking[title] = []
                    flag = "P"
                elif "RUNWAY" in title:
                    Runway[title] = []
                    flag = "R"
                elif "TAXIWAY" in title:
                    Taxiway[title] = []
                    flag = "T"
                else:
                    title = ""
                    flag = ""
                    print("Something went wrong with creating the Dictionaries.")
                continue

            if title != "" and flag != "":
                if line == "":
                    continue

                if flag == "P":
                    Parking[title].append(line)
                elif flag == "R":
                    Runway[title].append(line)
                elif flag == "T":
                    Taxiway[title].append(line)
    with open(outputFilePath, "w") as outFile:
        print(f"Starting to write Output File:\n\t{outputFilePath}")
        allDict = [Runway, Parking, Taxiway]

        outFile.write('\t<Folder>\n')
        outFile.write(f'\t\t<name>{AirportIcao}</name>\n')
        outFile.write('\t\t<open>1</open>\n')

        count = 1
        for dict in allDict:
            outFile.write('\t\t<Folder>\n')
            outFile.write(f'\t\t\t<name>Folder-{count}</name>\n')

            for name, coord in dict.items():
                outFile.write('\t\t\t<Placemark>\n')
                outFile.write(f'\t\t\t\t<name>{name.replace("/", "-")}</name>\n')
                outFile.write('\t\t\t\t<styleUrl>#msn_ylw-pushpin10</styleUrl>\n')
                outFile.write('\t\t\t\t<LineString>\n')
                outFile.write('\t\t\t\t\t<tessellate>1</tessellate>\n')
                outFile.write('\t\t\t\t\t<coordinates>\n')

                tempString = "\t\t\t\t\t\t"
                for indvCoord in coord:
                    if len(indvCoord.split(" ")) == 2:
                        tempString += f'{indvCoord.split(" ")[1]},{indvCoord.split(" ")[0]},0 '
                tempString += "\n"
                outFile.write(tempString)

                outFile.write('\t\t\t\t\t</coordinates>\n')
                outFile.write('\t\t\t\t</LineString>\n')
                outFile.write('\t\t\t</Placemark>\n')

            outFile.write('\t\t</Folder>\n')
            count += 1

        outFile.write('\t</Folder>\n')
    print("Complete")


def kmlToTxt():
    with open(inputFilePath, "r") as inFile:
        print(f"Reading File:\n\t{inputFilePath}")
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
                    kmlPlaceMarkers[title] = coords
                except KeyError:
                    print(f"There is already a Key with data in this Dictionary! Please fix name!\n{title}")

    with open(outputFilePath, "w") as outFile:
        print(f"Starting to write Output File:\n\t{outputFilePath}")
        for title, coordinate in kmlPlaceMarkers.items():
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


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1].split('.')[1] == "kml":
            inputFilePath = sys.argv[1]
            outputFilePath = f"{sys.argv[1].split('.')[0]}.txt"
            isTxtFile = False
        elif sys.argv[1].split('.')[1] == "txt":
            inputFilePath = sys.argv[1]
            outputFilePath = f"{sys.argv[1].split('.')[0]}.kml"
            isTxtFile = True
        else:
            print(f"I can't do anything with this file Extension: .{sys.argv[1].split('.')[1]}")
            exit(401)
    elif len(sys.argv) == 3:
        if sys.argv[1].split('.')[1] == "kml":
            inputFilePath = sys.argv[1]
            outputFilePath = f"{sys.argv[1].split('.')[0]}.txt"
            isTxtFile = False
        elif sys.argv[1].split('.')[1] == "txt":
            inputFilePath = sys.argv[1]
            outputFilePath = f"{sys.argv[1].split('.')[0]}.kml"
            isTxtFile = True
        else:
            print(f"I can't do anything with this file Extension: .{sys.argv[1].split('.')[1]}")
            exit(402)

        if str(sys.argv[2]).lower() == "y":
            roundCoords = True
        elif str(sys.argv[2]).lower() == "n":
            roundCoords = False
        else:
            print(f"{sys.argv[2]}, is not a valid option for Rounding Coordinates. Please try again with [Y/N]")
            exit(403)
    else:
        print("Your arguments are invalid. Try again.")
        print("Correct format is:\n"
              "\t{EXE FILE PATH}\t{KML FILE PATH}\t{OPTIONAL: ROUND COORDINATES [Y/N]}\n")
        exit(404)

    if isTxtFile == True:
        txtToKml()
    elif isTxtFile == False:
        kmlToTxt()
    else:
        print("Something Went Wrong!")
        exit(405)
