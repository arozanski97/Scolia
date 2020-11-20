## ----------------------IMPORT NECESSARY PACKAGES----------------------- 
#from optparse import OptionParser
import os
from webserver.backend import db_util
from os import popen
import shutil
import tempfile
import subprocess
import time
start_time=time.time()


##---------------------RUN CARD------------------------------
def CARD(input_dir,output_dir):
	print("Running CARD-rgi......")
	make_temp="mkdir "+output_dir+"/CARD"
	os.system(make_temp)
	CARD_output_path=output_dir+"/CARD"
	for files in os.listdir(input_dir):
		print("IN OS LIST DIR")
		prefix=files.split("_")[0]
		p=subprocess.Popen(command,stdout=subprocess.PIPE)
		out=p.communicate()
		final_output=CARD_output_path+"/"+prefix+"_CARD-RGI_coding"
		command = ["/projects/VirtualHost/predictc/html/miniconda_webserver/envs/rgi_env/bin/rgi","-i",input_dir+"/"+files,"-o",final_output,]
		p=subprocess.Popen(command, stdout=subprocess.PIPE)
		out = p.communicate()
		counter +=1
	return(CARD_output_path)
	
##-----------------------RUN VFDB--------------------------------
def VFDB(input_dir,output_dir):
	print("Running blastp on VFDB......")
	make_temp="mkdir "+output_dir+"/VFDB"
	os.system(make_temp)
	VFDB_output_path=output_dir+"/VFDB"

	for files in os.listdir(input_dir):
		prefix=files.split("_")[0]
		#prefix = files[0:7]
		command = ["blastn", "-db", "./Tools/Virulence_Factors_core_db", "-query",input_dir+"/"+files,"-out",VFDB_output_path+"/"+prefix+"_VFDB_coding", "-max_hsps","1","-max_target_seqs","1","-num_threads","4","-evalue","1e-5"]
		p=subprocess.Popen(command,stdout=subprocess.PIPE,)
		out=p.communicate()
	for file in os.listdir(VFDB_output_path):
		file_path=VFDB_output_path+"/"+file
		if os.stat(file_path).st_size == 0:
			command="rm "+file_path
			os.system(command)
	return(VFDB_output_path)
	

##-------------------FORMAT CARD OUTPUT SO IT IS IN ONE LINE GFF FORMAT-------------------------------
def formatCARD(input_dir,output_dir):
	make_temp="mkdir -p "+output_dir+"/format/CARD"
	os.system(make_temp)
	path_to_CARD=input_dir
	print("formatting...card")
	for filename in os.listdir(path_to_CARD):
		if "gff" in filename:
			sample=filename.split("_")[0]
			path_CARD_file=path_to_CARD+"/"+filename
			CARD_file=open(path_CARD_file,"r")
			CARD_output_path_gff=output_dir+"/format/CARD/"+sample+"_card_mapped.gff"
			CARD_output_gff=open(CARD_output_path_gff,"w+")
			for line in CARD_file:
				if line.startswith("NODE"):
					annotation=line.split("\t")
					node=annotation[0]
					node=node.split("_")
					node=node[:-1]
					node_join="_"
					node=node_join.join(node)
					annotation[0]=node
					annotation_join="\t"
					#print(annotation)
					annotation=annotation_join.join(annotation)
					gff_line=annotation
					#print(gff_line)
					CARD_output_gff.write(gff_line)
			CARD_output_gff.close()	

##-------------------FORMAT VFDB SO IT IS IN GFF FORMAT-------------------------------------	
def formatVFDB(input_dir,output_dir):
	VFDB_dir=input_dir
	make_temp="mkdir -p "+output_dir+"/format/VFDB"
	os.system(make_temp)
	print("formatting...VFDB")
	for filename in os.listdir(VFDB_dir):
		full_file_path=VFDB_dir+"/"+filename
		VFDB_file=open(full_file_path,"r")
		VFDB_file_read=VFDB_file.readlines()
		sample=filename.split("_")[0]
		output_path_gff=output_dir+"/format/VFDB/"+sample+"_VFDB.gff"
		gff_VFDB=open(output_path_gff,"w+") 
		for index in range(len(VFDB_file_read)):
			if "Query=" in VFDB_file_read[index] and "Sequences producing" in VFDB_file_read[index+4]:
				node=VFDB_file_read[index].split(" ")
				node=node[1]
				count=9
				start_bool=False
				while not "Lambda" in VFDB_file_read[index+count]:
					if "Score =" in VFDB_file_read[index+count]:
						score=VFDB_file_read[index+count]
						score=score.split(" ")
						score=score[-1].rstrip()
						strand=VFDB_file_read[index+count+2]
						strand=strand.split("/")[1].rstrip()
						if strand=="Plus":
							strand="+"
						if strand=="Minus":
							strand="-"
					if VFDB_file_read[index+count].startswith("Query"):
						split_line=VFDB_file_read[index+count].split(" ")
						if not start_bool:
							start_bool=True
							start=split_line[2]
						end=split_line[-1]
						end=end.rstrip()
					count=count+1
				gff_write=node.rstrip()+"\tVFDB\tprotein_match\t"+start+"\t"+end+"\t"+score+"\t"+strand+"\t.\tstitle="+VFDB_file_read[index+9].lstrip('>')
				gff_VFDB.write(gff_write)
		
		VFDB_file.close()
		gff_VFDB.close()

##-------------------------------MERGE ALL GFF FORMATTED FILES INTO ONE SO THAT NODES ARE IN ORDER FOR EACH SAMPLE------------------------
def mergeGff(output_dir,output_path2):
	print(output_dir)
	print(output_path2)
	print("Merging Files.....")
	make_temp="mkdir "+output_path2+"/merged"
	os.system(make_temp)
	make_temp="mkdir -p "+output_path2+"/VFDB"
	os.system(make_temp)
	copy_vfdb="for i in "+output_dir+"/format/VFDB/*; do cp $i "+output_path2+"/VFDB; done"
	os.system(copy_vfdb)
	make_temp="mkdir -p "+output_path2+"/CARD"
	os.system(make_temp)
	copy_card="for i in "+output_dir+"/format/CARD/*; do cp $i "+output_path2+"/CARD; done"
	os.system(copy_card)

	sample_dict={}
	mapped_dir_path=output_dir+"/format"
	for dir_name in os.listdir(mapped_dir_path):
		if dir_name=="eggNog" or dir_name=="CARD" or dir_name=="VFDB" or dir_name=="eggNOG" or dir_name=="SignalP" or dir_name=="Pilercr":
			tool_dir_path=mapped_dir_path+"/"+dir_name
			for filename in os.listdir(tool_dir_path):
				if "gff" in filename and not "getorf" in filename:
					filename_split=filename.split("_")
					sample=filename_split[0]
					tool=filename_split[1]
					file_path=tool_dir_path+"/"+filename
					annotation_file=open(file_path,"r")
					annotation_file_read=annotation_file.readlines()
					if sample in sample_dict:
						feature_dict=sample_dict.get(sample)
						for line in annotation_file_read:
							line_split=line.split("\t")
							node=line_split[0]
							write_dict=line
							if node in feature_dict:
								feature_dict[node]=feature_dict.get(node)+[write_dict]
							else:
								feature_dict[node]=[write_dict]
					if sample not in sample_dict:
						feature_dict={}
						for line in annotation_file_read:
							line_split=line.split("\t")
							node=line_split[0]
							write_dict=line
							if node in feature_dict:
								feature_dict[node]=feature_dict.get(node)+[write_dict]
							else:
								feature_dict[node]=[write_dict]
						sample_dict[sample]=feature_dict
					annotation_file.close()


	for key,value in sample_dict.items():
		sorted_dict={}
		feature_dict=value
		output_path=(output_path2+"/merged/"+key+"_merged.gff")
		output_file=open(output_path,"w+")
		sorted_list=sorted(feature_dict, key=lambda key1: int(key1.split("_")[1]))
		for i in sorted_list:
			node=i.split("_")[0:2]
			join_node="_"
			node=join_node.join(node)		
			if node in sorted_dict:
				sorted_dict[node].append(i)
			else:
				sorted_dict[node]=[i]
		sorted_list=sorted(sorted_dict, key=lambda key1: int(key1.split("_")[1]))
		for value_item in sorted_list:
			item=sorted_dict.get(value_item)
			value_sort=sorted(item, key=lambda key1: (int((key1.split(":")[1]).split("-")[1])))
			for get_item in value_sort:
				loop_lines=feature_dict.get(get_item)
				node=get_item
				header="##sequence_region "+node+"\n"
				output_file.write(header)
				for annotation in loop_lines:
					output_file.write(annotation)

		output_file.close()


	
def f(input_path,output_path,flag):
	temp_dir=output_path+"/temp_dir"
	make_temp="mkdir "+temp_dir
	os.system(make_temp)

##Run CARD and VFDB by default 
	CARD_output_path=CARD(input_path,temp_dir)
	
	VFDB_output_path=VFDB(input_path,temp_dir)

##Reformat CARD and VFDB  outputs into gff format to be merged
	formatCARD(CARD_output_path,temp_dir)
	formatVFDB(VFDB_output_path,temp_dir)

##Merge all of the reformated files so there is one full gff file for each sample 
	mergeGff(temp_dir,output_path)
	print(time.time()-start_time)
	shutil.rmtree(temp_dir)
###YOU MUST INCLUDE THIS IN YOUR PIPELINE input_path and output_path and flag are arguments given when called from routes.py
	if flag == 0:
		db_util.update_pipeline_status(input_path.split('/')[-2])
	print (output_path)
	p=subprocess.Popen(["tar","-czvf",output_path+".tar.gz",output_path], stdout=subprocess.PIPE)
	out=p.communicate()
	print (input_path)
	input_path=input_path.split('/')[0:4]
	input_path='/'.join(input_path)
	print (input_path)
	p=subprocess.Popen(["rm","-r",input_path], stdout=subprocess.PIPE)
	out=p.communicate()

