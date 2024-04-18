def extract_words(input_filename, output_filename):
    # Open the input file and read lines
    with open(input_filename, 'r') as file:
        lines = file.readlines()
        word_list = set()
        for line in lines:
            word = line.split()[0]
            word_list.add(word)
    
    with open(output_filename, 'w') as outfile:
        # Process each line
        for word in word_list:
            outfile.write(word + '\n')



# def prepare_labels(file_name,num_labels):
#   with open(file_name,"r") as cate:
#       lines = cate.readlines()
#       google_category_labels = []
#       for line in lines:
#           parts = line.strip()
#           print(parts)
#           break

input_filename = 'overall.txt'
output_filename = 'output_words_only.txt'
extract_words(input_filename, output_filename)
# prepare_labels(output_filename,20)
