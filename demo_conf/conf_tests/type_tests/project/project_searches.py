from spil_tests.utils.datasearch_data import test_data
from spil_tests.utils.dualsearch_a_b import test_search_ab
from spil_tests.utils.filesearch_fs import test_fs

if __name__ == "__main__":

    from spil import Data, FS
    from spil.util.log import setLevel, ERROR, DEBUG, WARN

    setLevel(DEBUG)
    setLevel(ERROR)

    print()
    print("Sid test starts")

    searches = dict()

    searches["*"] = "All projects"
    searches["*/s"] = "all project, one type"
    searches["*/a"] = "all project, one type"
    searches["*/a,s"] = "all project, all types"
    searches["*/a,s/*"] = "all project, some types, assettypes / seqs"
    searches["*/*"] = "all project, all types"
    searches["*/*/*"] = "all project, all types, assettypes / seqs"
    # searches["*/*/*/*"] = "all project, until shots / assets"  # Too slow
    # searches["tp/*/**"] = "This is currently unsupported ! Matches work under certain conditions."
    searches["*/a/characters/**"] = "all project, all character files"

    searches["tp"] = "One project"
    searches["tp/*"] = "One project, all types "
    searches["tp/s,a"] = "one project, some types"
    searches["tp/s,a/*"] = "one project, some types, cats / seqs"
    searches["tp/a,s/*/*"] = "one project, until shots / assets"
    searches["tp/s/*/*/*"] = "one project until shot tasks"
    searches["tp/s/**/movie"] = "one project all shot movies"
    searches["tp/s/**/movie?version=>"] = "one project all shot movies, last version"
    searches["tp/a,s/**"] = "one project, all leaves under a and s"
    searches["tp/a,s/**/ma,mov,avi,abc,fbx,zprj,spp,nk"] = "one project, all leaves under a and s, with extensions"

    searches["tp/s/**/maya"] = "one project, shots, all maya files"
    searches["tp/a/**/maya"] = "one project, assets, all maya files"

    # test_fs(searches)
    test_data(searches)
    #test_search_ab(searches, Data(), FS())


