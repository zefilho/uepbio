# coding: utf-8

from django.template.defaultfilters import slugify
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import generic_dna
from Bio.Align.Applications import ClustalwCommandline
from Bio import SeqIO
from Bio import AlignIO
from Bio import Phylo

from Bio.Align import MultipleSeqAlignment
from StringIO import StringIO
import os, sys

# Models' functions

def nomear_imagem(instance, filename):
    nome = [n.lower() for n in instance.nome_cientifico.split(' ', 2)]
    extensao = os.path.splitext(filename)[-1]
    return 'plantas/%s/%s%s' % (slugify(nome[0]), slugify(nome[1]), extensao)


def nomear_sequencia(instance, filename):
    nome = instance.planta.nome_cientifico.lower().replace(' ', '_')
    if instance.tipo == 'P':
        return 'sequencias/%s/proteina/%s.fasta' % (slugify(nome), slugify(instance.titulo))
    elif instance.tipo == 'N':
        return 'sequencias/%s/nucleotideo/%s.fasta' % (slugify(nome), slugify(instance.titulo))

# Views' functions

def paginar(queryset, request, quant_por_pagina=10):
    paginator = Paginator(queryset, quant_por_pagina)
    pagina = request.GET.get('pagina', '1')
    try:
        pagina_atual = paginator.page(pagina)
    except PageNotAnInteger:
        pagina_atual = paginator.page(1)
    except EmptyPage:
        pagina_atual = paginator.page(paginator.num_pages)
    return pagina_atual

from Bio.Phylo.PhyloXML import Phylogeny
import pylab

def alinhar(seq_one, seq_two):
	teste_one = SeqRecord(Seq('%s'%seq_one,generic_dna),id = '1')
	teste_two = SeqRecord(Seq('%s'%seq_two,generic_dna),id = '2')
	lista = [teste_one, teste_two]
	SeqIO.write(lista,"alinhamento.fasta","fasta")
	align1 = MultipleSeqAlignment([
             SeqRecord(Seq("ACTGCTAGCTAGACTGCTAGCTAGACTGCTAGCTAGACTGCTAGDTAGACTGCTAGDTAG", generic_dna), id="Alpha"),
             SeqRecord(Seq("ACT-CTAGCTAGACT-CTAGCTAGACT-CTAGCTAGACTGCTAGDTAGACTGCTAGDTAG", generic_dna), id="Beta"),
             SeqRecord(Seq("ACTGCTAGDTAGACTGCTAGDTAGACTGCTAGDTAG------------------------", generic_dna), id="Gamma"),
         ])
	#clustal
	out_handle = StringIO()
	SeqIO.write(lista,out_handle,'fasta')
	align1 = out_handle.getvalue()
	clus_exe = r"C:\Program Files\ClustalW2\clustalw2.exe"
	assert os.path.isfile(clus_exe),"Clustal Executado"
	clus_line = ClustalwCommandline(clus_exe,infile='alinhamento.fasta')
	stdout,stdeer = clus_line()
	
	align = AlignIO.read("alinhamento.aln", "clustal")
	#align = AlignIO.convert("alinhamento.aln", "clustal", "tese.fasta", "fasta")
	arvore = Phylo.read("alinhamento.dnd","newick")
	arvore2 = Phylo.parse('tree1.xml','phyloxml').next()
	tree = Phylogeny.from_tree(arvore)
	Phylo.convert('alinhamento.dnd','newick', "tree1.nex", "nexus")
	
	#Phylo.draw_ascii(arvore)
	#pylab.show()
	#pylab.savefig('arvore.png')
	
	#a = Phylo.draw(arvore)
	#alignments = [x for x in AlignIO.parse("alinhamento.aln", "clustal")]
	#out_handle = StringIO()
	
	#AlignIO.write([align1], out_handle, "phylip")
	#clustal_data = out_handle.getvalue()
	
	return align, align[1].seq, arvore2
	
#Motifs

from Bio import Motif
from Bio.Alphabet import IUPAC
from Bio.SeqUtils import GC
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
def motifs_teste(seq):
	motifs = Motif.Motif(alphabet=IUPAC.unambiguous_dna)
	motifs.add_instance(Seq("AAAAAAAAAATAATTTTTTTTTTGTGTGTGTGT",motifs.alphabet))
	motifs.add_instance(Seq("GGGGGGGGGGTAAGGGGGGGGGGATATATATAT",motifs.alphabet))
	motifs.add_instance(Seq("GGGAAAAAGGTAAGGGGGGGGGGATATATATAT",motifs.alphabet))
	test_seq=Seq("TATGATGTAGTATAATATAATTATAA",motifs.alphabet)
	fasta_string = open("zeamays.fasta").read()
	#result_handle = NCBIWWW.qblast("blastn","nr", fasta_string)
	#lista = ['%s - %s</br>'%(pos, seq.tostring()) for pos , seq in motifs.search_instances(test_seq)]
	#return lista
	#save_file = open("my_blast.xml", "w")
	#save_file.write(result_handle.read())
	#save_file.close()
	#result_handle.close()
	result_handle = open("my_blast.xml")
	blast_records = NCBIXML.parse(result_handle)
	t = blast_records.next()
	l = [blast for blast in t.alignments]
	return '****Alinhamento******\nSequencia: %s\n\nLenght: %s\nE-value: %0.5f\n\n\
%s...\n%s...\n%s...'%(l[1].title,l[1].length,l[1].hsps[0].expect,l[1].hsps[0].query[:65],l[1].hsps[0].match[:65],l[1].hsps[0].sbjct[:65])
	
	