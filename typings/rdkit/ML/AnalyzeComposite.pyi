from rdkit.Dbase.DbConnection import DbConnect as DbConnect
from rdkit.ML import ScreenComposite as ScreenComposite
from rdkit.ML.Data import Stats as Stats
from rdkit.ML.DecTree import Tree as Tree, TreeUtils as TreeUtils
from typing import Any

def ProcessIt(composites: Any, nToConsider: int = ..., verbose: int = ...): ...
def ErrorStats(conn: Any, where: Any, enrich: int = ...): ...
def ShowStats(statD: Any, enrich: int = ...) -> None: ...
def Usage() -> None: ...