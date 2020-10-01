def dendogram(working_dir, flag):
    import os
    import subprocess
    import re
    #Assumption1: There are no other than gff files in teh database
    #Assumption2:The Eggnog Annotation column is always the 9th one and the ID is second identifier in that column
    #Assumption3: The files needed are in the current folder, the directory name should be added when working on the final version
    
    ################# Creating an Absencepresence matrix #################################
    
    files=os.listdir(working_dir+'/') 
    idmatrix=[None]*len(files) #nested matrix for OrthoDB IDs each sample in a row
    count = 0
    Proteinsformatrix = set()

    if flag == 1:
        for file in files:
            f=open(working_dir+'/'+file, 'r')
            contents=f.readlines()
            ids=[]
            for id in contents:
                ids.append(id.strip())
                Proteinsformatrix.add(id.strip()) #set.add(), adds only unique ids
            idmatrix[count]=ids        
            count = count+1
            f.close()
    else:
        for file in files:
            subprocess.call( "grep '^NODE' "+working_dir+"/"+file+" | cut -f9 | grep -v '^\.' > temp", shell=True)
            f=open('temp', 'r')
            contents=f.readlines()
            ids=[]
    
            for line in contents:
                id = re.split(r'[;.]', line)
                if len(id) > 1 and len(id[1])<12:
                    ids.append(id[1])
                    Proteinsformatrix.add(id[1]) #set.add(), adds only unique ids
        
            idmatrix[count]=ids        
            count = count+1
            f.close()
            subprocess.call("rm temp", shell=True)

    #converting set to list for ease of use
    proteinsformatrix = list(Proteinsformatrix)


    #Defining the matrix length
    absencepresencematrix = [['0' for j in range(len(Proteinsformatrix)+1)] for i in range(len(files)+1)]
    #Defining headers
    for x in range(len(absencepresencematrix[0])-1):
        absencepresencematrix[0][x+1] = proteinsformatrix[x]
    labels=[]
    for y in range(len(absencepresencematrix)-1):
        label=files[y]
        if len(label)>15:
            label=label[:15]
        absencepresencematrix[y+1][0] = label
        labels.append(label)


    #Filling zeros and ones
    for i in range(len(absencepresencematrix)-1):
        for j in range(len(absencepresencematrix[i])-1):
            if absencepresencematrix[0][j+1] in idmatrix[i]:
                absencepresencematrix[i+1][j+1] = '1'

    o=open(working_dir+"/"+"presenceabsencematrix.tsv", "w+")
    o.write("\n".join(("\t".join(absencepresencematrix[i])) for i in range(len(absencepresencematrix))))
    o.close()



    ######################## Creating a dendogram #################################

    import subprocess
    #subprocess.call("pip install pandas", shell=True)
    #subprocess.call("pip install matplotlib", shell=True)
    #subprocess.call("pip install scipy", shell=True)

    import pandas
    import matplotlib
    from scipy.cluster.hierarchy import dendrogram, linkage
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    #preparing the binary matrix
    binmat = pandas.read_csv(working_dir+'/'+'presenceabsencematrix.tsv', "\t")
    binmat = binmat.set_index('0')
    bmat = binmat.astype('float64')

    # Getting distance matrix and drawing a histogram
    Z=linkage(bmat, 'single')
    fig = plt.figure(figsize=(25,15))
    dn = dendrogram(Z,labels=bmat.index, leaf_rotation=90)
    plt.title("Heirarchial Clustering Dendogram")
    fig.savefig(working_dir+"/"+'heirarchial clustering dendogram.png')


def main():

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--location", help = "path to the Directory of files to be analysed") 
    parser.add_argument("-f", "--flag", type=int,  help = "'1' for Analysis of gene names eg. CARD and VFDB and '0' for Annotated Gff file")	
    args = parser.parse_args()
    dendogram(args.location, args.flag)
    print("\n Presence/Absence Matrix and Dendogram COMPLETED!!!!")

if __name__ == "__main__":
	main()
