from ...main import db
from sqlalchemy import text
import datetime

class ManageDB:
    @staticmethod
    def _delete_record(hash:str) -> bool:
        if not hash:
            return True

        try: 
            delete_query = text( """
            DELETE FROM messages
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
            SELECT hashText FROM messages WHERE retrievalCount <= 0;
            """)

            result = db.session.execute(select_query).fetchall()

            for row in result:
                hash = row[0]
                if not ManageDB._delete_record(hash):
                    return

        except Exception as e:
            return


    @staticmethod
    def _delete_expired_data() -> None:
        try:
            # Get the current time
            current_time = datetime.now()

            # Query to select hashText where expiration is in the past and expiration is not -1
            select_query = text("""
            SELECT hashText, expiration FROM messages WHERE expiration != -1
            """)

            result = db.session.execute(select_query).fetchall()

            for row in result:
                hash = row[0]
                expiration_date = row[1]

                # Check if the expiration date is in the past
                if expiration_date and expiration_date < current_time:
                    # If the expiration date is in the past, delete the record
                    if not ManageDB._delete_record(hash):
                        return  # Stop if any delete fails

        except Exception as e:
            print(f"An error occurred: {e}")
            return
        
    @staticmethod
    def ServerTick():
        ManageDB._check_retrievals()
        ManageDB._delete_expired_data()

    # TODO how to manage if the timer set to 0 and not wanting to delete?