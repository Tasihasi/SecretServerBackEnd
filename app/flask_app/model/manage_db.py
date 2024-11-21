from ...main import db
from sqlalchemy import text

class ManageDB:
    @staticmethod
    def _delete_record(hash:str) -> bool:
        if not hash:
            return True

        try: 
            delete_query = text
            ( """
            DELETE FROM secret
            WHERE hashText = :hash;
            """)
            db.session.execute(delete_query, {'hash': hash}).fetchone()
            db.session.commit()

            return True

        except Exception as e:
            return False

    @staticmethod
    def _check_retrievals() -> None:
        try: 
            select_query = text( """
            SELECT hashText FROM secret WHERE retrievalCount <= 0;
            """)

            result = db.session.execute(select_query).fetchall()

            for row in result:
                hash = row[0]
                if not ManageDB._delete_record(hash):
                    return

        except Exception as e:
            return

    @staticmethod
    def _update_expiration_date() -> None:

        try: 
            update_query = text
            ( """
            UPDATE secret
            SET expiration = expiration - 1;
            """)
            db.session.execute(update_query).fetchall()
            db.session.commit()

        except Exception as e:
            return
        
    @staticmethod
    def _delete_expired_data() -> None:
        try: 
            select_query = text
            ( """
            SELECT hashText FROM secret WHERE expiration <= 0 AND expiration != -1;
            """)

            result = db.session.execute(select_query).fetchall()

            for row in result:
                hash = row[0]
                if not ManageDB._delete_record(hash):
                    return

        except Exception as e:
            return
        
    @staticmethod
    def ServerTick():
        ManageDB._check_retrievals()
        ManageDB._update_expiration_date()
        ManageDB._delete_expired_data()

    # TODO how to manage if the timer set to 0 and not wanting to delete?