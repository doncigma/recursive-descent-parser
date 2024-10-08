from Parser import Parser
import sys

def main():
    if len(sys.argv) == 3:
        inFile = "..\\text-sets\\" + sys.argv[1]
        outFile = "..\\output-files\\" + sys.argv[2]
        parser = Parser()
        parser.parse_file(inFile, outFile)
    else:
        print("Only provide 2 arguments: \"python input-file.txt output-file.json\"", "Make sure the files are in their correct directories (check README)")

if __name__ == "__main__":
    main()
