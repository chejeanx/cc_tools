"""
Methods for encoding and decoding Chip's Challenge (CC) data to and from JSON files
Created for the class Programming for Game Designers
"""
import json
import sys

import cc_data
import cc_dat_utils

def make_ccDataFile_from_json(json_data):
    myCCDataFile = cc_data.CCDataFile()
    for json_game in json_data:
        level_number = json_game["level_number"]
        time = json_game["time"]
        num_chips = json_game["num_chips"]
        upper_layer = json_game["upper_layer"]
        lower_layer = json_game["lower_layer"]
        optional_fields = json_game["optional_fields"]

        myLevel = cc_data.CCLevel()
        myLevel.level_number = level_number
        myLevel.time = time
        myLevel.num_chips = num_chips
        myLevel.upper_layer = upper_layer
        myLevel.lower_layer = lower_layer

        real_optional_fields = []
        for opt in optional_fields:
            if opt["type"] == 3:
                real_optional_fields.append(cc_data.CCMapTitleField(opt["title"]))

            elif opt["type"] == 4:
                traps = opt["traps"]
                real_traps = []
                for trap in traps:
                    x = trap["button_coord"]
                    y = trap["trap_coord"]
                    real_traps.append(cc_data.CCTrapControl(x[0],x[1],y[0],y[1]))
                real_optional_fields.append(cc_data.CCTrapControlsField(real_traps))

            elif opt["type"] == 5:
                machines = opt["machines"]
                real_machines = []
                for machine in machines:
                    x = machine["button_coord"]
                    y = machine["machine_coord"]
                    real_machines.append(cc_data.CCCloningMachineControl(x[0],x[1],y[0],y[1]))
                real_optional_fields.append(cc_data.CCCloningMachineControlsField(real_machines))

            elif opt["type"] == 6:
                real_optional_fields.append(cc_data.CCEncodedPasswordField(opt["password"]))

            elif opt["type"] == 7:
                real_optional_fields.append(cc_data.CCMapHintField(opt["hint"]))

            elif opt["type"] == 10:
                monsters = opt["monsters"]
                real_monsters = []
                for monster in monsters:
                    x = cc_data.CCCoordinate(monster[0], monster[1])
                    real_monsters.append(x)
                real_optional_fields.append(cc_data.CCMonsterMovementField(real_monsters))

        myLevel.optional_fields = real_optional_fields

        myCCDataFile.add_level(myLevel)

        print(myCCDataFile)

    return myCCDataFile


# Handling command line arguments
#  Note: sys.argv is a list of strings that contains each command line argument
#        The first element in the list is always the name of the python file being run
# Command line format: <input json filename> <output dat filename>

default_input_json_file = "data/pfgd_data.json"
default_output_dat_file = "data/pfgd_data.dat"

if len(sys.argv) == 3:
    input_json_file = sys.argv[1]
    output_dat_file = sys.argv[2]
    print("Using command line args:", input_json_file, output_dat_file)
else:
    input_json_file = default_input_json_file
    output_dat_file = default_output_dat_file
    print("Unknown command line options. Using default values:", input_json_file, output_dat_file)

# Reading the JSON data in from the input file
json_reader = open("data/pfgd_data.json", "r")
json_data = json.load(json_reader)
json_reader.close() #Close the file now that we're done using it

# Build the Python data structure from the JSON data
cc_levels = make_ccDataFile_from_json(json_data)

# Write data to DAT file
print("Writing data to output file", output_dat_file)
cc_dat_utils.write_cc_data_to_dat(cc_levels,output_dat_file)

