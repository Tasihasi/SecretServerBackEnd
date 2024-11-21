from flask import jsonify

from sqlalchemy import text

class GetData:
    def __init__(self, hash : str):
        self._hash = hash

    @property
    def get_hash(self) -> str:
        return self._hash

    def _decode_text(self, text : str) -> str:
        # implement some logic 
        return text
    
    def _get_text_from_db(self) -> str:
        if not self._hash:
            return "Hash was not provided."
        
        from ...main import db

        try:
            update_query = text
            ("""
            UPDATE secret
            SET retrievalCount = retrievalCount - 1
            WHERE hashText = :hash AND retrievalCount > 0;
            """)
            db.session.execute(update_query, {'hash': self._hash})
            db.session.commit()

            select_query = text
            ("""
            SELECT secretMessage FROM secret WHERE hashText = :hash AND retrievalCount > 0;
            """)
            result = db.session.execute(select_query, {'hash': self._hash}).fetchone()

            if result:
                return result[0]
            else:
                return "No secret found for this hash."
            
        except Exception as e:
            return f"An error occurred while retrieving the secret. Exception : {e}"

    
    def get_secret(self):
        return jsonify({"secret" : str(self._decode_text(self._get_text_from_db()))}), 200
