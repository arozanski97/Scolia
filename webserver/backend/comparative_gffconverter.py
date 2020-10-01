#!/usr/bin/env python
import os

# function to convert gff file to isolate - gene file
def gffconvertgene(path, output, genefilename, pafilename):
	outputpath = output+'/'+genefilename
	#write header to isolate - gene file
	fw = open(outputpath,"w")
	fw.write('Isolate file name'"\t"'Gene names (Tab delimited)'"\n")
    # iterate through each gff file in the path
	count = 0
	genelist = []
	for filename in os.listdir(path):
		if filename.endswith(".gff"):
			filepath=path + "/"+ filename
			# open each gff file and read each line
			fw.write("%s \t" % (filename))
			fr =open(filepath,"r")
			for line in fr:
				# if each line starts with NODE then consider that line as containing genes
				if line.startswith('NODE'):
					line9 = line.split("\t")[8]
					# nineth line of card gff starts with 'Name'
					if line9.startswith('Name'):
						gene = line9.split(";")[0].split("=")[1]
					# nineth line of vfdb gff startw with 'stitle'
					if line9.startswith('stitle'):
						gene = line9.split(" ")[1]
						#strip the paranthesis
						gene = gene[1:-1 ]
					fw.write("%s \t" %(gene))
					count = count + 1
					if gene not in genelist:
						genelist.append(gene)
			fw.write("\n")
			fr.close()
	fw.close()
	#call to function to convert genes file to presence absence file - tab delimited
	gffpresenceabsence(outputpath, pafilename, genelist, count)

#function to convert gff file to isolate - gene presence absence file - tab delimited
def gffpresenceabsence(path, pafilename, genelist, count):
	#cut GFFtoGene.txt and add GFFtoGenepa.txt
	outputpath = path.split(".")[0]+ pafilename
	#read the file line by line
	fwr = open(path,'r')
	next(fwr)
	fw2= open(outputpath,'w')
	fw2.write("Isolate file name""\t")
	for gene in genelist:
		fw2.write("%s \t" %(gene))
	fw2.write("\n")
	#iterate through isolate - gene file and generate a presence absence matrix
	for line in fwr:
		genes=line.split("\t")
		fw2.write("%s \t" % (genes[0]))
		for i in range(len(genelist)): 
			value = 0
			for j in range(1,len(genes)):
				if genelist[i] == genes[j].strip():
					value = 1
			fw2.write("%s \t" % (value))
		fw2.write("\n")
	fw2.close()
      
if __name__ == "__main__":
	#gff analysis of CARD and VFDB
	# # Two output files are provided - 1. GFFtoGene.txt file - gives each isolate and all its genes (tab delimited)
	# #2. GFFtoGenepa.tsv - gives presence absence matrix view of the isolates and genes
	
	#provide path to the locaiton of **** CARD **** gff files
	cardpath = "/home/projects/group-c/Team3-ComparativeGenomics/functional_annotation_data/CARD_gff"
	cardpathplasmid = "/home/projects/group-c/Team3-ComparativeGenomics/functional_annotation_data/plasmids/CARD_plasmids_gff"
	#provide path to the locaiton of **** VFDB **** gff files
	vfdbpath = "/home/projects/group-c/Team3-ComparativeGenomics/functional_annotation_data/VFDB_gff"
	vfdbpathplasmid = "/home/projects/group-c/Team3-ComparativeGenomics/functional_annotation_data/plasmids/VFDB_plasmids_gff"
	# #provide file extensions
	genefilename = 'GFFtoGene.txt'
	pagenefilename = 'pa.tsv' 
	#output file location
	outputpath = "/home/projects/group-c/Team3-ComparativeGenomics/script/GFF"

	# function to analyze CARD gff data
	gffconvertgene(cardpath,outputpath, "card"+genefilename, pagenefilename)
	gffconvertgene(cardpathplasmid, outputpath,"cardplasmid"+ genefilename, pagenefilename)
	print("CARD isolate-gene files and Presence absence matrix (paMatrix) generated")
	# function to convert VFDB gff data
	gffconvertgene(vfdbpath, outputpath, "vfdb"+genefilename, pagenefilename)
	gffconvertgene(vfdbpathplasmid, outputpath, "vfdbplasmid"+genefilename, pagenefilename)
	print("VFDB isolate-gene files and Presence absence matrix (paMatrix) generated")
