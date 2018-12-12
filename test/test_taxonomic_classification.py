import unittest
import os
import subprocess


class TestTaxonomicClassification(unittest.TestCase):
    '''
        Test the taxonomic classification workflows: 
        We test by checking if the correct files are created at the end of the workflow.
    '''
#     @classmethod
#     def setUpClass(cls):
#         os.chdir("../workflows/")
#         subprocess.run('export SINGULARITY_BINDPATH="data:/tmp"')
    
    def setUp(self):
        os.chdir("../workflows/")
        os.environ['SINGULARITY_BINDPATH'] = "data:/tmp"
        
    def test_1_taxonomic_classification_signatures_workflow(self):
        #Note: This runs the comparison/compute_read_signatures rule
        snakemake_command = "snakemake -q --core=6 --use-singularity --configfile=../test/test_taxonomic_classification_workflow.json taxonomic_classification_signatures_workflow"
        subprocess.run([snakemake_command], shell=True)
        dirname = os.getcwd()
        filename_1 = os.path.join(dirname,  "data/data/SRR606249_subset10.trim2_scaled10k.k21_31_51.sig")
        filename_2 = os.path.join(dirname,  "data/SRR606249_subset10.trim30_scaled10k.k21_31_51.sig")
        self.assertTrue(os.path.isfile(filename_1) and os.path.isfile(filename_2))
        
    def test_2_taxonomic_classification_gather_workflow(self):
        snakemake_command = "snakemake -q --core=6 --use-singularity --configfile=../test/test_taxonomic_classification_workflow.json taxonomic_classification_gather_workflow"
        subprocess.run([snakemake_command], shell=True)
        dirname = os.getcwd()
        filename_1 = os.path.join(dirname,  "data/SRR606249_subset10-k21.trim2.gather_matches.csv")
        filename_2 = os.path.join(dirname,  "data/SRR606249_subset10-k21.trim2.gather_output.csv")
        filename_3 = os.path.join(dirname,  "data/SRR606249_subset10-k21.trim2.gather_unassigned.csv")
        filename_4 = os.path.join(dirname,  "data/SRR606249_subset10-k21.trim30.gather_matches.csv")
        filename_5 = os.path.join(dirname,  "data/SRR606249_subset10-k21.trim30.gather_output.csv")
        filename_6 = os.path.join(dirname,  "data/SRR606249_subset10-k21.trim30.gather_unassigned.csv")
        filename_7 = os.path.join(dirname,  "data/SRR606249_subset10-k31.trim2.gather_matches.csv")
        filename_8 = os.path.join(dirname,  "data/SRR606249_subset10-k31.trim2.gather_output.csv")
        filename_9 = os.path.join(dirname,  "data/SRR606249_subset10-k31.trim2.gather_unassigned.csv")
        filename_10 = os.path.join(dirname,  "data/SRR606249_subset10-k31.trim30.gather_matches.csv")
        filename_11 = os.path.join(dirname,  "data/SRR606249_subset10-k31.trim30.gather_output.csv")
        filename_12 = os.path.join(dirname,  "data/SRR606249_subset10-k31.trim30.gather_unassigned.csv")
        filename_13 = os.path.join(dirname,  "data/SRR606249_subset10-k51.trim2.gather_matches.csv")
        filename_14 = os.path.join(dirname,  "data/SRR606249_subset10-k51.trim2.gather_output.csv")
        filename_15 = os.path.join(dirname,  "data/SRR606249_subset10-k51.trim2.gather_unassigned.csv")
        filename_16 = os.path.join(dirname,  "data/SRR606249_subset10-k51.trim30.gather_matches.csv")
        filename_17 = os.path.join(dirname,  "data/SRR606249_subset10-k51.trim30.gather_output.csv")
        filename_18 = os.path.join(dirname,  "data/SRR606249_subset10-k51.trim30.gather_unassigned.csv")
        self.assertTrue(os.path.isfile(filename_1) and os.path.isfile(filename_2) and os.path.isfile(filename_3) and os.path.isfile(filename_4) and   
                        os.path.isfile(filename_5) and os.path.isfile(filename_6) and os.path.isfile(filename_7) and os.path.isfile(filename_8) and 
                        os.path.isfile(filename_9) and os.path.isfile(filename_10) and os.path.isfile(filename_11) and os.path.isfile(filename_12) and
                        os.path.isfile(filename_13) and os.path.isfile(filename_14) and os.path.isfile(filename_15) and os.path.isfile(filename_16) and
                        os.path.isfile(filename_17) and os.path.isfile(filename_18))
        
if __name__ == '__main__':
    unittest.main()