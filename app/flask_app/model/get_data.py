from flask import jsonify
from sqlalchemy import text
from datetime import datetime

class GetData:
    def __init__(self, hash : str):
        self._hash = hash
        self.current_time = self._gen_current_time_to_int()
        print(f"Current time: {self.current_time}")

    @property
    def get_hash(self) -> str:
        return self._hash

    def _decode_text(self, text : str) -> str:
        # implement some logic 
        return text
    
    def _gen_current_time_to_int(self):
        # Get the current time
        now = datetime.now()
        
        # Extract hour and minute
        hour = now.hour
        minute = now.minute
        
        # Combine hour and minute into an integer in the format HHMM
        time_int = hour * 60 + minute
        
        return time_int

    def _get_text_from_db(self) -> str:
        if not self._hash:
            return "Hash was not provided."
        
        # Needs to delete the import because the ManageDB is imported from this module
        # IF the db is not declared  before importing -> circular import error
        from ...main import db
        

        try:
            update_query = text("""
            UPDATE secret
            SET retrievalCount = retrievalCount - 1
            WHERE hashText = :hash AND retrievalCount > 0;
            """)
            

            select_query = text("""
            SELECT secretMessage FROM secret WHERE hashText = :hash AND retrievalCount > 0 AND expiration >= :current_time;
            """)
            result = db.session.execute(select_query, {'hash': self._hash, "current_time" : self.current_time}).fetchone()

            db.session.execute(update_query, {'hash': self._hash})
            db.session.commit()

            if result:
                return result[0]
            else:
                return "No secret found for this hash."
            
        except Exception as e:
            return f"An error occurred while retrieving the secret. Exception : {e}"

    
    def get_secret(self):
        return jsonify({"secret" : str(self._decode_text(self._get_text_from_db()))}), 200
