# from flask import request
# from app import app
#
#
#
import os
from pathlib import Path
import re
import uuid

from tidb_vector.integrations import TiDBVectorClient
from peewee import Model, MySQLDatabase, TextField, SQL
import pymysql
from pymysql import Connection
from pymysql.cursors import DictCursor
from tidb_vector.peewee import VectorField

from flask import Flask, request
from flask_restful import Resource, Api
from flask import request, Response, jsonify, json, abort
from flask_restful import Resource, Api
from flask_cors import CORS


import google.generativeai as genai
from pypdf import PdfReader

from config import Config
from dotenv import load_dotenv

dotenv_path = Path("./.env")
load_dotenv(dotenv_path=dotenv_path)


app = Flask(__name__)
api = Api(app, prefix="/api")
CORS(app, resources={r"/*": {"origins": "*"}})


genai.configure(api_key=os.environ.get("API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")
embedding_model = "models/text-embedding-004"
embedding_dimensions = 768

# Init TiDB connection

db = MySQLDatabase(
    "konverse",
    user=os.environ.get("TIDB_USER"),
    password=os.environ.get("TIDB_PASSWORD"),
    host=os.environ.get("TIDB_HOST"),
    port=int(os.environ["TIDB_PORT"]),
    ssl_verify_cert=True,
    ssl_verify_identity=True,
)


def InlineFormatting(text):
    text = re.sub(r"\_(.+?)_\|", "", text)
    text = re.sub(r"\*\*(.+?)\*\*", "", text)
    return text


class NewDocumentEmbeddings(Resource):
    def post(self):
        documents = []

        if request.files.get("pdf_file"):
            reader = PdfReader(request.files.get("pdf_file"))
            pages = len(reader.pages)

            for page in range(int(pages)):
                _page = reader.pages[page]

                documents.append(re.sub(r"[^a-zA-Z0-9\s]", "", _page.extract_text()))

            embeddings = genai.embed_content(
                model=embedding_model, content=documents, task_type="retrieval_document"
            )

            class DocModel(Model):
                text = TextField()
                embedding = VectorField(dimensions=embedding_dimensions)

                class Meta:
                    database = db
                    table_name = request.form.get("filename")

                    def __str__(self):
                        return self.text

            db.connect()
            db.drop_tables([DocModel])
            db.create_tables([DocModel])

            data_source = [
                {"text": doc, "embedding": emb}
                for doc, emb in zip(documents, embeddings["embedding"])
            ]

            DocModel.insert_many(data_source).execute()

            return jsonify(response="Success")

        else:
            abort(400)


api.add_resource(NewDocumentEmbeddings, "/embeddings/new")


class GetDocumentEmbeddings(Resource):
    def post(self):
        query = request.form.get("prompt")

        query_embeddings = genai.embed_content(
            model=embedding_model, content=[query], task_type="retrieval_query"
        )["embedding"][0]

        class DocModel(Model):
            text = TextField()
            embedding = VectorField(dimensions=len(query_embeddings))

            class Meta:
                database = db
                table_name = request.form.get("document")

            def __str__(self):
                return self.text

        related_docs = (
            DocModel.select(
                DocModel.text,
                DocModel.embedding.cosine_distance(query_embeddings).alias("distance"),
            )
            .order_by(SQL("distance"))
            .limit(3)
        )

        docs = []

        for doc in related_docs:
            docs.append(doc.text)

        db.close()

        context = " ".join(docs)
        prompt = f"{ query } in this { context } context"
        response = model.generate_content(prompt)

        return jsonify(response=InlineFormatting(response.text))


api.add_resource(GetDocumentEmbeddings, "/embeddings")


class SummarizeText(Resource):
    def post(self):
        query = request.form.get("prompt")

        query_embeddings = genai.embed_content(
            model=embedding_model, content=[query], task_type="retrieval_query"
        )["embedding"][0]

        class DocModel(Model):
            text = TextField()
            embedding = VectorField(dimensions=len(query_embeddings))

            class Meta:
                database = db
                table_name = request.form.get("document")

            def __str__(self):
                return self.text

        related_docs = (
            DocModel.select(
                DocModel.text,
                DocModel.embedding.cosine_distance(query_embeddings).alias("distance"),
            )
            .order_by(SQL("distance"))
            .limit(3)
        )

        docs = []

        for doc in related_docs:
            docs.append(doc.text)

        db.close()

        context = " ".join(docs)
        prompt = f"summarize  this { query } in this { context } context."
        response = model.generate_content(prompt)

        return jsonify(response=InlineFormatting(response.text))


api.add_resource(SummarizeText, "/summarize")


if __name__ == "__main__":
    app.run(debug=True)
