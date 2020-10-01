#!/usr/bin/env python3

import time
import subprocess
import glob
import os

from webserver.backend import db_util

# PIPELINE HELPER FUNCTION
def f(input_dir, flag,output_dir, tools):
    print(input_dir)
    # DIRECTORIES

    subprocess.call("mkdir "+output_dir+"/fastp", shell=True)
    subprocess.call("mkdir "+output_dir+"/trimmed", shell=True)
    subprocess.call( "mkdir "+output_dir+"/assembly", shell=True)
    subprocess.call("mkdir " + output_dir + "/passembly", shell=True)
    subprocess.call("mkdir " + output_dir + "/quality", shell=True)
    subprocess.call("mkdir "+output_dir+"/passembly/pipeline_temp", shell=True)
    subprocess.call(" mkdir"+output_dir+" /quality/pipeline_temp", shell=True)
    fastp_dir = output_dir + '/fastp'
    print("fastp" + fastp_dir)
    trimmed_dir = output_dir + '/trimmed'
    assembly_dir = output_dir + '/assembly'
    passembly_dir = output_dir + '/passembly/pipeline_temp'
    quality_dir = output_dir + '/quality/pipeline_temp'
    trim_flag = 'trim' in tools
    run_fastp(input_dir, fastp_dir, trimmed_dir, trim_flag)
    run_multiqc(fastp_dir)
    print(tools)
    if 'skesa' in tools:
        run_skesa(trimmed_dir, assembly_dir)
    else:
        run_spades(trimmed_dir, assembly_dir)
    run_plasmidspades(trimmed_dir, passembly_dir)
    run_assemblyquality(assembly_dir, quality_dir)

    if flag == 0:
        db_util.update_pipeline_status(input_dir.split('/')[-2])

    p = subprocess.Popen(["tar", "-czvf", output_dir + ".tar.gz", output_dir], stdout=subprocess.PIPE)
    out = p.communicate()
    print(input_dir)
    input_path = input_dir.split('/')[0:4]
    input_path = '/'.join(input_path)
    print(input_path)
    p = subprocess.Popen(["rm", "-r", input_path], stdout=subprocess.PIPE)
    out = p.communicate()

################## QUALITY CONTROL

######### FASTP

# assumptions about input files: all of the input files are contained in a single directory
# all of the files fit the pattern *.f*, both of the reads for the sample share a sample id
# read one: _1.f*, read two: _2.f*

# load fastq files into fastp
def run_fastp(raw_dir, fastp_dir, trimmed_dir, trim=True):
    # deleting previous directories, make new ones
    print("running fastp.........")
    # subprocess.call(['rm', '-rf', fastp_dir, trimmed_dir])
    # subprocess.call(['mkdir', fastp_dir, trimmed_dir])

    for filename in glob.glob(raw_dir + '/*1.f*'):
        id = filename[len(raw_dir)+1:filename.find('.') - 6]
        print(id)
        print(glob.glob('{}*{}*2*'.format(raw_dir, id))[0])
        arg_list = ['fastp',
                    '-i', filename,
                    '-I', glob.glob('{}*{}*2*'.format(raw_dir, id))[0],
                    '-o', '{}/{}_r1.fq'.format(trimmed_dir, id),
                    '-O', '{}/{}_r2.fq'.format(trimmed_dir, id)]
        if trim:
            arg_list += ['-f', '5', '-F', '30', '-t', '10', '-e', '28', '-c', '-5', '5', '-M', '27']
        else:
            subprocess.call(['cp', filename, trimmed_dir])
            subprocess.call(['cp', glob.glob('{}*{}*2*'.format(raw_dir, id))[0], trimmed_dir])

        arg_list += ['-j', '{}/{}_fastp.json'.format(fastp_dir, id)]

        subprocess.call(arg_list)
    print("completed fastp....")

######### MULTIQC

# output: multiqc report, fastp_dir + 'multiqc_report.html'
# '/home/projects/group-c/Team3-GenomeAssembly/1.readQC/pipeline_temp/multiqc_report.html'
def run_multiqc(fastp_dir):
    print("running multiqc.....")
    subprocess.call(['multiqc', fastp_dir, '-o', fastp_dir])
    print("completed multiqc........")

################## GENOME ASSEMBLY

def run_spades(trimmed_dir, assembly_dir):
    print("running spades........")
    samples = subprocess.check_output("ls " + trimmed_dir + " | grep -o '^.*_' | uniq", shell=True,
                                        universal_newlines=True)
    idlist = samples.split()

    for id in idlist:
        # delete previous temporary directories, make new temporary directories
        id_dir = assembly_dir + '/' + id[:-1]
        subprocess.call(['rm', '-rf', id_dir])
        subprocess.call(['mkdir', id_dir])
        print("generated"+id_dir+"......")
        # run plasmid spades
        subprocess.call(
            ['spades.py', '--careful', '-o', id_dir, '--pe1-1', '{}/{}r1.fq'.format(trimmed_dir, id),
                '--pe1-2', '{}/{}r2.fq'.format(trimmed_dir, id)])

def run_skesa(trimmed_dir, assembly_dir):
    samples = subprocess.check_output("ls " + trimmed_dir + " | grep -o '^.*_' | uniq", shell=True,
                                        universal_newlines=True)
    idlist = samples.split()

    for ii in idlist:
        # delete previous temporary directories, make new temporary directories
        id_dir = assembly_dir + '/' + ii[:-1]
        subprocess.call(['rm', '-rf', id_dir])
        subprocess.call(['mkdir', id_dir])

        sample1 = trimmed_dir + '/' + ii + 'r1.fq'
        sample2 = trimmed_dir + '/' + ii + 'r2.fq'
        # output = assembly_dir+'/'+idlist[ii]+'skesa.fa'
        command = ['skesa', '--fastq', sample1, sample2, '--contigs_out', id_dir + '/contigs.fasta']
        subprocess.call(command)

################## PLASMID ASSEMBLY

def run_plasmidspades(trimmed_dir, passembly_dir):
    samples = subprocess.check_output("ls " + trimmed_dir + " | grep -o '^.*_' | uniq", shell=True,
                                        universal_newlines=True)
    idlist = samples.split()

    for id in idlist:
        # delete previous temporary directories, make new temporary directories
        id_dir = passembly_dir + '/' + id[:-1]
        subprocess.call(['rm', '-rf', id_dir])
        subprocess.call(['mkdir', id_dir])

        # run plasmid spades
        subprocess.call(
            ['spades.py', '--plasmid', '--careful', '-o', id_dir, '--pe1-1', '{}/{}r1.fq'.format(trimmed_dir, id),
                '--pe1-2', '{}/{}r2.fq'.format(trimmed_dir, id)])

################## ASSEMBLY QUALITY

def run_assemblyquality(assembly_dir, quality_dir):
    idlist = subprocess.check_output("ls " + assembly_dir, shell=True, universal_newlines=True)
    subprocess.call(['rm', '-rf', quality_dir, '/assemblyfiles'])
    subprocess.call(['mkdir', quality_dir, '/assemblyfiles'])
    subprocess.call(['rm', '-rf', quality_dir, '/quast'])
    subprocess.call(['mkdir', quality_dir, '/quast'])
    subprocess.call(['rm', '-rf', quality_dir, '/Busco'])
    subprocess.call(['mkdir', quality_dir, '/Busco'])

    for id in idlist:
        subprocess.call(
            'cp ' + assembly_dir + '/' + id + '/contigs.fasta ' + quality_dir + '/assemblyfiles/' + id + '_contigs.fasta',
            shell=True, universal_newlines=True)
        subprocess.call(['rm', '-rf', quality_dir, '/Busco/', id])
        subprocess.call(['mkdir', quality_dir, '/Busco/', id])
        subprocess.call(
            'busco -m Genome -i ' + assembly_dir + '/' + id + ' -l bacteria_odb10 -o ' + quality_dir + '/Busco/' + id,
            shell=True, universal_newlines=True)

    subprocess.call('quast ' + quality_dir + '/assemblyfiles/* -o ' + quality_dir + '/quast/ --circos', shell=True,
                    universal_newlines=True)


