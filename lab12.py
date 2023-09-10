input_name = input()
output_name = input()

try:
    infile = open(input_name, "r")
except:
    print("unable to open the input file")

try:
    outfile = open(output_name, "w")
except:
    print("unable to open the output file")

line = infile.readline()
while line!="":
    if line[0]!="#":
        outfile.write(line)
    line=infile.readline()

infile.close()
outfile.close()