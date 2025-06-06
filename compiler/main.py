import os, time, shutil, argparse, logging, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from compiler.helpers.dataset import parseDatasetFile
from compiler.helpers.parseContent import parseMarkdownFiles
from compiler.report.generateTaxcoReport import generateTaxcoReport
from compiler.report.generateContentReport import generateContentReport
from compiler.report.populate import populateTaxcoReport, populateContentReport
from compiler.helpers.media import fillMediaList, processMediaList
from compiler.config import DATASET_PATH, SRC_DIR, DEST_DIR

class ContentCompiler:
    def __init__(self, skipLinkCheck: bool = False):
        self.skipLinkCheck = skipLinkCheck
        self.setupLogging()

    @staticmethod
    def setupLogging():
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def handlePaths(self):
        # Check if the dataset and source directory exist
        if not os.path.exists(DATASET_PATH):
            raise FileNotFoundError(f"Dataset file {DATASET_PATH} not found.")
        if not os.path.exists(SRC_DIR):
            raise FileNotFoundError(f"Source directory {DATASET_PATH} not found.")
        
        # Create destination directory
        if os.path.exists(DEST_DIR):
            shutil.rmtree(DEST_DIR)
        os.mkdir(DEST_DIR)

    def compile(self):
        try:            
            # Handle paths checking and creation
            self.handlePaths()
            
            logging.info("Starting content compilation...")
            
            parseDatasetFile()
            logging.info("Dataset parsed successfully")
            
            populateTaxcoReport()
            populateContentReport()
            logging.info("Reports populated")
            
            fillMediaList()
            logging.info("Candidate media files initialized")
            
            parseMarkdownFiles(self.skipLinkCheck)
            logging.info("Markdown files parsed")
            
            processMediaList()
            logging.info("Media validation finalized")
            
            generateTaxcoReport()
            generateContentReport()
            logging.info("Reports generated successfully")
            
        except Exception as e:
            logging.error(f"Error during compilation: {str(e)}", exc_info=True)
            raise

def main():
    parser = argparse.ArgumentParser(description="Compile content script.")
    parser.add_argument('--skip-link-check', required=False, action='store_true', help='Skip link check in markdown helpers.')
    args = parser.parse_args()

    startTime = time.time()
    
    try:
        compiler = ContentCompiler(skipLinkCheck=args.skip_link_check)
        compiler.compile()
    except Exception as e:
        logging.error(f"Compilation failed: {str(e)}")
        exit(1)
    finally:
        elapsedTime = time.time() - startTime
        logging.info(f"Execution time: {elapsedTime:.2f} seconds")

if __name__ == "__main__":
    main()
