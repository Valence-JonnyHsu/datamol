from typing import Optional
from typing import cast

import pkg_resources

import pandas as pd

from .io import read_sdf
from .convert import from_df
from .convert import render_mol_df


def freesolv():
    """Return the FreeSolv dataset as a dataframe.

    The dataset contains 642 molecules and the following columns:
    `['iupac', 'smiles', 'expt', 'calc']`.

    Warning:
        This dataset is only meant to be used as a toy dataset for pedagogic and
        testing purposes. **It is not** a dataset for benchmarking, analysis or
        model training.
    """

    with pkg_resources.resource_stream("datamol", "data/freesolv.csv") as f:
        data = pd.read_csv(f)
    return data


def cdk2(as_df: bool = True, mol_column: Optional[str] = "mol"):
    """Return the RDKit CDK2 dataset from `RDConfig.RDDocsDir, 'Book/data/cdk2.sdf'`.

    Args:
        as_df: Whether to return a list mol or a pandas DataFrame.
        mol_column: Name of the mol column. Only relevant if `as_df` is True.
    """

    with pkg_resources.resource_stream("datamol", "data/cdk2.sdf") as f:
        data = read_sdf(f, as_df=as_df, mol_column=mol_column)
    return data


def solubility(as_df: bool = True, mol_column: Optional[str] = "mol"):
    """Return the RDKit solubility dataset from `RDConfig.RDDocsDir, 'Book/data/solubility.{train|test}.sdf'`.

    The dataframe or the list of molecules with contain a `split` column, either `train` or `test`.

    Args:
        as_df: Whether to return a list mol or a pandas DataFrame.
        mol_column: Name of the mol column. Only relevant if `as_df` is True.
    """

    with pkg_resources.resource_stream("datamol", "data/solubility.train.sdf") as f:
        train = read_sdf(f, as_df=True, mol_column="mol", smiles_column=None)

    with pkg_resources.resource_stream("datamol", "data/solubility.test.sdf") as f:
        test = read_sdf(f, as_df=True, mol_column="mol", smiles_column=None)

    train = cast(pd.DataFrame, train)
    test = cast(pd.DataFrame, test)

    train["split"] = "train"
    test["split"] = "test"

    # NOTE(hadim): LMAO RDkit consistency xD
    test = test.rename(columns={"SMILES": "smiles"})

    data = pd.concat([train, test], ignore_index=True)

    if as_df:
        if mol_column is None:
            data = data.drop(columns=["mol"])

        render_mol_df(data)
        return data

    return from_df(data, mol_column=mol_column)
