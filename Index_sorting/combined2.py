from subprocess import call
import os
import tempfile
import sys

cwd = os.getcwd()
inFile = open(sys.argv[1],'r')
#Data storage strings
s502header = ''
s502data = ''

#quary="+AGAGGATA"
#List of quary string
quary2=["+ATAGAGAG", "+AGAGGATA", "+TCTACTCT", "+TCTTACGC"]

#Storage of hits
s502 = []
Name=['ATAGAGAG', 'AGAGGATA', 'TCTACTCT', 'TCTTACGC']
#Enumerated tuple of the quary list. Cycles through each quary and gives it a number
for i, barcode in enumerate(quary2):
        inFile.seek(0)
        s502 = []
        s502header=''
        s502data=''
        for line in inFile:
            if line[0] == "@":
                hit=0
                if barcode in line:
                    hit=1
                    s502.append((1,line))
            else:
                if hit==1:
                    s502.append((1,line))
        f=open(cwd +"/Reads_%s.fq" % Name[i], 'w')
        for item in s502:
            f.write(item[1])
        f.close()
    


Files = []
Files += os.listdir()
store=[]
quary="Read"
name=''
path=[]
cwd = os.getcwd()

for a in Files:
    if quary in a:
        store.append((1,a))

for i in store:
    path.append(""+cwd+"/"+i[1]+"")

Name=['AlignTest_A.csv', 'AlignTest_B.csv', 'AlignTest_C.csv', 'AlignTest_D.csv']

blastDB ='/media/sf_GeCKO/Installation/LibM.db'

#Temporary paths and files for storing interrim datasets

g=''
e=0

for part in path:
    print("PROCESSING"+ part +"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    fd, tmp = tempfile.mkstemp('.fq')
    fs, tmp2 = tempfile.mkstemp('.fa')
    print("ALLIGNING TO U6 BINDING SITE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    call(["/media/sf_GeCKO/Installation/bbmap/bbduk.sh in=" + part + " outm="+ tmp +" k=23 hdist=1 ref=/media/sf_GeCKO/Installation/AlexAdapt.fa"], shell=True)
    print("TRIMMING AND MAKING UNIQUE LIST!!!!!!!!!!!!!!!!!!!!!!!")
    call(["/media/sf_GeCKO/Installation/bbmap/bbduk.sh in=" + tmp + " out=stdout.fq ftl=0 ftr=19 | /media/sf_GeCKO/Installation/bbmap/kmercountexact.sh in=stdin.fq k=20 out=" + tmp2 + " overwrite=true"], shell=True)
    
    file=open(tmp)
    data=file.read()
    os.close(fd)
    os.remove(tmp)
    g=Name[e]
    call(["blastn -max_target_seqs 1 -word_size 7 -db " + blastDB + " -outfmt 10 -query "+ tmp2 + " -out /media/sf_GeCKO/Installation/CombinedTest/" + Name[e] +""], shell=True)
    print("FINISHED ALIGNMENT!!!!!!!!!!!!!!!!!!!!!!!!!"+ g +"")
    
    e+=1
    file=open(tmp2)
    data=file.read()
    os.close(fs)
    os.remove(tmp2)

    
#/media/sf_GeCKO/Installation/Status_from_initial_alignment/pB1M.fq