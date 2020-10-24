import unittest
import pathlib

import datamol as dm

ROOT_DIR = pathlib.Path(__file__).parent.resolve()
DATA_DIR = ROOT_DIR / "data"


class TestMol(unittest.TestCase):
    def test_to_mol(self):
        smiles = "O=C(C)Oc1ccccc1C(=O)O"
        mol = dm.to_mol(smiles)
        assert mol.GetNumAtoms() == 13

        smiles = "O=C(C)Oc1ccccc1C(=O)O"
        mol = dm.to_mol(smiles, add_hs=True)
        assert mol.GetNumAtoms() == 21

        smiles = "fake_smiles"
        mol = dm.to_mol(smiles)
        assert mol is None

    def test_reorder_atoms(self):
        smiles = "c1ccc(C(=O)O)c(c1)OC(=O)C"
        mol = dm.to_mol(smiles, add_hs=False, explicit_only=False)

        orders = [a.GetAtomicNum() for a in mol.GetAtoms()]
        assert orders == [6, 6, 6, 6, 6, 8, 8, 6, 6, 8, 6, 8, 6]

        mol = dm.reorder_atoms(mol)
        orders = [a.GetAtomicNum() for a in mol.GetAtoms()]
        assert orders == [6, 8, 8, 8, 6, 6, 6, 6, 8, 6, 6, 6, 6]

    def test_randomize_atoms(self):
        smiles = "c1ccc(C(=O)O)c(c1)OC(=O)C"
        mol = dm.to_mol(smiles)
        orders = [a.GetAtomicNum() for a in mol.GetAtoms()]

        randomized_mol = dm.randomize_atoms(mol)
        randomized_orders = [a.GetAtomicNum() for a in mol.GetAtoms()]

        assert sum(orders) == sum(randomized_orders)

    def test_to_neutral(self):

        # NOTE(hadim): add a more complex test.
        smiles = "[NH4+]"
        mol = dm.to_mol(smiles, add_hs=False, explicit_only=False)

        smiles = dm.to_smiles(dm.to_neutral(mol))
        assert smiles == "[NH4]"

    def sanitize_mol(self):
        # NOTE(hadim): not testing much here. Improve me please.
        smiles = "CC(=O)Oc1ccccc1C(=O)O"
        mol = dm.to_mol(smiles, sanitize=False)
        mol = dm.sanitize_mol(mol, charge_neutral=True)
        assert dm.to_smiles(mol) == "CC(=O)Oc1ccccc1C(=O)O"

        mol = dm.sanitize_mol(None, charge_neutral=True)
        assert mol is None

    def test_to_smiles(self):

        smiles = "O=C(C)Oc1ccccc1C(=O)O"
        mol = dm.to_mol(smiles)

        smiles = dm.to_smiles(
            mol,
            isomeric=True,
            ordered=True,
            explicit_bonds=False,
            explicit_hs=False,
        )
        assert smiles == "CC(=O)Oc1ccccc1C(=O)O"

        smiles = dm.to_smiles(
            mol,
            isomeric=True,
            ordered=False,
            explicit_bonds=True,
            explicit_hs=False,
        )
        assert smiles == "C-C(=O)-O-c1:c:c:c:c:c:1-C(=O)-O"

        smiles = dm.to_smiles(
            mol,
            isomeric=True,
            ordered=False,
            explicit_bonds=False,
            explicit_hs=True,
        )
        assert smiles == "[CH3][C](=[O])[O][c]1[cH][cH][cH][cH][c]1[C](=[O])[OH]"

        smiles = "O=C(C)Oc1ccccc1C(=O)O"
        mol = dm.to_mol(smiles)
        randomized_smiles = dm.to_smiles(mol, randomize=True)
        randomized_mol = dm.to_mol(randomized_smiles)

        assert dm.to_smiles(randomized_mol) == dm.to_smiles(mol)

    def test_to_selfies(self):
        smiles = "CC(=O)Oc1ccccc1C(=O)O"
        mol = dm.to_mol(smiles)

        true_sf = "[C][C][Branch1_2][C][=O][O][C][=C][C][=C][C][=C][Ring1][Branch1_2][C][Branch1_2][C][=O][O]"

        selfies = dm.to_selfies(smiles)
        assert selfies == true_sf

        selfies = dm.to_selfies(mol)
        assert selfies == true_sf

    def test_from_selfies(self):
        selfies = "[C][C][Branch1_2][C][=O][O][C][=C][C][=C][C][=C][Ring1][Branch1_2][C][Branch1_2][C][=O][O]"

        smiles = dm.from_selfies(selfies, as_mol=False)
        assert smiles == "CC(=O)OC1=CC=CC=C1C(=O)O"

        mol = dm.from_selfies(selfies, as_mol=True)
        assert dm.to_smiles(mol) == "CC(=O)Oc1ccccc1C(=O)O"

    def test_to_smarts(self):
        smiles = "O=C(C)Oc1ccccc1C(=O)O"
        mol = dm.to_mol(smiles)

        smarts = dm.to_smarts(mol, keep_hs=True)
        assert smarts == "[CH3]-[C](=[O])-[O]-[c]1:[cH]:[cH]:[cH]:[cH]:[c]:1-[C](=[O])-[OH]"

        smarts = dm.to_smarts(mol, keep_hs=False)
        assert smarts == "[CH3]-[C](=[O])-[O]-[c]1:[cH]:[cH]:[cH]:[cH]:[c]:1-[C](=[O])-[OH]"

        assert dm.to_smarts(None) is None

    def test_inchi(self):
        smiles = "CC(=O)Oc1ccccc1C(=O)O"
        mol = dm.to_mol(smiles)

        inchi = dm.to_inchi(mol)
        assert inchi == "InChI=1S/C9H8O4/c1-6(10)13-8-5-3-2-4-7(8)9(11)12/h2-5H,1H3,(H,11,12)"

        inchikey = dm.to_inchikey(mol)
        assert inchikey == "BSYNRYMUTXBXSQ-UHFFFAOYSA-N"

        new_mol = dm.from_inchi(inchi)
        assert dm.to_smiles(new_mol) == smiles

        assert dm.to_inchi(None) is None
        assert dm.to_inchikey(None) is None
        assert dm.from_inchi(None) is None
