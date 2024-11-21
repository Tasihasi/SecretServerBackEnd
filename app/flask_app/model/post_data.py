from datetime import datetime, timedelta
import hashlib
from ...main import db
from sqlalchemy import text

class PostData:
    def __init__(self, secret_text: str, expire_after_views: int, expire_after: int):

        if expire_after_views < 1:
            raise ValueError("Expiration values must be non-negative")
        if expire_after < 0:
            raise ValueError("Expiration time must be non-negative")
        elif expire_after == 0:
            self.expire_after = -1
            self._expiration_date = self._calculate_expiration(99999999)
        
        self._secret_text = secret_text
        self._expire_after_views = expire_after_views
        
        self._expire_after = expire_after
        self._hash = self._generate_unique_hash()
        self._created_at = datetime.now()
        self._expiration_date = self._calculate_expiration(expire_after)

    @property
    def secret_text(self) -> str:
        return self._secret_text

    @secret_text.setter
    def secret_text(self, value) -> None:
        self._secret_text = value

    @property
    def expire_after_views(self) -> int:
        return self._expire_after_views

    @expire_after_views.setter
    def expire_after_views(self, value) -> None:
        if value < 0:
            raise ValueError("expire_after_views must be non-negative")
        self._expire_after_views = value

    @property
    def expire_after(self) -> int:
        return self._expire_after

    @expire_after.setter
    def expire_after(self, value) -> None:
        if value < 0:
            raise ValueError("expire_after must be non-negative")
        self._expire_after = value

    @property
    def hash(self) -> str:
        return self._hash

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def expiration_date(self) -> datetime:
        return self._expiration_date

    def _generate_hash(self):
        return hashlib.sha256(self.secret_text.encode()).hexdigest()
    
    def _is_hash_unique(self, hash: str) -> bool:
        query = text( "SELECT 1 FROM secret WHERE hashText = :hash LIMIT 1;")
        result = db.session.execute(query, {'hash': hash})
        db.session.close()
        return result is None
    
    def _generate_unique_hash(self) -> str:
        while True:
            generated_hash = self._generate_hash()
            if self._is_hash_unique(generated_hash):
                return generated_hash

    def _calculate_expiration(self, minutes : int):
        return self.created_at + timedelta(minutes=minutes)
    
    def _check_necessary_data(self) -> bool:
        if self.hash and self.secret_text and self.expire_after and self.expire_after_views:
            return True
        
        return False
    
    def post_to_db(self) -> bool:

        if not self._check_necessary_data():
            return False
        
        if self._expiration_date:
            expiration_date_str = self._expiration_date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            expiration_date_str = None

        # Prepare the insert query and data
        query = text(  """
        INSERT INTO secret (hashText, secretMessage, retrievalCount, expiration)
        VALUES (:hash, :secretMessage, :retrievalCount, :expiration)
        """)

        data = {
            'hash': self.hash,
            'secretMessage': self.secret_text,
            'retrievalCount': self.expire_after_views,
            'expiration': self.expire_after
        }

        try:
            # Execute the query and commit the transaction

            db.session.execute(query, data)
            db.session.commit()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            db.session.rollback()
            return False
    
    
