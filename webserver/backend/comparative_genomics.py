#!/usr/bin/env python
import argparse
import subprocess
import re
import sys




def FastANI():
	
	return




def StringMLST():
	os.system("mkdir -p stringMLST_analysis; cd stringMLST_analysis")
	# Download the Listeria MLST scheme
	os.system("stringMLST.py --getMLST -P listeria/lsa --species Listeria")
	# Run the tool
	os.system("stringMLST.py --predict -d /home/projects/group-c/data -P listeria/lsa -k 35 -o StringMLST_Listeria")
	return




def ChewBBACA():
	os.system("mkdir -p ChewBBACA_MLST_analysis; cd ChewBBACA_MLST_analysis")
	# wgMLST schema creation
	os.system("chewBBACA.py CreateSchema -i /home/projects/group-c/Team3-ComparativeGenomics/functional_annotation_data/comparative_fna -o schema_seed --cpu 6 --ptf Listeria_monocytogenes.trn")
	# Allele calling with the created wgMLST schema
	os.system("chewBBACA.py AlleleCall -i /home/projects/group-c/Team3-ComparativeGenomics/functional_annotation_data/comparative_fna -g schema_seed/ -o results_cg --cpu 6 --ptf Listeria_monocytogenes.trn")
	# Paralog detection
	os.system("chewBBACA.py RemoveGenes -i results_alleles.tsv -g RepeatedLoci.txt -o alleleCallMatrix_cg")
	# Test genome quality for cgMLST
	os.system("chewBBACA.py TestGenomeQuality -i alleleCallMatrix_cg.tsv -n 13 -t 200 -s 5")
	# Allele calling with the created cgMLST schema
	os.system("chewBBACA.py AlleleCall -i /home/projects/group-c/Team3-ComparativeGenomics/functional_annotation_data/comparative_fna -g listgenes_core.txt -o results --cpu 6 --ptf Listeria_monocytogenes.trn")
	# Extract only the loci present in 95% of the matrix
	os.system("chewBBACA.py ExtractCgMLST -i alleleCallMatrix_cg.tsv -o cgMLST_completegenomes -p 0.95")
	# Assess the cgMLST allele quality attribution for all the genomes
	os.system("chewBBACA.py TestGenomeQuality -i cgMLST_all.tsv -n 13 -t 300 -s 5")
	
	# For Minimum Spanning Tree, analysis_all/cgMLST_25/cgMLST.tsv can be run with Phyloviz after running the following line 
	# os.system("chewBBACA.py ExtractCgMLST -i cgMLST_all.tsv -o cgMLST_25 -g removedGenomes_25.txt")

	return




def kSNP():##only for 7210 project, cd to ComparativeGenomics directory
    subprocess.call(["conda", "activate", "T3env4"])    
    subprocess.call(["kSNP3", "-in", "SNP/list_file.txt", "-outdir","output", "-k","19", "-ML","|", "tee","log.txt"])   
    subprocess.call(["ete3", "view", "--text", "SNP/output/tree_tipAlleleCounts.ML.tre"])  
    return




def Roary():
	
	return




def BPGA():
	
	return


def GFFanalysis():
	subprocess.call(["cd","/home/projects/group-c/Team3-ComparativeGenomics/script"])
	subprocess.call(["mkdir","GFF"])
	subprocess.call(["./comparative_gffconverter.py"])


def main():
    jobs = {"FastANI": FastANI, "StringMLST": StringMLST, "ChewBBACA": ChewBBACA, "kSNP": kSNP, "Roary": Roary, "BPGA": BPGA, "GFFanalysis":GFFanalysis}
    choosenOption = sys.argv[1]
    jobs[choosenOption]()

if __name__ == "__main__":
    main()
