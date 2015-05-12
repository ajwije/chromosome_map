
#!/usr/bin/python

# coding: utf-8



from reportlab.lib.units import cm, inch
from Bio.Graphics import BasicChromosome

from sys import argv
import getopt

def do_help():
   
    
    print """


    This python code will generate chromosome maps that shows physical coordinates and mapping distance. To use this script you will need to provide the following:
        -d, --directory = path to the directory that contains files 
        -i, --input_file = This file contains a list of files for each chromosome 
        -o, --output_file = The name of the output files (PDF format)
        -t, --title = Title for your chromosome map



"""

    exit()



def main():
    

    try:
        opts, args = getopt.getopt(argv[1:], 'd:i:o:t:h', ['directory=', 'input_file=', 'output_file=', 'title=','help'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            do_help()

        elif opt in ('-d', '--directory'):
            file_path_arg = arg
        elif opt in ('-i', '--input_file'):
            input_files_arg = arg
        elif opt in ('-o', '--output_file'):
            output_file_arg = arg
        elif opt in ('-t', '--title'):
            title = arg

        else:
            do_help()
            sys.exit(2)


    entries = []
    max_length =[]
    file_path = file_path_arg

    output_file = file_path + output_file_arg + ".PDF"

    input_files = open((file_path + input_files_arg), "r")
    for input_lines in input_files:
        split_lines = input_lines.strip("\r\n").split("\t")
        max_length.append(int(split_lines[1]))
        file_name = file_path +  input_lines.split("\t")[0] + ".txt"
        split_lines.append(file_name)
        entries.append(split_lines)
    

    # In[6]:

    max_len = max(max_length) #Could compute this
    telomere_length = max_len * 0.01 #For illustration
    per_page = 7
    chr_diagram = BasicChromosome.Organism()
    #chr_diagram.page_size = (per_page*2.2633333*cm + inch, 21*cm) #A4 landscape
    chr_diagram.page_size = (29.7*cm, 21*cm)
    chr_percentage = 0.075
    label_percentage = 0.13
    label_size = 3

    for name, length, filename in entries:
        #print name, filename
        with open(filename) as input_data:
            lines = [lines.replace("BARC_2.0_", "") for lines in input_data]
            
            #lines of the input file split using space and then first columns coverted to int
            #combine first three int and last two str 
            #converted to tuple
            #pos = [tuple(map(int, lines.split()[:3]) + (lines.split()[3:])) for lines in input_data]
            pos = [tuple(map(int, items.split()[:3]) + (items.split()[3:])) for items in lines]
            cur_chromosome = BasicChromosome.Chromosome(name)
        
        #Set the scale to the MAXIMUM length plus the two telomeres in bp,
        #want the same scale used on all five chromosomes so they can be
        #compared to each other
            cur_chromosome.scale_num = max_len + 2 * telomere_length
            cur_chromosome.chr_percent = chr_percentage
            cur_chromosome.label_sep_percent = label_percentage
            cur_chromosome.label_size = label_size
        #Add an opening telomere
            start = BasicChromosome.TelomereSegment()
            start.scale = telomere_length
            start.chr_percent = chr_percentage
            cur_chromosome.add(start)
        
        
        #Add a body - again using bp as the scale length here.
            body = BasicChromosome.AnnotatedChromosomeSegment(int(length), pos)
            body.scale = int(length)
            body.chr_percent = chr_percentage
            cur_chromosome.add(body)
           
        #Add a closing telomere
            end = BasicChromosome.TelomereSegment(inverted=True)
            end.scale = telomere_length
            end.chr_percent = chr_percentage
            cur_chromosome.add(end)

        #This chromosome is done
            chr_diagram.add(cur_chromosome)


    chr_diagram.draw(output_file, title)
    input_files.close() 

    if len(argv) < 4:
        do_help()   
       
if __name__ == "__main__":
    main()
  

