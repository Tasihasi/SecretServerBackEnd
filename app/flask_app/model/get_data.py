from flask import jsonify
from flask_app import db


class GetData:
    def __init__(self, hash : str):
        self._hash = hash

    @property
    def get_hash(self) -> str:
        return self._hash

     # Hash will be not set after creation


    def _decode_text(self, text : str) -> str:

        # implement some logic 
        return text
    
    def _get_text_from_db(self) -> str:
        if not self._hash:
            return "Hash was not provided."

        # Get the database connection
        db = get_db()
        try:

            # Decrease the retrieval count, ensuring it is only updated if count > 0
            update_query = """
            UPDATE secret
            SET retrievalCount = retrievalCount - 1
            WHERE hashText = ? AND retrievalCount > 0;
            """
            db.execute(update_query, (self._hash,))
            db.commit()

            # Now fetch the secretMessage from the same row
            select_query = """
            SELECT secretMessage FROM secret WHERE hashText = ? AND retrievalCount > 0;
            """
            result = db.execute(select_query, (self._hash,)).fetchone()



            # If a row is found, return the secretMessage, otherwise return a default message
            if result:
                return result['secretMessage']
            else:
                return "No secret found for this hash."
        except Exception as e:
            return f"An error occurred while retrieving the secret. Exception : {e}"

    
    def get_secret(self):
        return jsonify({"secret" : str(self._decode_text(self._get_text_from_db()))}), 200

