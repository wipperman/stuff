## Modified by rafwiewiora for pdb splitting into files containing a number of models (i.e. 100 each from a large simulation)
## Original from fomightez/structurework

import os
import sys
import argparse
from argparse import RawTextHelpFormatter


###---------------------------HELPER FUNCTIONS---------------------------------###

def generate_output_files_prefix(file_name):
    '''
    Takes a file name as an argument and returns string for the prefix of the
    individual output files. The generated name is based on the original file
    name.

    Specific example
    ================
    Calling function with
        ("reductase_ensemble.pdb")
    returns
        "reductase_ensemble"
    '''
    main_part_of_name, file_extension = os.path.splitext(
        file_name) #from http://stackoverflow.com/questions/541390/extracting-extension-from-filename-in-python
    if '.' in file_name:  #I don't know if this is needed with the os.path.splitext method but I had it before so left it
        return main_part_of_name
    else:
        return file_name

def extract_models(multi_model_PDB_file):
    '''
    This function takes a file containing several PDB-formatted structure models
    and extracts each individual mode. Saving each individual model to a
    new file based on the name of the original file.

    Arguments for the function are as follows:
        * the file with PDB-formatted models. Requires the PDB file include
        both MODEL and ENDMDL

    The function returns the following:
        * number of models_extracted
        * the first part of the name of the created output_files
    '''
    # in preparation use the file name to generate a prefix for the
    # name of the output files.
    generated_output_files_prefix = generate_output_files_prefix(
        multi_model_PDB_file)

    #initialize values
    the_multi_file_stream = open(multi_model_PDB_file , "r")
    model_number = 1
    modelcounter = 0
    new_file_text = ""
    for line in the_multi_file_stream:
        line = line.strip() #for better control of ends of lines
        if line == "ENDMDL":
            new_file_text += line + '\n'
            modelcounter += 1
            if modelcounter < 100:
                continue
            else:
            # save file with file number in name
                output_file = open(generated_output_files_prefix +"_model_" + str(
                    model_number) + ".pdb", "w")
                output_file.write(new_file_text.rstrip('\r\n')) #rstrip to remove trailing newline
            # from http://stackoverflow.com/questions/275018/how-can-i-remove-chomp-a-newline-in-python
                output_file.close()
            # reset everything for next model
                model_number += 1
                new_file_text = ""
                modelcounter = 0
        else:
            new_file_text += line + '\n'
    # the loop won't have saved unless reached 100 models - for files with less & last set of models for files with NOT exactly x00 models need to save the last set. I.e. check if something left in new_file_text, if so - save.
    if new_file_text:
        output_file = open(generated_output_files_prefix +"_model_" + str(
            model_number) + ".pdb", "w")
        output_file.write(new_file_text.rstrip('\r\n'))
        output_file.close()        

    the_multi_file_stream.close()
    # The model number will be one higher than it should be because the process
    # of resetting for the next model adds one the model counter, even when
    # there is not a next model in the file. Reducing by one will fix.
    model_number -= 1
    return (model_number, generated_output_files_prefix)




###--------------------------END OF HELPER FUNCTIONS---------------------------###







###-----------------Actual Main function of script---------------------------###
###----------------------GET FILE AND PREPARE TO PARSE-----------------------###
#file to be provided as a argument when call program.
#argparser from http://docs.python.org/2/library/argparse.html#module-argparse and http://docs.python.org/2/howto/argparse.html#id1
parser = argparse.ArgumentParser(
    prog='multiple_model_PDB_file_splitter.py',description="multiple_model_PDB_file_splitter.py is designed to split a multi-model PDB\nfile into multiple files of the individual structure models.\nRequires the PDB file include both MODEL and ENDMDL records for each of the models.\n\nWritten by Wayne Decatur --> Fomightez @ Github or Twitter.  \n \n \n \n \nActual example what to enter on command line to run program:\npython multiple_model_PDB_file_splitter.py multi_model.pdb\n \n \n \n ", formatter_class=RawTextHelpFormatter
    )
#learned how to control line breaks in description above from http://stackoverflow.com/questions/3853722/python-argparse-how-to-insert-newline-the-help-text
#DANG THOUGH THE 'RawTextHelpFormatter' setting seems to apply to all the text for argument choices. I don't know yet if that is what really what I wanted.
parser.add_argument("InputFile", help="name of file containing multiple PDB formatted structure models. REQUIRED.")
#I would also like trigger help to display if no arguments provided because need at least input file
if len(sys.argv)==1:    #from http://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

if os.path.isfile(args.InputFile):
    #root_path = path_to_folder_with_file # LEFT HERE FOR USE IN DEBUGGING
    #fastq_file = open(root_path + FASTA_protein_sequence_records_file , "r")# LEFT HERE FOR USE IN DEBUGGING; JUST UNCOMMENT THIS AND ABOVE LINE AND COMMENTOUT NEXT LINE
    multi_model_PDB_file = args.InputFile
    #logging.debug(multi_model_PDB_file)
    number_of_models = 0 #initiate with zero as value of number of models recognized


    #Read PDB models, keeping track of total, and write each model
    # to a file. THIS FUNCTION CALL IS THE MAIN POINT OF THIS PROGRAM.
    sys.stderr.write("Reading in your file...")
    number_of_models, output_files_prefix = (
        extract_models(multi_model_PDB_file))

    #FOR DEBUGGING
    #logging.debug(number_of_models)
    #logging.debug(output_files_prefix)

    #give user some stats and feeback
    sys.stderr.write("\nConcluded. \n")
    if number_of_models < 2:
        sys.stderr.write("Sorry. Only one model was recognized in the file. \
            Please examine your file for the presence of multiple 'MODEL' and 'ENDMDL' indicators.")
        sys.stderr.write("A file named '"+ output_files_prefix+"_model_1.pdb' was made in the process. ")
    else:
        sys.stderr.write("File split into "+ str(number_of_models)+" models. ")
        sys.stderr.write("\nFiles with names '"+
            output_files_prefix+"_model_1.pdb', '"+
            output_files_prefix+"_model_2.pdb', etc., "+
            "\nhave been created in same directory as the input file.\n\n")


else:
    sys.stderr.write("SORRY. " + args.InputFile + " IS NOT RECOGNIZED AS A FILE.\n\n")
    parser.print_help()
    sys.exit(1)


#*******************************************************************************
###-***********************END MAIN PORTION OF SCRIPT***********************-###
#*******************************************************************************
