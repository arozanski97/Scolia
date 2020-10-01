# SCOLiA

SCOLiA (Subtyping and Comparison Of LIsteria Assemblies) is a webserver for analyzing *Listeria monocytogenes* genomes. 

# User Guide

SCOLiA offers four different modules for analyzing *Listeria monocytogenes* genomes: genome assembly, gene prediction, functional annotation, and comparative genomics. Each of these steps can be executed independently by users.

## Genome Assembly

The genome assembly module is optimized for paired-end Illumina reads sequenced from *Listeria monocytogenes*. Upon job submission, the genome assembly pipeline performs quality control and trimming on the samples using fastp and MultiQC. From there, the trimmed reads are passed onto either SPAdes or SKESA for assembly. Regardless of assembler choice, plasmids are assembled through SPAdes using the plasmid assembly option. Finally, BUSCO and Quast are used to assess the quality and completeness scores of the assembled contigs. 

* *Input Files:* FASTQ files for up to 50 isolates 
* *Options:* 
    * Skip trimming
    * Choose assembly tool: SPAdes (default) or SKESA
* *Output Files:* 
    * Fastp and MultiQC quality control report
    * Contigs for each isolate
    * Assembly quality report generated from BUSCO and Quast

## Gene Prediction

The gene prediction module allows for the prediction of both coding and non-coding genes, both of which are predicted using *ab initio* tools and validated using homology-based tools. For coding genes, the gene prediction pipeline runs two ab initio tools (PRODIGAL and GENEMarkS-2), uses BLAST to compare the resulting gene list to the CDS of the query sequence, and finally retrieves the coding output. A similar process is used for non-coding genes, with threee ab initio tools (ARAGORN, BARRNARP, and RNAmmer) run and the homology-based tool Infernal used to validate and retrieve the non-coding output.

* *Input Files:*
    * Assembled genomes and plasmids from the genome assembly pipeline
    * Coding sequences of the query species in FASTA format
* *Output Files*
    * Coding FASTA files and GFF files
    * Non-coding FASTA files and GFF files

## Functional Annotation

The functional annotation module allows users to annotate .FNA files produced by a gene prediction pipeline with predicted functions. The genes from the .FNA files are clustered by similarity using UCLUSt and then compared to genes present in the CARD-RGI and VFDB databases. CARD-RGI contains information about antibiotic resistance, while VFDB contains information about virulence. Functional annotations from these two databases are then merged to produce the final output. 

* *Input Files:* .FNA files
* *Output Files:* 
    * .GFF files with annotations
    * Count for each tool
    * A list of significant antibiotic and resistance genes present

## Comparative Genomics

The comparative gneomics module allows users to find the genetic relatedness between isolates using the following methods: Average Nucleotide Identity (ANI), allele phylogenetic trees, and/or annotated hierarchical trees.

* *Input Files:* 
    * Up to 10 FASTA files
    * OR up to 10 .GFF files
* *Options:* 
    * Input a reference genome or compare to default reference
    * Choose comparative genomics tools: FAST-ANI, StringMLST, and/or kSNP
* *Output Files:* 
    * For FASTA input: ANI distribution figure, maximum likelihood allele phylogenetic tree
    * For .GFF input: hierarchical clustering dendrogram
* *For Deployment:*
    * How it is set up now after speaking with IT, we still have to manually run the program within the path "/projects/VirtualHost/predictc/html/Team3-WebServer " within this directory run webserver.wsgi by using the command ./webserser.wsgi &
    * Once this is done the webserver will be fully functional through the link http://predict2020t3.biosci.gatech.edu
    * In the future we hope to get this set up so that we do not have to manually run it 
# Authors

* Sonali Gupta
* Aparna Maddala
* Allison Nicole Rozanski
* Ahish Melkote Sujay
* Yiqiong Xiao
* Yuhua Zhang



