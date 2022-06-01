import epp_reader as r
import epp_writer as w

if __name__ == '__main__':
    filename = "evaluations_20211220-164427.csv"
    tempfile = "temp.csv"
    
    r.clean_csv(filename, tempfile)
    
    print("Reading " + filename)
    rows = r.read_csv(tempfile)
    epp = r.parse(rows)
    
    print("Computing scores")
    epp.compute(0, 3)
    print(epp)
    
    print("Writing ")
    w.write_xlsx("temp.xlsx", epp) 