#!/mnt/sdh/xiaoxi/.linuxbrew/bin/python3
#-*- coding:utf-8 -*-

from subprocess import Popen, PIPE

def bgzip(filename):
    """Call bgzip to compress a file."""
    Popen(['bgzip', '-f', filename])

def tabix_index(filename,
        preset="gff", chrom=1, start=4, end=5, skip=0, comment="#"):
    """Call tabix to create an index for a bgzip-compressed file."""
    Popen(['tabix', '-p', preset, '-s', chrom, '-b', start, '-e', end,
        '-S', skip, '-c', comment])

def tabix_query(filename, chrom, start, end):
    """Call tabix and generate an array of strings for each line it returns."""
    query = '{}:{}-{}'.format(chrom, start, end)
    process = Popen(['tabix', '-f', filename, query], stdout=PIPE)
    for line in process.stdout:
        yield line.strip().split()

def tabix_bed(bedfile,preset,chrom,start,end):
    """ Call tabix and query if chrom,start,end in bedfile """
    query = '{}:{}-{}'.format(chrom, start, end)
    process = Popen(['tabix', '-p',preset, bedfile , query],stdout=PIPE)
    for line in process.stdout:
        yield line.decode().strip().split()


if __name__ == "__main__":
    a=tabix_bed("/mnt/sdh/xiaoxi/database/DUST/hs37d5_LCR_20200129.bed.gz",'bed','X','66766386','66766387')
    print([i for i in a])
