import json
import lucene
import os
import logging
from org.apache.lucene.store import NIOFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, TextField, StringField, IntPoint, StoredField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, DirectoryReader
from org.apache.lucene.queryparser.classic import MultiFieldQueryParser, QueryParser
from org.apache.lucene.search import IndexSearcher, BooleanClause, BooleanQuery
from org.apache.lucene.search.similarities import BM25Similarity
from flask import request, Flask, render_template

# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Sample JSON file path
json_file_path = 'output.json'
index_dir_path = 'sample_lucene_index/'

def create_index(storedir):
    try:
        logging.info("Initializing Lucene VM...")
        lucene.initVM()
        logging.info("Lucene VM initialized.")
        
        index_dir = NIOFSDirectory(Paths.get(storedir))
        analyzer = StandardAnalyzer()
        config = IndexWriterConfig(analyzer)
        writer = IndexWriter(index_dir, config)
        
        logging.info("IndexWriter created.")
        
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            logging.info(f"Loaded {len(data)} entries from JSON file.")
            for entry in data:
                doc = Document()
                doc.add(StringField("subreddit", entry["subreddit"], Field.Store.YES))
                doc.add(StringField("author", entry["author"], Field.Store.YES))
                doc.add(TextField("title", entry["title"], Field.Store.YES))
                doc.add(TextField("selftext", entry["selftext"], Field.Store.YES))
                doc.add(StringField("post_id", entry["post ID"], Field.Store.YES))
                doc.add(IntPoint("score", entry["score"]))
                doc.add(StoredField("score_val", entry["score"]))  # Store the score as a separate field for retrieval
                doc.add(StringField("permalink", entry["permalink"], Field.Store.YES))
                doc.add(StringField("image_url", entry["image url"], Field.Store.YES))
                
                writer.addDocument(doc)
                logging.debug(f"Added document for post ID: {entry['post ID']}")

                for comment in entry.get("comments", []):
                    comment_doc = Document()
                    comment_doc.add(StringField("post_id", entry["post ID"], Field.Store.YES))
                    comment_doc.add(StringField("author", comment["author"], Field.Store.YES))
                    comment_doc.add(TextField("body", comment["body"], Field.Store.YES))
                    writer.addDocument(comment_doc)
                    logging.debug(f"Added comment for post ID: {entry['post ID']}")
                    
        writer.close()
        logging.info("Index created successfully.")
    except Exception as e:
        logging.error("Error in create_index: %s", e)
        raise

def retrieve(storedir, query):
    try:
        lucene.getVMEnv().attachCurrentThread()
        search_dir = NIOFSDirectory(Paths.get(storedir))
        searcher = IndexSearcher(DirectoryReader.open(search_dir))
        searcher.setSimilarity(BM25Similarity())
        
        analyzer = StandardAnalyzer()
        parserTitle = QueryParser('title', analyzer)
        parserSelftext = QueryParser('selftext', analyzer) 
        parserBody = QueryParser('body', analyzer) 

        query_title = parserTitle.parse(query)
        query_selftext = parserSelftext.parse(query)
        query_body = parserBody.parse(query)

        boolean_query = BooleanQuery.Builder()
        boolean_query.add(query_title, BooleanClause.Occur.SHOULD);
        boolean_query.add(query_selftext, BooleanClause.Occur.SHOULD);
        boolean_query.add(query_body, BooleanClause.Occur.SHOULD);

        parsed_query = boolean_query.build()
        
        top_docs = searcher.search(parsed_query, 10).scoreDocs
        topk_docs = []
        logging.info("5")
        for hit in top_docs:
            doc = searcher.doc(hit.doc)
            topk_docs.append({
                "score": hit.score,
                "subreddit": doc.get("subreddit"),
                "author": doc.get("author"),
                "title": doc.get("title"),
                "url": doc.get("url"),
                "selftext": doc.get("selftext"),
                "post_id": doc.get("post_id"),
                "score_val": doc.get("score_val"),
                "permalink": doc.get("permalink"),
                "image_url": doc.get("image_url"),
                "body": doc.get("body")
            })
        return topk_docs

    except Exception as e:
        logging.error("Error in retrieve: %s", e)
        raise

@app.route("/", methods=['POST', 'GET'])
def home():
    try:
        return render_template('input.html')
    except Exception as e:
        logging.error("Error in /input route: %s", e)
        return "Internal Server Error", 500

#@app.route("/input", methods=['POST', 'GET'])
#def input():
#    try:
#        return render_template('input.html')
#    except Exception as e:
#        logging.error("Error in /input route: %s", e)
#        return "Internal Server Error", 500

@app.route("/output", methods=['POST', 'GET'])
def output():
    if request.method == 'GET':
        return "Nothing to display"
    if request.method == 'POST':
        try:
            form_data = request.form
            query = form_data['query']
            lucene.getVMEnv().attachCurrentThread()
            print(query)
            docs = retrieve(index_dir_path, str(query))
            print(docs)
            
            return render_template('output.html', lucene_output=docs)
        except Exception as e:
            logging.error("Error in /output route: %s", e)
            return "Internal Server Error", 500

lucene.initVM(vmargs=['-Djava.awt.headless=true'])

if not os.path.exists(index_dir_path) or not os.listdir(index_dir_path):
    os.makedirs(index_dir_path, exist_ok=True)
    logging.info("Creating index as it doesn't exist or is empty")
    create_index(index_dir_path)

