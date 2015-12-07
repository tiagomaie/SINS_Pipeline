import os.path

'''
Automatically creates the necessary files with the necessary data for SinsSampler to run
Currently I only tested it with a single autosome and a single layer. Need to run more tests in the future
'''


def main(simulation_name):
    path_to_sins_input_folder = None
    name_of_sins_project = None
    address_of_input_folder = None
    number_of_layers = None
    number_of_autosomes_line = None
    type_of_chromosome_x = None
    type_of_chromosome_y = None
    type_of_chromosome_mt = None
    type_of_chromosome_a = None
    recording_starts_at_gen = None

    with open("./Input_SINS_Pipeline.par", 'r') as inF:
        for line in inF:
            if 'PATH_TO_SINS_INPUT_FOLDER' in line:
                path_to_sins_input_folder = line.split()[2]
            elif 'NAME_OF_SINS_PROJECT' in line:
                name_of_sins_project = line.split()[2]
            elif 'PATH_TO_SINSSAMPLER_INPUT_FOLDER' in line:
                address_of_input_folder = line.split()[2]

    address_of_pref_file = path_to_sins_input_folder + name_of_sins_project + "/output_preferences.txt"
    address_of_world_file = path_to_sins_input_folder + name_of_sins_project + "/world.txt"

    '''
    open file sequentially and search for string in line
    '''
    with open(address_of_pref_file, 'r') as inF:
        for line in inF:
            if 'generationsIntervalgen' in line:
                global generationsSampledInterval
                generationsSampledInterval = int(line.split()[1])
            elif 'recStart' in line:
                recording_starts_at_gen = int(line.split()[1])

    name_of_layer = ''
    with open(address_of_world_file, 'r') as inF:
        for line in inF:
            if 'numberOfGenerations' in line:
                global numberOfGenerations
                numberOfGenerations = int(line.split()[1])
            elif 'layerName' in line:
                name_of_layer += line.split()[1] + "\n"
            elif 'number_of_layers' in line:
                number_of_layers = line.split()[1]

    address_of_genotype_file = path_to_sins_input_folder + name_of_sins_project + "/genetics/" + name_of_layer.split("\n")[0] + "/genotype.txt"

    with open(address_of_genotype_file, 'r') as inF:
        for line in inF:
            if 'typeX' in line:
                type_of_chromosome_x = line
            elif 'typeY' in line:
                type_of_chromosome_y = line
            elif 'typeMT' in line:
                type_of_chromosome_mt = line
            elif 'typeA' in line:
                type_of_chromosome_a += line + "\n"
            elif 'nbAutosomes' in line:
                number_of_autosomes_line = line

    '''
    Creates sampling files necessary for SinsSampler to run
    '''
    ''''Create config.txt'''
    config_file = open(address_of_input_folder + 'config' + simulation_name + '.txt', 'w+')
    config_file.write("inputInformation\n"
                      "layerNumber " + number_of_layers + "\n" +
                      name_of_layer +
                      number_of_autosomes_line +
                      type_of_chromosome_x +
                      type_of_chromosome_y +
                      type_of_chromosome_mt +
                      type_of_chromosome_a)

    '''Create generation.txt'''
    if os.path.isfile(address_of_input_folder + 'generations.txt'):
        generation_file = open(address_of_input_folder + 'generations.txt', 'w+')
    else:
        generation_file = open(address_of_input_folder + 'generations.txt', 'a')

    for i in range(recording_starts_at_gen, numberOfGenerations + 1, generationsSampledInterval):
        print i
        generation_file.write(str(i) + "\n")

    generation_file.close()

    '''
    Create sampling[generation].txt

    Example:
    "PopulationName DemeLine DemeColumn NumMale NumFemale\n"
    "layerOne 0 0 10 10\n"
    "layer0 0 4 10 10\n"
    "layer0 0 8 10 10\n"
    "layer0 2 2 10 10\n"
    "layer0 2 6 10 10\n"
    "layer0 4 0 10 10\n"
    "layer0 4 4 10 10\n"
    "layer0 4 8 10 10\n"
    "layer0 6 2 10 10\n"
    "layer0 6 6 10 10\n"
    "layer0 8 0 10 10\n"
    "layer0 8 4 10 10\n"
    "layer0 8 8 10 10"
    '''
    # range(initial generation, number of generations + 1, generations sampling interval)
    for i in range(recording_starts_at_gen, numberOfGenerations + 1, generationsSampledInterval):
        print i
        sampling_file = open(address_of_input_folder + 'sampling' + str(i) + '.txt', 'w+')
        sampling_file.write("PopulationName DemeLine DemeColumn NumMale NumFemale\n"
                            "layerOne 0 0 10 10\n")
        sampling_file.close()
